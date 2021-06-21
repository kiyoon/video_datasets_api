import csv
import numpy as np

from .definitions import *
import os



SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))



def get_class_keys(classes_txt_path = os.path.join(SCRIPT_DIR, 'classes.txt')):
    """
    Returns:
        class keys (list of string)
    """
    labels = []
    with open(classes_txt_path) as f:
        labels = f.read().splitlines()

    assert len(labels) == NUM_CLASSES, "incorrect number of classes"

    return labels



if __name__ == "__main__":
    class_keys = get_class_keys()

    print(class_keys)

