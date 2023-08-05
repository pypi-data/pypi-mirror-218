r"""
Module to run an animal detection model on images.

The main function in this script also renders the predicted
bounding boxes on images and saves the resulting images (with bounding boxes).

This script is not a good way to process lots of images (tens of thousands,
say). It does not facilitate checkpointing the results so if it crashes you
would have to start from scratch. If you want to run a detector (e.g., ours)
on lots of images, you should check out:

1) run_detector_batch.py (for local execution)

2) https://github.com/ecologize/CameraTraps/tree/master/api/batch_processing
   (for running large jobs on Azure ML)

To run this script, we recommend you set up a conda virtual environment
following instructions in the Installation section on the main README, using
`environment-detector.yml` as the environment file where asked.

This is a good way to test our detector on a handful of images and get
super-satisfying, graphical results.  It's also a good way to see how fast a
detector model will run on a particular machine.

If you would like to *not* use the GPU on the machine, set the environment
variable CUDA_VISIBLE_DEVICES to "-1".

If no output directory is specified, writes detections for c:\foo\bar.jpg to
c:\foo\bar_detections.jpg.

This script will only consider detections with > 0.005 confidence at all times.
The `threshold` you provide is only for rendering the results. If you need to
see lower-confidence detections, you can change
DEFAULT_OUTPUT_CONFIDENCE_THRESHOLD.

Reference:
https://github.com/tensorflow/models/blob/master/research/object_detection/inference/detection_inference.py
"""

#%% Constants, imports, environment

import glob
import os
import statistics
import sys
import time
import warnings

import humanfriendly
from tqdm import tqdm

import imageUtils as image_utils

# ignoring all "PIL cannot read EXIF metainfo for the images" warnings
warnings.filterwarnings('ignore', '(Possibly )?corrupt EXIF data', UserWarning)

# Metadata Warning, tag 256 had too many entries: 42, expected 1
warnings.filterwarnings('ignore', 'Metadata warning', UserWarning)

# Numpy FutureWarnings from tensorflow import
warnings.filterwarnings('ignore', category=FutureWarning)

# Useful hack to force CPU inference
# os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


# An enumeration of failure reasons
FAILURE_INFER = 'Failure inference'
FAILURE_IMAGE_OPEN = 'Failure image access'

# Number of decimal places to round to for confidence and bbox coordinates
CONF_DIGITS = 3
COORD_DIGITS = 4

# Label mapping for MegaDetector
DEFAULT_DETECTOR_LABEL_MAP = {
    '1': 'animal',
    '2': 'person',
    '3': 'vehicle'  # available in megadetector v4+
}

# Should we allow classes that don't look anything like the MegaDetector classes?
USE_MODEL_NATIVE_CLASSES = False

# Each version of the detector is associated with some "typical" values
# that are included in output files, so that downstream applications can 
# use them as defaults.
DETECTOR_METADATA = {
    'v2.0.0':
        {'megadetector_version':'v2.0.0',
         'typical_detection_threshold':0.8,
         'conservative_detection_threshold':0.3},
    'v3.0.0':
        {'megadetector_version':'v3.0.0',
         'typical_detection_threshold':0.8,
         'conservative_detection_threshold':0.3},
    'v4.1.0':
        {'megadetector_version':'v4.1.0',
         'typical_detection_threshold':0.8,
         'conservative_detection_threshold':0.3},
    'v5a.0.0':
        {'megadetector_version':'v5a.0.0',
         'typical_detection_threshold':0.2,
         'conservative_detection_threshold':0.05},
    'v5b.0.0':
        {'megadetector_version':'v5b.0.0',
         'typical_detection_threshold':0.2,
         'conservative_detection_threshold':0.05}
}

DEFAULT_RENDERING_CONFIDENCE_THRESHOLD = DETECTOR_METADATA['v5b.0.0']['typical_detection_threshold']
DEFAULT_OUTPUT_CONFIDENCE_THRESHOLD = 0.005

DEFAULT_BOX_THICKNESS = 4
DEFAULT_BOX_EXPANSION = 0
    
#%% Utility functions

def convert_to_tf_coords(array):
    """From [x1, y1, width, height] to [y1, x1, y2, x2], where x1 is x_min, x2 is x_max

    This is only used to keep the interface of the synchronous API.
    """
    x1 = array[0]
    y1 = array[1]
    width = array[2]
    height = array[3]
    x2 = x1 + width
    y2 = y1 + height
    return [y1, x1, y2, x2]


def get_detector_metadata_from_version_string(detector_version):
    """
    Given a MegaDetector version string (e.g. "v4.1.0"), return the metadata for
    the model.  Used for writing standard defaults to batch output files.
    """
    if detector_version not in DETECTOR_METADATA:
        print('Warning: no metadata for unknown detector version {}'.format(detector_version))
        default_detector_metadata = {
            'megadetector_version':'unknown'
        }
        return default_detector_metadata
    else:
        return DETECTOR_METADATA[detector_version]


