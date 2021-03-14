import csv
import numpy as np

from .definitions import *

def labels_str2int(label_csv_path, class_indices = SOMETHINGV1_TEMPORAL_CLASSES_INDICES):
    labels = {}
    index = NUM_CLASSES_KINETICS_TEMPORAL
    with open(label_csv_path) as csvfile:
        reader = csv.reader(csvfile)
        for i, row in enumerate(reader):
            if i in class_indices:
                labels[''.join(row)] = index
                index += 1

    return labels



def read_splits(split_csv_path, labels_str2int):
    """
        Returns:
            Two numpy arrays. The first one is the video indices, and the second one is the labels in integer.
    """

    with open(split_csv_path) as csvfile:
        reader = csv.reader(csvfile, delimiter=';')

        uids = []
        labels = []

        for i, row in enumerate(reader):
            key = row[1].replace(',', '')
            if key in labels_str2int.keys():
                uids.append(int(row[0]))
                labels.append(labels_str2int[key])

    return np.array(uids, dtype=int), np.array(labels, dtype=int)


def get_class_keys(label_csv_path, class_indices = SOMETHINGV1_TEMPORAL_CLASSES_INDICES):
    """
    Returns:
        class keys (list of string)
    """
    labels = []
    with open(label_csv_path) as csvfile:
        reader = csv.reader(csvfile)
        for i, row in enumerate(reader):
            if i in class_indices:
                labels.append(''.join(row))

    return labels

def get_class_keys_shrinked(label_csv_path):
    """
    Returns:
        class keys, but "something" is replaced by "[]"
    """
    class_keys = get_class_keys(label_csv_path)
    for i, class_key in enumerate(class_keys):
        temp_class_key = class_key.replace("something", "[]")
        class_keys[i] = temp_class_key.replace("Something", "[]")
        
    return class_keys


if __name__ == "__main__":
    labels = labels_str2int('/home/kiyoon/datasets/something-something-v1/annotations/something-something-v1-labels.csv')
    train_uids, train_labels = read_splits('/home/kiyoon/datasets/something-something-v1/annotations/something-something-v1-train.csv', labels)

    print(train_uids)
    print(train_labels)

