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

def read_annotation(csv_path, labels):
    """
        Returns:
            Two numpy arrays. The first one is the video indices, and the second one is the labels in integer.
    """
    with open(csv_path) as csvfile:
        nb_samples = sum(1 for row in csv.reader(csvfile))
        assert nb_samples in [NB_TRAIN_SAMPLES, NB_VAL_SAMPLES, NB_TEST_SAMPLES], "The annotation file is not official or corrupted?"

    with open(csv_path) as csvfile:
        reader = csv.reader(csvfile, delimiter=';')

        X = np.zeros(nb_samples, dtype=int)
        Y = np.zeros(nb_samples, dtype=int)

        for i, row in enumerate(reader):
            X[i] = int(row[0])
            Y[i] = labels[row[1].replace(',', '')]

    return X, Y


if __name__ == "__main__":
    labels = labels_str2int('/home/kiyoon/datasets/something-something-v1/annotations/something-something-v1-labels.csv')
    X_train, Y_train = read_annotation('/home/kiyoon/datasets/something-something-v1/annotations/something-something-v1-train.csv', labels)

    print(X_train)
    print(Y_train)

