import numpy as np
import json


def read_splits(split_json_path):
    """
        Returns:
            Two numpy arrays. The first one is the video indices, and the second one is the labels in integer.
    """
    with open(split_json_path) as jsonfile:
        data = json.load(jsonfile)
        nb_samples = len(data)

    vid_names = [''] * nb_samples
    uids = np.zeros(nb_samples, dtype=int)
    labels = np.zeros(nb_samples, dtype=int)
    num_frames = np.zeros(nb_samples, dtype=int)

    for i, sample in enumerate(data):
        assert sample['start_frame'] == 0

        vid_names[i] = sample['vid_name']
        labels[i] = sample['label']
        num_frames[i] = sample['end_frame'] + 1

    return vid_names, labels, num_frames


def get_class_keys(vocab_json_path):
    """
    Returns:
        class keys (list of string)
    """
    labels = []
    with open(vocab_json_path) as jsonfile:
        data = json.load(jsonfile)
        for label in data:
            labels.append('-'.join(label))

    return labels


if __name__ == "__main__":
    class_keys = get_class_keys('/disk/scratch1/common_datasets/diving48/annotations/Diving48_vocab.json')
    print(class_keys)
    vid_names, labels, num_frames = read_splits('/disk/scratch1/common_datasets/diving48/annotations/Diving48_V2_train.json')
    print(labels)
