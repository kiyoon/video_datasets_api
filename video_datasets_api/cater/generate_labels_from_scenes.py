import json
from .class_keys import ACTION_CLASSES, ORDERING, _BEFORE, _AFTER, _DURING, class_keys_task2, class_keys_to_labels
from .definitions import NUM_CLASSES_TASK2

import os
from collections import OrderedDict
from itertools import permutations, product, combinations


def get_ordering(act1_time, act2_time):
    if act1_time[1] <= act2_time[0]:
        # act1 should finish before act2 starts
        return _BEFORE
    elif act2_time[1] <= act1_time[0]:
        # act1 should start after act2 ends
        return _AFTER
    else:
        # We define everything else as "during", though it might be partly
        # overlapped etc
        return _DURING

# From rohitgirdhar/CATER. For evaluation purposes, but extremely slow.
# DO NOT USE.
def satisfy_action_class(action_class, actions_set):#{{{
    action_class_ents, action_class_ord = action_class
    assert len(action_class_ents) == len(actions_set), \
        'Must be same number of actions'
    # The action set must contain the exact objects in exact motion
    for action_class_ent, action in zip(action_class_ents, actions_set):
        if (action_class_ent[0] != action[0] or
                action_class_ent[1] != action[1][0]):
            return False
    # Now need to make sure the intervals make sense w.r.t the relation
    for i in range(len(action_class_ord)):
        if not get_ordering(
                actions_set[i][1][2:],
                actions_set[i + 1][1][2:]) == action_class_ord[i]:
            return False
    return True


# slow version of `generate_task2_labels_from_scenes()`
def compute_active_labels(movements, objects, classes, n=2):
    name_to_type = {el['instance']: el['shape'] for el in objects}
    all_actions = []
    for name, motions in movements.items():
        for motion in motions:
            all_actions.append((
                name_to_type[name],
                motion))
    # Consider all n-length permutations of all_actions, and check if it
    # fits any of the classes
    this_lbl = set()
    for (cls_id, action_class), actions_set in product(
            enumerate(classes), permutations(all_actions, n)):
        if satisfy_action_class(action_class, actions_set):
            this_lbl.add(cls_id)
    return this_lbl#}}}
# END DO NOT USE.

class AllActions():
    def __init__(self, movements, objects):
        name_to_type = {el['instance']: el['shape'] for el in objects}
        self.all_actions = []        # _no_op filtered out
        for name, motions in movements.items():
            for motion in motions:
                if motion[0] != '_no_op':
                    self.all_actions.append(OneAction(
                        name,
                        name_to_type[name],
                        motion))

    def __iter__(self):
        return self.all_actions.__iter__()
    def __next__(self):
        return self.all_actions.__next__()
    def __len__(self):
        return self.all_actions.__len__()
    def __repr__(self):
        return self.all_actions.__repr__()
    def __str__(self):
        return self.all_actions.__str__()
    def __getitem__(self, index):
        return self.all_actions.__getitem__(index)
    def __setitem__(self, index, value):
        return self.all_actions.__setitem__(index, value)

    def sort(self):
        self.all_actions = sorted(self.all_actions, key=lambda x: x.start_time())

class OneAction():
    def __init__(self, name, obj_type, motion):
        self.action = (name, obj_type, motion)

    def start_time(self):
        return self.action[2][2]
    def end_time(self):
        return self.action[2][3]
    def time(self):
        return self.action[2][2:]
    def movement(self):
        return self.action[2][0]
    def instance(self):
        return self.action[0]
    def obj_type(self):
        return self.action[1]
    def containee(self):
        return self.action[2][1]

    def __repr__(self):
        return self.action.__repr__()
    def __str__(self):
        return self.action.__str__()


def generate_task2_labels_from_all_actions(all_actions, class_keys_to_labels_dict):

    def actions_pair_to_class_keys_only_before(actions_pair):
        order = get_ordering(actions_pair[0].time(), actions_pair[1].time())
        if order == _AFTER:
            class_key = f"{actions_pair[1].obj_type()}{actions_pair[1].movement()} before {actions_pair[0].obj_type()}{actions_pair[0].movement()}"
            return (actions_pair[1], actions_pair[0]), class_key
        elif order == _BEFORE:
            class_key = f"{actions_pair[0].obj_type()}{actions_pair[0].movement()} before {actions_pair[1].obj_type()}{actions_pair[1].movement()}"
            return actions_pair, class_key
        elif order == _DURING:
            class_key = f"{actions_pair[0].obj_type()}{actions_pair[0].movement()} during {actions_pair[1].obj_type()}{actions_pair[1].movement()}"
            return actions_pair, class_key
        else:
            raise NotImplementedError()

    labels = set()
    actions_in_charge = {}
    for actions_pair in combinations(all_actions, n):
        this_actions_pair, class_key = actions_pair_to_class_keys_only_before(actions_pair)
        label = class_keys_to_labels_dict[class_key]
        labels.add(label)
        if label not in actions_in_charge.keys():
            actions_in_charge[label] = []
        actions_in_charge[label].append(actions_pair)

    return labels, actions_in_charge


