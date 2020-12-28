import csv
import numpy as np

from .definitions import *

def labels_str2int(label_csv_path):
    labels = {}
    with open(label_csv_path) as csvfile:
        reader = csv.reader(csvfile)
        for i, row in enumerate(reader):
            labels[''.join(row)] = i

    return labels



def labels_str2int_sorted(label_csv_path):
    with open(label_csv_path) as f:
        lines = f.readlines()
    categories = []
    for line in lines:
        line = line.rstrip()
        categories.append(line)
    categories = sorted(categories)

    dict_categories = {}
    for i, category in enumerate(categories):
        dict_categories[category.replace(',', '')] = i

    return dict_categories


def read_splits(split_csv_path, labels_str2int):
    """
        Returns:
            Two numpy arrays. The first one is the video indices, and the second one is the labels in integer.
    """
    with open(split_csv_path) as csvfile:
        nb_samples = sum(1 for row in csv.reader(csvfile))
        assert nb_samples in [NB_TRAIN_SAMPLES, NB_VAL_SAMPLES, NB_TEST_SAMPLES], "The annotation file is not official or corrupted?"

    with open(split_csv_path) as csvfile:
        reader = csv.reader(csvfile, delimiter=';')

        uids = np.zeros(nb_samples, dtype=int)
        labels = np.zeros(nb_samples, dtype=int)

        for i, row in enumerate(reader):
            uids[i] = int(row[0])
            labels[i] = labels_str2int[row[1].replace(',', '')]

    return uids, labels 


def get_class_keys(label_csv_path):
    """
    Returns:
        class keys (list of string)
    """
    labels = []
    with open(label_csv_path) as csvfile:
        reader = csv.reader(csvfile)
        for i, row in enumerate(reader):
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

