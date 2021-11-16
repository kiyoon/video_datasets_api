#!/usr/bin/env python3

OBJECT_LABEL_PATH = '/media/kiyoon/Elements/EPIC_KITCHENS_2018/annotations/EPIC_train_object_labels.csv'
INPUT_DIR = '/media/kiyoon/Elements/experiments/EPIC-Kitchens/object_detection/coco_frcnn_0.1_images'

TRAIN_VIDEO_IDS = ['P01_01','P01_02','P01_03','P01_04','P01_05','P01_06','P01_07','P01_08','P01_09','P01_10','P01_16','P01_17','P01_18','P01_19','P02_01','P02_02','P02_03','P02_04','P02_05','P02_06','P02_07','P02_08','P02_09','P02_10','P02_11','P03_02','P03_03','P03_04','P03_05','P03_06','P03_07','P03_08','P03_09','P03_10','P03_11','P03_12','P03_13','P03_14','P03_15','P03_16','P03_17','P03_18','P03_19','P03_20','P03_27','P03_28','P04_01','P04_02','P04_03','P04_04','P04_05','P04_06','P04_07','P04_08','P04_09','P04_10','P04_11','P04_12','P04_13','P04_14','P04_15','P04_16','P04_17','P04_18','P04_19','P04_20','P04_21','P04_22','P04_23','P05_01','P05_02','P05_03','P05_04','P05_05','P05_06','P05_08','P06_01','P06_02','P06_03','P06_05','P06_07','P06_08','P06_09','P07_01','P07_02','P07_03','P07_04','P07_05','P07_06','P07_07','P07_08','P07_09','P07_10','P07_11','P08_01','P08_02','P08_03','P08_04','P08_05','P08_06','P08_07','P08_08','P08_11','P08_12','P08_13','P08_18','P08_19','P08_20','P08_21','P08_22','P08_23','P08_24','P08_25','P08_26','P08_27','P08_28','P10_01','P10_02','P10_04','P12_01','P12_02','P12_04','P12_05','P12_06','P12_07','P13_04','P13_05','P13_06','P13_07','P13_08','P13_09','P13_10','P14_01','P14_02','P14_03','P14_04','P14_05','P14_07','P14_09','P15_01','P15_02','P15_03','P15_07','P15_08','P15_09','P15_10','P15_11','P15_12','P15_13','P16_01','P16_02','P16_03','P17_01','P17_03','P17_04','P19_01','P19_02','P19_03','P19_04','P20_01','P20_02','P20_03','P20_04','P21_01','P21_03','P21_04','P22_05','P22_06','P22_07','P22_08','P22_09','P22_10','P22_11','P22_12','P22_13','P22_14','P22_15','P22_16','P22_17','P23_01','P23_02','P23_03','P23_04','P24_01','P24_02','P24_03','P24_04','P24_05','P24_06','P24_07','P24_08','P25_01','P25_02','P25_03','P25_04','P25_05','P25_09','P25_10','P25_11','P25_12','P26_01','P26_02','P26_03','P26_04','P26_05','P26_06','P26_07','P26_08','P26_09','P26_10','P26_11','P26_12','P26_13','P26_14','P26_15','P26_16','P26_17','P26_18','P26_19','P26_20','P26_21','P26_22','P26_23','P26_24','P26_25','P26_26','P26_27','P26_28','P26_29','P27_01','P27_02','P27_03','P27_04','P27_06','P27_07','P28_01','P28_02','P28_03','P28_04','P28_05','P28_06','P28_07','P28_08','P28_09','P28_10','P28_11','P28_12','P28_13','P28_14','P29_01','P29_02','P29_03','P29_04','P30_01','P30_02','P30_03','P30_04','P30_05','P30_06','P30_10','P30_11','P31_01','P31_02','P31_03','P31_04','P31_05','P31_06','P31_07','P31_08','P31_09','P31_13','P31_14']

import argparse