def get_detector_version_from_filename(detector_filename):
    """
    Get the version number component of the detector from the model filename.  
    
    *detector_filename* will almost always end with one of the following:
        
    megadetector_v2.pb
    megadetector_v3.pb
    megadetector_v4.1 (not produed by run_detector_batch.py, only found in Azure Batch API output files)
    md_v4.1.0.pb
    md_v5a.0.0.pt
    md_v5b.0.0.pt
    
    ...for which we identify the version number as "v2.0.0", "v3.0.0", "v4.1.0", 
    "v4.1.0", "v5a.0.0", and "v5b.0.0", respectively.
    """
    fn = os.path.basename(detector_filename)
    known_model_versions = {'v2':'v2.0.0',
                            'v3':'v3.0.0',
                            'v4.1':'v4.1.0',
                            'v5a.0.0':'v5a.0.0',
                            'v5b.0.0':'v5b.0.0'}
    matches = []
    for s in known_model_versions.keys():
        if s in fn:
            matches.append(s)
    if len(matches) == 0:
        print('Warning: could not determine MegaDetector version for model file {}'.format(detector_filename))
        return 'unknown'
    elif len(matches) > 1:
        print('Warning: multiple MegaDetector versions for model file {}'.format(detector_filename))
        return 'multiple'
    else:
        return known_model_versions[matches[0]]
    

def get_typical_confidence_threshold_from_results(results):
    """
    Given the .json data loaded from a MD results file, determine a typical confidence
    threshold based on the detector version.
    """
    if 'detector_metadata' in results['info'] and \
        'typical_detection_threshold' in results['info']['detector_metadata']:
        default_threshold = results['info']['detector_metadata']['typical_detection_threshold']
    elif ('detector' not in results['info']) or (results['info']['detector'] is None):
        print('Warning: detector version not available in results file, using MDv5 defaults')
        detector_metadata = get_detector_metadata_from_version_string('v5a.0.0')
        default_threshold = detector_metadata['typical_detection_threshold']
    else:
        print('Warning: detector metadata not available in results file, inferring from MD version')
        detector_filename = results['info']['detector']
        detector_version = get_detector_version_from_filename(detector_filename)
        detector_metadata = get_detector_metadata_from_version_string(detector_version)
        default_threshold = detector_metadata['typical_detection_threshold']

    return default_threshold    

    
def is_gpu_available(model_file):
    """Decide whether a GPU is available, importing PyTorch or TF depending on the extension
    of model_file.  Does not actually load model_file, just uses that to determine how to check 
    for GPU availability."""
    
    if model_file.endswith('.pb'):
        import tensorflow.compat.v1 as tf
        gpu_available = tf.test.is_gpu_available()
        print('TensorFlow version:', tf.__version__)
        print('tf.test.is_gpu_available:', gpu_available)                
        return gpu_available
    elif model_file.endswith('.pt'):
        import torch
        gpu_available = torch.cuda.is_available()
        print('PyTorch reports {} available CUDA devices'.format(torch.cuda.device_count()))
        if not gpu_available:
            try:
                # mps backend only available in torch >= 1.12.0
                if torch.backends.mps.is_built and torch.backends.mps.is_available():
                    gpu_available = True
                    print('PyTorch reports Metal Performance Shaders are available')
            except AttributeError:
                pass
        return gpu_available
    else:
        raise ValueError('Unrecognized model file extension for model {}'.format(model_file))


def load_detector(model_file, force_cpu=False):
    """Load a TF or PT detector, depending on the extension of model_file."""
    
    start_time = time.time()
    if model_file.endswith('.pb'):
        from tf_detector import TFDetector
        if force_cpu:
            raise ValueError('force_cpu option is not currently supported for TF detectors, ' + \
                             'use CUDA_VISIBLE_DEVICES=-1')
        detector = TFDetector(model_file)
    elif model_file.endswith('.pt'):
        from pytorch_detector import PTDetector
        detector = PTDetector(model_file, force_cpu, USE_MODEL_NATIVE_CLASSES)        
    else:
        raise ValueError('Unrecognized model format: {}'.format(model_file))
    elapsed = time.time() - start_time
    print('Loaded model in {}'.format(humanfriendly.format_timespan(elapsed)))
    return detector


#%% Main function

