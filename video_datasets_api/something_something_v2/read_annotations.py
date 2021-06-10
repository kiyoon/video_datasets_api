import json
import numpy as np

from .definitions import *
import logging

logger = logging.getLogger(__name__)

def add_brackets_to_class_key(class_key: str) -> str:
    for something_variation in something_variations:
        class_key = class_key.replace(something_variation, f'[{something_variation}]')
    return class_key.replace(' something', ' [something]').replace('Something', '[Something]')
def replace_sth_to_brackets(class_key: str) -> str:
    for something_variation in something_variations:
        class_key = class_key.replace(something_variation, '[]')
    return class_key.replace(' something', ' []').replace('Something', '[]')

def class_keys_to_int_label(label_json_path):
    with open(label_json_path) as jsonfile:
        data = json.load(jsonfile)

    labels = {}
    # convert class keys to have brackets 
    # convert to int
    for key, value in data.items():
        labels[add_brackets_to_class_key(key)] = int(value)

    return labels


def read_splits(split_json_path, class_keys_to_int, no_labels=False):
    """
        Returns:
            Two numpy arrays. The first one is the video indices, and the second one is the labels in integer.
    """
    with open(split_json_path) as jsonfile:
        data = json.load(jsonfile)

    num_samples = len(data)
    if num_samples not in [NB_TRAIN_SAMPLES, NB_VAL_SAMPLES, NB_TEST_SAMPLES]:
        logger.warning(f'Something-Something-V2 dataset loaded with different number of samples. Official split has: {NB_TRAIN_SAMPLES}, {NB_VAL_SAMPLES}, {NB_TEST_SAMPLES}. Got {num_samples}')

    uids = np.zeros(num_samples, dtype=int)
    if not no_labels:
        labels = np.zeros(num_samples, dtype=int)

    for i, sample in enumerate(data):
        uids[i] = int(sample['id'])
        if not no_labels:
            labels[i] = class_keys_to_int[sample['template']]

    if not no_labels:
        return uids, labels 
    else:
        return uids


def get_class_keys(label_json_path):
    """
    Returns:
        class keys (list of string)
    """
    with open(label_json_path) as jsonfile:
        data = json.load(jsonfile)

    labels = []
    # convert class keys to have brackets 
    for i, (key, value) in enumerate(data.items()):
        assert i == int(value), "Wrong format"
        labels.append(add_brackets_to_class_key(key))

    return labels

def get_class_keys_shrinked(label_csv_path):
    """
    Returns:
        class keys, but "something" is replaced by "[]"
    """
    with open(label_json_path) as jsonfile:
        data = json.load(jsonfile)

    labels = []
    # convert class keys to have brackets 
    for i, (key, value) in enumerate(data.items()):
        assert i == int(value), "Wrong format"
        labels.append(replace_sth_to_brackets(key))

    return labels


if __name__ == "__main__":
    class_keys_to_int = class_keys_to_int_label('/home/kiyoon/project/PyVideoAI/submodules/video_datasets_api/video_datasets_api/something_something_v2/something-something-v2-labels.json')
    train_uids, train_labels = read_splits('something-something-v2-test.json', class_keys_to_int)

    print(train_uids)
    print(train_labels)