def generate_task2_labels_from_scenes(movements, objects, class_keys_to_labels_dict):
    """Faster version of `compute_active_labels()` but only works with task2 (len(classes) == 301 and n==2)
    It also returns the actual primitive action pairs that are in charge of the final labels.
    """

    n = 2
    all_actions = AllActions(movements, objects)
    return generate_task2_labels_from_all_actions(all_actions)



def main_single_scene(CATER_dir):
    import time

    scenes_dir = os.path.join(CATER_dir, 'max2action/scenes')
    scene_path = os.path.join(scenes_dir, 'CATER_new_000012.json')
    with open(scene_path, 'r', encoding='utf8') as scene_file:
        scene = json.load(scene_file, object_hook=OrderedDict)

    classes = class_keys_task2(string=False)

    # slow way
    start_time = time.time()
    labels = compute_active_labels(scene['movements'], scene['objects'], classes)
    elapsed_time = time.time() - start_time
    print(sorted(list(labels)))
    print(f'Elapsed time of the slow function from CATER: {elapsed_time}')

    # fast way
    class_keys_to_labels_dict = class_keys_to_labels(classes)
    start_time = time.time()
    labels, actions_in_charge = generate_task2_labels_from_scenes(scene['movements'], scene['objects'], class_keys_to_labels_dict)
    elapsed_time = time.time() - start_time
    labels = sorted(list(labels))
    print(labels)
    print(actions_in_charge[labels[0]])
    print(f'Elapsed time of the fast function from video_datasets_api: {elapsed_time}')


def main_all_scenes(CATER_dir):
    import time
    import tqdm

    scenes_dir = os.path.join(CATER_dir, 'max2action/scenes')
    lists_dir = os.path.join(CATER_dir, 'max2action/lists/actions_order_uniq')

    # read lists
    print("Reading lists..")
    labels_from_lists = {}
    with open(os.path.join(lists_dir, 'train.txt'), 'r') as split_file:
        for line in split_file.readlines():
            filename, labels = line.split(' ')
            basename, _ = os.path.splitext(filename)
            labels_list = list(map(int, labels.split(',')))
            labels_from_lists[basename] = labels_list
    with open(os.path.join(lists_dir, 'val.txt'), 'r') as split_file:
        for line in split_file.readlines():
            filename, labels = line.split(' ')
            basename, _ = os.path.splitext(filename)
            labels_list = list(map(int, labels.split(',')))
            labels_from_lists[basename] = labels_list

    classes = class_keys_task2(string=False)

    # read scenes
    print("Reading scenes..")
    scenes = {}
    for basename in labels_from_lists.keys():
        scene_path = os.path.join(scenes_dir, basename + '.json')
        with open(scene_path, 'r', encoding='utf8') as scene_file:
            scenes[basename] = json.load(scene_file, object_hook=OrderedDict)

    if False:
        # slow way
        print("Evaluating the slow function..")
        start_time = time.time()
        for basename, labels_lists in tqdm.tqdm(labels_from_lists.items()):
            scene = scenes[basename]
            labels_scenes = compute_active_labels(scene['movements'], scene['objects'], classes)
            assert set(labels_lists) == labels_scenes, f"Labels generated does not match with labels provided in `lists`. {labels_lists} and {sorted(list(labels_scenes))}"

        elapsed_time = time.time() - start_time
        print(f'Elapsed time of the slow function from CATER: {elapsed_time}')

    # fast way
    print("Evaluating the fast function..")
    class_keys_to_labels_dict = class_keys_to_labels(classes)
    start_time = time.time()
    for basename, labels_lists in tqdm.tqdm(labels_from_lists.items()):
        scene = scenes[basename]
        labels_scenes, actions_in_charge = generate_task2_labels_from_scenes(scene['movements'], scene['objects'], class_keys_to_labels_dict)
        assert set(labels_lists) == labels_scenes, f"Labels generated does not match with labels provided in `lists`. {labels_lists} and {sorted(list(labels_scenes))}"

    elapsed_time = time.time() - start_time
    print(f'Elapsed time of the fast function from video_datasets_api: {elapsed_time}')

if __name__ == '__main__':
    CATER_dir = '/home/kiyoon/datasets/CATER'
    #main_single_scene(CATER_dir)
    main_all_scenes(CATER_dir)