def load_and_run_detector(model_file, image_file_names, output_dir,
                          render_confidence_threshold=DEFAULT_RENDERING_CONFIDENCE_THRESHOLD,
                          crop_images=False, box_thickness=DEFAULT_BOX_THICKNESS, 
                          box_expansion=DEFAULT_BOX_EXPANSION, image_size=None
                          ):
    """Load and run detector on target images, and visualize the results."""
    
    if len(image_file_names) == 0:
        print('Warning: no files available')
        return

    print('GPU available: {}'.format(is_gpu_available(model_file)))
    
    detector = load_detector(model_file)

    detection_results = []
    time_load = []
    time_infer = []

    # Dictionary mapping output file names to a collision-avoidance count.
    #
    # Since we'll be writing a bunch of files to the same folder, we rename
    # as necessary to avoid collisions.
    output_filename_collision_counts = {}

    def input_file_to_detection_file(fn, crop_index=-1):
        """Creates unique file names for output files.

        This function does 3 things:
        1) If the --crop flag is used, then each input image may produce several output
            crops. For example, if foo.jpg has 3 detections, then this function should
            get called 3 times, with crop_index taking on 0, 1, then 2. Each time, this
            function appends crop_index to the filename, resulting in
                foo_crop00_detections.jpg
                foo_crop01_detections.jpg
                foo_crop02_detections.jpg

        2) If the --recursive flag is used, then the same file (base)name may appear
            multiple times. However, we output into a single flat folder. To avoid
            filename collisions, we prepend an integer prefix to duplicate filenames:
                foo_crop00_detections.jpg
                0000_foo_crop00_detections.jpg
                0001_foo_crop00_detections.jpg

        3) Prepends the output directory:
                out_dir/foo_crop00_detections.jpg

        Args:
            fn: str, filename
            crop_index: int, crop number

        Returns: output file path
        """
        fn = os.path.basename(fn).lower()
        name, ext = os.path.splitext(fn)
        if crop_index >= 0:
            name += '_crop{:0>2d}'.format(crop_index)
        fn = '{}{}{}'.format(name, image_utils.ImagePathUtils.DETECTION_FILENAME_INSERT, '.jpg')
        if fn in output_filename_collision_counts:
            n_collisions = output_filename_collision_counts[fn]
            fn = '{:0>4d}'.format(n_collisions) + '_' + fn
            output_filename_collision_counts[fn] += 1
        else:
            output_filename_collision_counts[fn] = 0
        fn = os.path.join(output_dir, fn)
        return fn

    # ...def input_file_to_detection_file()
    
    for im_file in tqdm(image_file_names):

        try:
            start_time = time.time()

            image = image_utils.load_image(im_file)

            elapsed = time.time() - start_time
            time_load.append(elapsed)

        except Exception as e:
            print('Image {} cannot be loaded. Exception: {}'.format(im_file, e))
            result = {
                'file': im_file,
                'failure': FAILURE_IMAGE_OPEN
            }
            detection_results.append(result)
            continue

        try:
            start_time = time.time()

            result = detector.generate_detections_one_image(image, im_file,
                       detection_threshold=DEFAULT_OUTPUT_CONFIDENCE_THRESHOLD,
                       image_size=image_size)
            detection_results.append(result)

            elapsed = time.time() - start_time
            time_infer.append(elapsed)

        except Exception as e:
            print('An error occurred while running the detector on image {}. Exception: {}'.format(im_file, e))
            continue

        try:
            if crop_images:

                images_cropped = image_utils.crop_image(result['detections'], image)

                for i_crop, cropped_image in enumerate(images_cropped):
                    output_full_path = input_file_to_detection_file(im_file, i_crop)
                    cropped_image.save(output_full_path)

            else:

                # Image is modified in place
                image_utils.render_detection_bounding_boxes(result['detections'], image,
                            label_map=DEFAULT_DETECTOR_LABEL_MAP,
                            confidence_threshold=render_confidence_threshold,
                            thickness=box_thickness, expansion=box_expansion)
                output_full_path = input_file_to_detection_file(im_file)
                image.save(output_full_path)

        except Exception as e:
            print('Visualizing results on the image {} failed. Exception: {}'.format(im_file, e))
            continue

    # ...for each image

    ave_time_load = statistics.mean(time_load)
    ave_time_infer = statistics.mean(time_infer)
    if len(time_load) > 1 and len(time_infer) > 1:
        std_dev_time_load = humanfriendly.format_timespan(statistics.stdev(time_load))
        std_dev_time_infer = humanfriendly.format_timespan(statistics.stdev(time_infer))
    else:
        std_dev_time_load = 'not available'
        std_dev_time_infer = 'not available'
    print('On average, for each image,')
    print('- loading took {}, std dev is {}'.format(humanfriendly.format_timespan(ave_time_load),
                                                    std_dev_time_load))
    print('- inference took {}, std dev is {}'.format(humanfriendly.format_timespan(ave_time_infer),
                                                      std_dev_time_infer))