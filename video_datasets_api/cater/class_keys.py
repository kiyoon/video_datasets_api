# Run with caffe2_Nov_2018 conda env

#import glob
#import os.path as osp
#import json
#from gen_utils import mkdir_p
#import numpy as np
#from tqdm import tqdm
#import logging
#import subprocess
#from functools import partial
#import re
#import cPickle as pkl
#from collections import defaultdict, OrderedDict
from itertools import permutations, product
#import multiprocessing as mp
#import math
#import copy

ACTION_CLASSES = [
    # object, movement
    ('sphere', '_slide'),
    ('sphere', '_pick_place'),
    ('spl', '_slide'),
    ('spl', '_pick_place'),
    ('spl', '_rotate'),
    ('cylinder', '_pick_place'),
    ('cylinder', '_slide'),
    ('cylinder', '_rotate'),
    ('cube', '_slide'),
    ('cube', '_pick_place'),
    ('cube', '_rotate'),
    ('cone', '_contain'),
    ('cone', '_pick_place'),
    ('cone', '_slide'),
]
_BEFORE = 'before'
_AFTER = 'after'
_DURING = 'during'
ORDERING = [
    _BEFORE,
    _DURING,
    _AFTER,
]




def action_order_unique(classes):
    def reverse(el):
        if el == ('during',):
            return el
        elif el == ('before',):
            return ('after',)
        elif el == ('after',):
            return ('before',)
        else:
            raise ValueError('This should not happen')
    classes_uniq = []
    for el in classes:
        if el not in classes_uniq and ((el[0][1], el[0][0]), reverse(el[1])) not in classes_uniq:
            classes_uniq.append(el)
    return classes_uniq


def class_keys_task1(string=True):
    classes = ACTION_CLASSES

    if string:
        classes = [x[0] + x[1] for x in classes]
        return classes

    else:
        return classes


def class_keys_task2(n=2, unique=True, string=True):
    action_sets = list(product(ACTION_CLASSES, repeat=n))
    # all orderings
    orderings = list(product(ORDERING, repeat=(n-1)))
    # all actions and orderings
    classes = list(product(action_sets, orderings))
    if unique:
        # Remove classes such as "X before Y" when "Y after X" already exists in the data
        classes = action_order_unique(classes)

    if string:
        classes = [x[0][0][0] + x[0][0][1] + ' ' + x[1][0] + ' ' + x[0][1][0] + x[0][1][1] for x in classes]
        return classes

    else:
        return classes


def main():
    print(class_keys_task1())
    print(class_keys_task2())



if __name__ == '__main__':
    main()