def get_parser():
    parser = argparse.ArgumentParser(description="Calculate average IOU per ground truth using Detectron2 predictions",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--input-dir", type=str, default=INPUT_DIR, help="A directory used for storing output results. Must contain directories of participant ids (e.g. P01, P02, P03)")
    parser.add_argument("--object-label-path", type=str, default=OBJECT_LABEL_PATH, help="Path to EPIC_train_object_labels.csv")
    parser.add_argument("--visualise", action='store_true', help="visualise the boxes")

    return parser

parser = get_parser()
args = get_parser().parse_args()

import time
import tqdm
import numpy as np
import os
import sys
import pickle
from epic_utils.epic_bounding_box_parser import EPIC_parse_object_bounding_box_labels
import epic_utils.visualization_utils as vis_util
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('tkagg')

def np_vec_no_jit_iou(bboxes1, bboxes2):
    x11, y11, x12, y12 = np.split(bboxes1, 4, axis=1)
    x21, y21, x22, y22 = np.split(bboxes2, 4, axis=1)
    xA = np.maximum(x11, np.transpose(x21))
    yA = np.maximum(y11, np.transpose(y21))
    xB = np.minimum(x12, np.transpose(x22))
    yB = np.minimum(y12, np.transpose(y22))
    interArea = np.maximum((xB - xA + 1), 0) * np.maximum((yB - yA + 1), 0)
    boxAArea = (x12 - x11 + 1) * (y12 - y11 + 1)
    boxBArea = (x22 - x21 + 1) * (y22 - y21 + 1)
    iou = interArea / (boxAArea + np.transpose(boxBArea) - interArea)
    return iou

for train_video_id in tqdm.tqdm(TRAIN_VIDEO_IDS):
    participant_id = train_video_id[:3]

    bounding_box_labels = EPIC_parse_object_bounding_box_labels(train_video_id, args.object_label_path, height_width_representation = False)
    with open(os.path.join(args.input_dir, '%s/%s/all_detection_outputs.pkl' % (participant_id, train_video_id)), 'rb') as f:
        all_detection_outputs = pickle.load(f)


    ious = []

    for frame_num in bounding_box_labels.keys():
        ground_truth_boxes = np.array(bounding_box_labels[frame_num]['boxes'])
        if not len(ground_truth_boxes):
            continue

        detection_boxes = all_detection_outputs[frame_num]['detection_boxes']
        # XYXY to YXYX
        detection_boxes[:, [0,1]] = detection_boxes[:, [1,0]]
        detection_boxes[:, [2,3]] = detection_boxes[:, [3,2]]

        if not len(detection_boxes):
            ious.extend([0.] * len(ground_truth_boxes))
            continue

        iou = np_vec_no_jit_iou(ground_truth_boxes, detection_boxes)

        '''
        if iou.max(axis=1).max() > 0.5:
            print(frame_num)
            print(ground_truth_boxes)
            print(detection_boxes)
            print(iou)
            print(iou.max(axis=1))
        '''

        if args.visualise:
            print(ground_truth_boxes)
            print(detection_boxes)
            amax = iou.argmax(axis=1)
            print(iou.max(axis=1))
            print(amax)
            print(detection_boxes[amax])
            #time.sleep(5)

            detection_vis = np.ones((1080,1920,3), dtype=int) * 255
            vis_util.visualize_boxes_and_labels_on_image_array(
              detection_vis,
              detection_boxes,
              None,
              None,
              None,
              min_score_thresh=0.1,
              use_normalized_coordinates=False,
              line_thickness=8)

            plt.imshow(detection_vis)
            plt.show()

            ground_truth_vis = np.ones((1080,1920,3), dtype=int) * 255
            vis_util.visualize_boxes_and_labels_on_image_array(
              ground_truth_vis,
              ground_truth_boxes,
              None,
              None,
              None,
              min_score_thresh=0.1,
              use_normalized_coordinates=False,
              line_thickness=8)

            plt.imshow(ground_truth_vis)
            plt.show()

            selected_detection_vis = np.ones((1080,1920,3), dtype=int) * 255
            vis_util.visualize_boxes_and_labels_on_image_array(
              selected_detection_vis,
              detection_boxes[amax],
              None,
              None,
              None,
              min_score_thresh=0.1,
              use_normalized_coordinates=False,
              line_thickness=8)

            plt.imshow(selected_detection_vis)
            plt.show()
        
        ious.extend(iou.max(axis=1))

print(sum(ious) / len(ious))

    

