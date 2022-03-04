#!/usr/bin/env python3

import tarfile
import tqdm
import pickle
import os

import argparse
def get_parser():
    parser = argparse.ArgumentParser(description="From the extracted optical flow directory, hard-link copy only the ones used in action recognition to another folder. You MUST run epic_convert_rgb_to_flow_frame_idxs.py before running this.",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("flow_dir", help="Path to the directory with flow files. (EPIC-100 extensions directory)")
    parser.add_argument("output_dir", help="Directory to save train.csv and val.csv")
    parser.add_argument("annotations_root_dir", type=str, help="Path to annotations root dir.")

    return parser

parser = get_parser()
args = parser.parse_args()

if __name__ == '__main__':
    os.makedirs(args.output_dir, exist_ok=True)

    used_frames = {}
    print("Getting frame information from annotations..")
    for split in ['train', 'validation']:
        label_path = os.path.join(args.annotations_root_dir, f'EPIC_100_{split}_flow.pkl')
        if not os.path.isfile(label_path):
            raise FileNotFoundError(f'{label_path} not available. Did you forget to run epic_convert_rgb_to_flow_frame_idxs.py?')
            
        with open(label_path, 'rb') as f:
            epic_action_labels = pickle.load(f)

        num_videos = len(epic_action_labels.index)
        for index in range(num_videos):
            narration_id = epic_action_labels.index[index]

            participant_id = epic_action_labels.participant_id.iloc[index]
            epicvideo_id = epic_action_labels.video_id.iloc[index]
            start_frame = epic_action_labels.start_frame.iloc[index]
            stop_frame = epic_action_labels.stop_frame.iloc[index]

            dir_path = os.path.join(args.epic100_dir, narration_id)
            
            if epicvideo_id in used_frames.keys():
                used_frames[epicvideo_id].extend(range(start_frame, stop_frame+1))
            else:
                used_frames[epicvideo_id] = list(range(start_frame, stop_frame+1))

    print("Creating another directory with only action recognition files..")
    for epicvideo_id, frames in tqdm.tqdm(used_frames.items()):
        participant_id = epicvideo_id[:3]


        flow_dirs = ['u', 'v']
        files_to_keep = [f'frame_{frame:010d}.jpg' for frame in frames]
        for flow_dir in flow_dirs:
            input_dir = os.path.join(args.flow_dir, participant_id, epicvideo_id, flow_dir)
            output_dir = os.path.join(args.output_dir, participant_id, epicvideo_id, flow_dir)
            os.makedirs(output_dir)
            for file_to_keep in files_to_keep:
                os.link(os.path.join(input_dir, file_to_keep), os.path.join(output_dir, file_to_keep))

