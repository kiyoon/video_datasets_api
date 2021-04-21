# CATER videos are 301 frames long with ~10 time slots per video.
# This code allows to trim the video and return e.g. 2-slot video,
# without cutting when actions are active, nor when containment has been done previously.

import json
import pickle
import os
import copy
from collections import OrderedDict
from .generate_labels_from_scenes import AllActions
import tqdm

def generate_task2_dataset_cut_two_time_slots(scenes_dir, video_ids, mode='containment_only'):
    cut_dataset = []
    for video_id in tqdm.tqdm(video_ids):
        scene_path = os.path.join(scenes_dir, f'CATER_new_{video_id:06d}.json')

        with open(scene_path, 'r', encoding='utf8') as scene_file:
            scene = json.load(scene_file, object_hook=OrderedDict)

        movements = scene['movements']
        objects = scene['objects']

        all_actions = AllActions(movements, objects)
        time_slots = get_time_slots(all_actions)

        cut_dataset.extend(cut_video_into_two_time_slots(video_id, time_slots, mode))
    return cut_dataset

def cut_video_into_two_time_slots(video_id, time_slots, mode='containment_only'):
    '''
    params:
        mode (str): containment_only, never_containment, all
    '''
    assert mode in ['containment_only', 'never_containment', 'all'], f'Unknown mode: {mode}'

    cut_dataset = []

    def two_time_slots_to_one_slice(video_id, time_slot1, time_slot2):
        return {'video_id': video_id,
                'start': time_slot1['start'],
                'end': time_slot2['end'],
                'actions': time_slot1['actions'] + time_slot2['actions'],
                }

    for i in range(len(time_slots)-1):
        # check time_slots[i] and time_slots[i+1] to see if you can include that to the dataset.
        if time_slots[i]['num_containments'] == 0:
            # containment doesn't happen or happens at the second time slot.
            # We consider it as no containment
            if mode != 'containment_only':
                cut_dataset.append(two_time_slots_to_one_slice(video_id, time_slots[i], time_slots[i+1]))
                continue

        elif time_slots[i]['num_containments'] > 0:
            # check if containment is happening now.
            if i == 0 or (time_slots[i-1]['num_containments'] == 0):
                # either it's the first time slot,
                # or previous time slot didn't have any containment.
                # Meaning, containment happening at i-th time slot now.
                if mode != 'never_containment':
                    cut_dataset.append(two_time_slots_to_one_slice(video_id, time_slots[i], time_slots[i+1]))
                    continue

    return cut_dataset


def get_time_slots(all_actions: AllActions):
    all_actions = copy.deepcopy(all_actions)
    all_actions.sort()
    time_slots = []
    containers = set()

    # initialise with the first element
    if len(all_actions) > 0:
        action = all_actions[0]
        actions_in_time_slot = [action]
        if action.movement() == '_contain':
            containers.add(action.instance())
        time_slot_start = action.start_time()
        time_slot_end = action.end_time()
        

    # iterate
    if len(all_actions) > 1:
        for action in all_actions[1:]:
            if action.start_time() >= time_slot_end:
                # finalise old time slot
                time_slots.append({'start': time_slot_start, 'end': time_slot_end, 'num_containments': len(containers), 'actions': actions_in_time_slot})
                # new time slot
                actions_in_time_slot = [action]
                time_slot_start = action.start_time()
                time_slot_end = action.end_time()
            else:
                # add to existing slot
                actions_in_time_slot.append(action)
                #time_slot_start = min(time_slot_start, action.start_time())     # no need to do, as it's sorted
                time_slot_end = max(time_slot_end, action.start_time())

            if action.movement() == '_contain':
                containers.add(action.instance())
            elif action.movement() == '_pick_place':
                containers.discard(action.instance())    # if the instance is a container, it's not anymore.
                                                        # if it isn't a container, no change nor error

    # finalise
    if len(all_actions) > 0:
        time_slots.append({'start': time_slot_start, 'end': time_slot_end, 'num_containments': len(containers), 'actions': actions_in_time_slot})

    return time_slots
    

def main_cut_one_video():
    CATER_dir = '/home/kiyoon/datasets/CATER'
    scenes_dir = os.path.join(CATER_dir, 'max2action/scenes')
    video_id = 12
    scene_path = os.path.join(scenes_dir, 'CATER_new_{video_id:06d}.json')

    with open(scene_path, 'r', encoding='utf8') as scene_file:
        scene = json.load(scene_file, object_hook=OrderedDict)

    movements = scene['movements']
    objects = scene['objects']

    all_actions = AllActions(movements, objects)
    time_slots = get_time_slots(all_actions)
    print(time_slots)

    cut_dataset = cut_video_into_two_time_slots(video_id, time_slots, 'containment_only')
    print(cut_dataset)
    cut_dataset = cut_video_into_two_time_slots(video_id, time_slots, 'never_containment')
    print(cut_dataset)
    cut_dataset = cut_video_into_two_time_slots(video_id, time_slots, 'all')
    print(cut_dataset)

def main_generate_cut_dataset():
    video_ids = {}
    from .trainval_splits.max2action.actions_order_uniq.train import video_ids as train_video_ids
    from .trainval_splits.max2action.actions_order_uniq.val import video_ids as val_video_ids
    video_ids['max2action'] = {'train': train_video_ids, 'val': val_video_ids}

    from .trainval_splits.max2action_cameramotion.actions_order_uniq.train import video_ids as train_video_ids
    from .trainval_splits.max2action_cameramotion.actions_order_uniq.val import video_ids as val_video_ids
    video_ids['max2action_cameramotion'] = {'train': train_video_ids, 'val': val_video_ids}

    CATER_dir = '/home/kiyoon/datasets/CATER'
    output_CATER_dir = '/home/kiyoon/datasets/CATER'

    CATER_modes = ['max2action', 'max2action_cameramotion']
    modes = ['containment_only', 'never_containment', 'all']
    for cater_mode in CATER_modes:
        scenes_dir = os.path.join(CATER_dir, cater_mode, 'scenes')
        for mode in modes:
            output_dir = os.path.join(output_CATER_dir, cater_mode, 'twoslot_dataset_splits', mode)
            os.makedirs(output_dir, exist_ok=True)

            for trainval_mode in ['train', 'val']:
                cut_dataset = generate_task2_dataset_cut_two_time_slots(scenes_dir, video_ids[cater_mode][trainval_mode], mode)
                with open(os.path.join(output_dir, f'{trainval_mode}.pkl'), 'wb') as f:
                    pickle.dump(cut_dataset, f, pickle.HIGHEST_PROTOCOL)
    

if __name__ == '__main__':
    #main_cut_one_video()
    main_generate_cut_dataset()
