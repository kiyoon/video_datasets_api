#!/usr/bin/env python3

import argparse

MODEL_DIR = '/media/kiyoon/Elements/EPIC_KITCHENS_2018/object_detection_model'
NOUN_LABEL_PATH = '/media/kiyoon/Elements/EPIC_KITCHENS_2018/annotations/EPIC_noun_classes.csv'
OBJECT_LABEL_PATH = '/media/kiyoon/Elements/EPIC_KITCHENS_2018/annotations/EPIC_train_object_labels.csv'

def get_parser():
    parser = argparse.ArgumentParser(description="Run object detection using a TensorFlow object detector api's model for the EPIC-Kitchens dataset. It can run on a directory containing images, or a single video file.",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--video-input", type=str, help="Path to video file.")
    parser.add_argument("--images-input-dir", type=str, help="A directory of input images with extension *.jpg. The file names should be the frame number (e.g. 00000000001.jpg)")
    parser.add_argument("--video-id-for-ground-truth", type=str, help="EPIC-Kitchens video id (e.g. P01_01) for searching ground truth data. If not specified, don't visualise ground truth. Only works when --images-input-dir is specified.")
    parser.add_argument("--model-dir", type=str, default=MODEL_DIR, help="Directory to the TensorFlow object detection model. The directory has to contain the 'frozen_inference_graph.pb' file.")
    parser.add_argument("--noun-label-path", type=str, default=NOUN_LABEL_PATH, help="Path to EPIC_noun_classes.csv")
    parser.add_argument("--object-label-path", type=str, default=OBJECT_LABEL_PATH, help="Path to EPIC_train_object_labels.csv")
    parser.add_argument(
        "--output",
        required=True,
        help="A file or directory to save output visualisations and prediction data."
    )

    parser.add_argument(
        "--confidence-threshold",
        type=float,
        default=0.5,
        help="Minimum score for instance predictions to be shown",
    )

    return parser

parser = get_parser()
args = get_parser().parse_args()

if args.video_input and args.images_input_dir:
    parser.error("--video-input and --images-input-dir can't come together.")

if not args.video_input and not args.images_input_dir:
    parser.error("Either --video-input or --images-input-dir has to be specified.")

if args.video_input and args.video_id_for_ground_truth:
    parser.error("--video-input and --video-id-for-ground-truth can't come together.")

import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile

from distutils.version import StrictVersion
from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image

# This is needed since the notebook is stored in the object_detection folder.
#sys.path.append("..")
from object_detection.utils import ops as utils_ops

if StrictVersion(tf.__version__) < StrictVersion('1.9.0'):
      raise ImportError('Please upgrade your TensorFlow installation to v1.9.* or later!')



import csv
import tqdm
import glob
from pprint import pprint
from epic_utils.epic_bounding_box_parser import EPIC_parse_object_bounding_box_labels
from epic_utils.epic_read_noun_labels import EPIC_read_noun_labels_to_category_index
import epic_utils.visualization_utils as vis_util

import pickle
import cv2




def RGB_frame_from_video(video):
    frame_num = 1
    while video.isOpened():
        success, frame = video.read()
        if success:
            yield frame_num, frame[:,:,::-1]
            frame_num += 1
        else:
            break


def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(
                      (im_height, im_width, 3)).astype(np.uint8)


'''
def run_inference_for_single_image(image, graph):
    with graph.as_default():#{{{
        with tf.Session() as sess:
            # Get handles to input and output tensors
            ops = tf.get_default_graph().get_operations()
            all_tensor_names = {output.name for op in ops for output in op.outputs}
            tensor_dict = {}
            for key in [
              'num_detections', 'detection_boxes', 'detection_scores',
              'detection_classes', 'detection_masks'
              ]:
                tensor_name = key + ':0'
                if tensor_name in all_tensor_names:
                    tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
                                        tensor_name)
            if 'detection_masks' in tensor_dict:
            # The following processing is only for single image
                detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
                detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
                # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
                real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
                detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
                detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
                detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
                        detection_masks, detection_boxes, image.shape[0], image.shape[1])
                detection_masks_reframed = tf.cast(
                        tf.greater(detection_masks_reframed, 0.5), tf.uint8)
                # Follow the convention by adding back the batch dimension
                tensor_dict['detection_masks'] = tf.expand_dims(
                        detection_masks_reframed, 0)
            image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

            # Run inference
            output_dict = sess.run(tensor_dict,
                      feed_dict={image_tensor: np.expand_dims(image, 0)})

            # all outputs are float32 numpy arrays, so convert types as appropriate
            output_dict['num_detections'] = int(output_dict['num_detections'][0])
            output_dict['detection_classes'] = output_dict[
                    'detection_classes'][0].astype(np.uint8)
            output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
            output_dict['detection_scores'] = output_dict['detection_scores'][0]
            if 'detection_masks' in output_dict:
                output_dict['detection_masks'] = output_dict['detection_masks'][0]
    return output_dict#}}}


def run_inference_for_multiple_images(images, graph):
    """Run inference using list of images (numpy arrays)#{{{

    Keyword arguments:
    images -- list of numpy arrays
    graph -- Frozen (pb) tensorflow graph (object detection model)
    """
    with graph.as_default():
        with tf.Session() as sess:
            # Get handles to input and output tensors
            ops = tf.get_default_graph().get_operations()
            all_tensor_names = {output.name for op in ops for output in op.outputs}
            tensor_dict = {}
            for key in [
              'num_detections', 'detection_boxes', 'detection_scores',
              'detection_classes', 'detection_masks'
              ]:
                tensor_name = key + ':0'
                if tensor_name in all_tensor_names:
                    tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
                                        tensor_name)
            if 'detection_masks' in tensor_dict:
            # The following processing is only for single image
                detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
                detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
                # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
                real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
                detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
                detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
                detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
                        detection_masks, detection_boxes, image.shape[0], image.shape[1])
                detection_masks_reframed = tf.cast(
                        tf.greater(detection_masks_reframed, 0.5), tf.uint8)
                # Follow the convention by adding back the batch dimension
                tensor_dict['detection_masks'] = tf.expand_dims(
                        detection_masks_reframed, 0)
            image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

            # Run inference
            output_list = []
            for image in images:
                output_dict = sess.run(tensor_dict,
                          feed_dict={image_tensor: np.expand_dims(image, 0)})

                # all outputs are float32 numpy arrays, so convert types as appropriate
                output_dict['num_detections'] = int(output_dict['num_detections'][0])
                output_dict['detection_classes'] = output_dict[
                        'detection_classes'][0].astype(np.uint8)
                output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
                output_dict['detection_scores'] = output_dict['detection_scores'][0]
                if 'detection_masks' in output_dict:
                    output_dict['detection_masks'] = output_dict['detection_masks'][0]

                output_list.append(output_dict)

    return output_list#}}}
'''


if __name__ == '__main__':
    path_to_frozen_graph = os.path.join(args.model_dir, 'frozen_inference_graph.pb')

    # Load a (frozen) Tensorflow model into memory.
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(path_to_frozen_graph, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
    #noun_labels = EPIC_read_noun_labels(LABEL_PATH)
    #print(noun_labels)

    category_index = EPIC_read_noun_labels_to_category_index(args.noun_label_path)

    all_detection_outputs = {}

    with detection_graph.as_default():
        with tf.Session() as sess:
            # Get handles to input and output tensors
            ops = tf.get_default_graph().get_operations()
            all_tensor_names = {output.name for op in ops for output in op.outputs}
            tensor_dict = {}
            for key in [
              'num_detections', 'detection_boxes', 'detection_scores',
              'detection_classes', 'detection_masks'
              ]:
                tensor_name = key + ':0'
                if tensor_name in all_tensor_names:
                    tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
                                        tensor_name)
            if 'detection_masks' in tensor_dict:
            # The following processing is only for single image
                detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
                detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
                # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
                real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
                detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
                detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
                detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
                        detection_masks, detection_boxes, image.shape[0], image.shape[1])
                detection_masks_reframed = tf.cast(
                        tf.greater(detection_masks_reframed, 0.5), tf.uint8)
                # Follow the convention by adding back the batch dimension
                tensor_dict['detection_masks'] = tf.expand_dims(
                        detection_masks_reframed, 0)
            image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

            if args.images_input_dir:
                os.makedirs(os.path.join(args.output, 'detection'), exist_ok=True)

                if args.video_id_for_ground_truth:
                    bounding_box_labels = EPIC_parse_object_bounding_box_labels(args.video_id_for_ground_truth, args.object_label_path, height_width_representation = False)
                    os.makedirs(os.path.join(args.output, 'ground_truth'), exist_ok=True)
                    os.makedirs(os.path.join(args.output, 'ground_truth_and_detection'), exist_ok=True)

                test_image_paths = glob.glob(os.path.join(args.images_input_dir, "*.jpg"))
                for image_path in tqdm.tqdm(test_image_paths):
                    image = Image.open(image_path)
                    # the array based representation of the image will be used later in order to prepare the
                    # result image with boxes and labels on it.
                    image_np = load_image_into_numpy_array(image)
                    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                    #image_np_expanded = np.expand_dims(image_np, axis=0)

                    # Run inference
                    output_dict = sess.run(tensor_dict,
                              feed_dict={image_tensor: np.expand_dims(image_np, 0)})

                    # all outputs are float32 numpy arrays, so convert types as appropriate
                    output_dict['num_detections'] = int(output_dict['num_detections'][0])
                    output_dict['detection_classes'] = output_dict[
                            'detection_classes'][0].astype(np.uint8)
                    output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
                    output_dict['detection_scores'] = output_dict['detection_scores'][0]
                    if 'detection_masks' in output_dict:
                        output_dict['detection_masks'] = output_dict['detection_masks'][0]

                    #pprint(output_dict)

                    image_groundtruth = image_np.copy()

                    vis_util.visualize_boxes_and_labels_on_image_array(
                      image_np,
                      output_dict['detection_boxes'],
                      output_dict['detection_classes'],
                      output_dict['detection_scores'],
                      category_index,
                      min_score_thresh=args.confidence_threshold,
                      instance_masks=output_dict.get('detection_masks'),
                      use_normalized_coordinates=True,
                      line_thickness=8)

                    image_basename = os.path.basename(image_path)
                    im = Image.fromarray(image_np)
                    im.save(os.path.join(args.output, 'detection/' + image_basename))

                    frame = int(os.path.splitext(image_basename)[0])
                    all_detection_outputs[frame] = output_dict
                    
                    if args.video_id_for_ground_truth:
                        if frame in bounding_box_labels.keys() and len(bounding_box_labels[frame]['classes']) > 0:
                            vis_util.visualize_boxes_and_labels_on_image_array(
                              image_groundtruth,
                              np.array(bounding_box_labels[frame]['boxes']),
                              np.array(bounding_box_labels[frame]['classes']),
                              np.ones(len(bounding_box_labels[frame]['classes'])),
                              category_index,
                              use_normalized_coordinates=False,
                              line_thickness=8)

                            im = Image.fromarray(image_groundtruth)
                            im.save(os.path.join(args.output, 'ground_truth/' + image_basename))

                        ## concatenate the ground truth and predictions
                        # Note that the ground truth can be empty (image without ground truth bounding boxes)
                        image_concat = np.vstack((image_groundtruth, image_np))
                        im = Image.fromarray(image_concat)
                        im.save(os.path.join(args.output, 'ground_truth_and_detection/' + image_basename))

                with open(os.path.join(args.output, "all_detection_outputs.pkl"), 'wb') as pfile:
                    pickle.dump(all_detection_outputs, pfile, protocol=pickle.HIGHEST_PROTOCOL)

            else:   # args.video_input
                os.makedirs(os.path.dirname(args.output), exist_ok=True)

                video = cv2.VideoCapture(args.video_input)
                width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
                frames_per_second = video.get(cv2.CAP_PROP_FPS)
                num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
                basename = os.path.basename(args.video_input)

                if os.path.isdir(args.output):
                    output_fname = os.path.join(args.output, basename)
                    #output_fname = os.path.splitext(output_fname)[0] + ".mkv"
                else:
                    output_fname = args.output
                assert not os.path.isfile(output_fname), output_fname
                output_file = cv2.VideoWriter(
                    filename=output_fname,
                    # some installation of opencv may not support x264 (due to its license),
                    # you can try other format (e.g. MPEG)
                    fourcc=cv2.VideoWriter_fourcc(*"x264"),
                    fps=float(frames_per_second),
                    frameSize=(width, height),
                    isColor=True,
                )

                assert os.path.isfile(args.video_input)
                for frame_num, image_frame in tqdm.tqdm(RGB_frame_from_video(video), total=num_frames):

                    # Run inference
                    output_dict = sess.run(tensor_dict,
                              feed_dict={image_tensor: np.expand_dims(image_frame, 0)})

                    # all outputs are float32 numpy arrays, so convert types as appropriate
                    output_dict['num_detections'] = int(output_dict['num_detections'][0])
                    output_dict['detection_classes'] = output_dict[
                            'detection_classes'][0].astype(np.uint8)
                    output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
                    output_dict['detection_scores'] = output_dict['detection_scores'][0]
                    if 'detection_masks' in output_dict:
                        output_dict['detection_masks'] = output_dict['detection_masks'][0]

                    #pprint(output_dict)

                    vis_util.visualize_boxes_and_labels_on_image_array(
                      image_frame,
                      output_dict['detection_boxes'],
                      output_dict['detection_classes'],
                      output_dict['detection_scores'],
                      category_index,
                      min_score_thresh=args.confidence_threshold,
                      instance_masks=output_dict.get('detection_masks'),
                      use_normalized_coordinates=True,
                      line_thickness=8)

                    output_file.write(image_frame[:,:,::-1])
                    all_detection_outputs[frame_num] = output_dict

                video.release()
                output_file.release()
                 
                with open(output_fname + '.pkl', 'wb') as pfile:
                    pickle.dump(all_detection_outputs, pfile, protocol=pickle.HIGHEST_PROTOCOL)
