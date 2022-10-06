from __future__ import annotations
from dataclasses import dataclass, asdict
from functools import lru_cache
from types import MappingProxyType  # immutable dict

import pickle
import os
from ..beoid.read_annotations import read_all_annotations as beoid_read_all_annotations
from ..beoid.read_annotations import BEOIDClipLabel
from .class_keys import read_class_keys
#from video_datasets_api.beoid.read_annotations import read_all_annotations
#from video_datasets_api.wray_multiverb.class_keys import read_class_keys


# 23 verb classes
# Use class_filter_indices() to get filtering indices from the Wray labels.
Wray_verb_class_keys_filtered = ('move', 'open', 'pull-out', 'plug', 'insert', 'press', 'pull', 'rotate', 'scan', 'switch-on', 'fill', 'hold-down', 'scoop', 'take', 'stir', 'pick-up', 'put', 'pour', 'turn', 'let-go', 'place', 'push', 'rinse')
NUM_CLASSES_FILTERED = len(Wray_verb_class_keys_filtered)

# 90 verb classes
Wray_verb_class_keys = ('divide', 'point', 'wash-up', 'move', 'set-up', 'replace', 'wash', 'hold-on', 'shake', 'touch', 'open', 'find', 'cut', 'pull-out', 'transfer', 'swipe', 'start', 'spread', 'fumble', 'crack', 'input', 'kick', 'grip', 'plug', 'distribute', 'return', 'insert', 'put-down', 'spoon', 'lift', 'press', 'hold', 'pull', 'rotate', 'flip', 'remove', 'untangle', 'slide', 'adjust', 'grasp', 'grab', 'activate', 'tap', 'scan', 'twist', 'carry', 'unlock', 'switch-on', 'pull-up', 'close', 'check', 'examine', 'fill', 'screw', 'hold-down', 'turn-on', 'scoop', 'squeeze', 'relax', 'tip', 'turn-off', 'mix', 'take', 'swirl', 'plug-in', 'weaken', 'stir', 'step-on', 'pick-up', 'peel', 'compress', 'reach', 'release', 'spray', 'press-down', 'put', 'pedal', 'pour', 'dry', 'drain', 'fill-up', 'drive', 'turn', 'switch', 'let-go', 'place', 'clean', 'push', 'position', 'rinse')

# Classes that have samples in BEOID when the softlabels are thresholded with 0.5
# 42 verb classes
# This may NOT include the original BEOID verb labels.
classes_exist = [False, False, False,  True, False, False,  True, False, False,
        True,  True, False, False,  True, False, False, False, False,
       False, False, False, False, False,  True, False, False,  True,
        True, False,  True,  True,  True,  True,  True, False,  True,
       False,  True,  True, False, False, False, False,  True,  True,
        True, False,  True, False,  True, False, False,  True, False,
       False,  True,  True, False, False, False,  True,  True,  True,
        True,  True, False,  True, False,  True, False, False, False,
        True, False,  True,  True,  True, False, False, False,  True,
       False,  True,  True, False,  True,  True,  True, False,  True]
Wray_verb_class_keys_thresholded = tuple(class_key for class_key, class_exist in zip(Wray_verb_class_keys, classes_exist) if class_exist)
NUM_CLASSES_THRESHOLDED = len(Wray_verb_class_keys_thresholded)     # 42


# Verb, noun spaces are replaced to -
# Noun separator is +
Wray_class_key_to_BEOID_class_keys = MappingProxyType({
    'fill_cup': ['fill_cup', 'fill_cup+tap'],
    'hold-down_button': ['hold-down_button'],
    'insert_foot': ['insert_foot+pedal', 'insert_pedal'],
    'insert_screwdriver+wire': ['insert_wire+screwdriver'],
    'insert_weight-pin': ['insert_weight-pin'],
    'let-go_rowing-machine': ['let-go_rowing-machine'],
    'move_rest': ['move_rest'],
    'move_seat': ['move_seat'],
    'open_door': ['open_door'],
    'open_jar': ['open_jar'],
    'pick-up_cup': ['pick-up_mug', 'pick-up_cup'],
    'pick-up_jar': ['pick-up_jar'],
    'pick-up_plug': ['pick-up_plug'],
    'pick-up_tape': ['pick-up_tape'],
    'place_box+tape': ['place_tape+box'],
    'plug_plug': ['plug_plug', 'plug_socket', 'plug_plug+socket'],
    'pour_spoon': ['pour_spoon+jar', 'pour_spoon+cup'],
    'press_button': ['press_button', 'press_stop-button', 'push_button'],
    'pull-out_weight-pin': ['pull-out_weight-pin', 'pull_weight-pin'],
    'pull_drawer': ['pull_drawer'],
    'pull_rowing-machine': ['pull_rowing-machine'],
    'push_drawer': ['push_drawer'],
    'push_rowing-machine': ['push_rowing-machine'],
    'put_cup': ['put_cup', 'put_mug'],
    'put_jar': ['put_jar'],
    'rinse_cup': ['rinse_cup'],
    'rotate_weight-setting': ['rotate_weight-setting'],
    'scan_card-reader': ['scan_card-reader'],
    'scoop_spoon': ['scoop_spoon', 'scoop_jar+spoon', 'scoop_spoon+jar', 'spoon_'],
    'stir_spoon': ['stir_spoon+cup', 'stir_spoon', 'stir_cup+spoon'],
    'switch-on_socket': ['switch-on_socket'],
    'take_cup': ['take_cup'],
    'take_spoon': ['take_spoon'],
    'turn_tap': ['turn_tap']})


BEOID_class_keys_to_ignore = (
            'adjust_pedal',
            'check_screwdriver',
            'close_jar',
            'untangle_wire',
        )


@dataclass(frozen=True, order=True)
class BEOIDMultiVerb23Label(BEOIDClipLabel):
    """
    Filtered version (23 verbs) of the original Wray label (90 verbs).
    Using the verbs that exist in the Wray's 34 verb+noun suggestions.
    """
    wray_verblabel_str: str
    wray_verblabel_idx: int
    wray_multiverb_softlabel: list[float]
    wray_multiverb_str: list[str]
    wray_multiverb_idx: list[int]


    @classmethod
    def from_BEOIDClipLabel(cls, instance: BEOIDClipLabel, /,
            multiverb_filtered_softlabel: list[float],
            l1_norm = False,
            threshold = 0.2):

        if instance.label_str in BEOID_class_keys_to_ignore:
            return None

        dict_instance = asdict(instance)
        del dict_instance['label_str']      # Remove non-init values.

        # Single verb label
        beoid_to_wray_key = BEOID_class_key_to_Wray_class_key()
        wray_verblabel_str = beoid_to_wray_key[instance.label_str].split('_')[0]
        wray_verblabel_idx = Wray_verb_class_keys_filtered.index(wray_verblabel_str)

        if l1_norm:
            sum_softlabel = sum(multiverb_filtered_softlabel)
            multiverb_filtered_softlabel = [score / sum_softlabel for score in multiverb_filtered_softlabel]

        # Threshold soft labels
        multiverb_filtered_str = []
        for idx, label in enumerate(multiverb_filtered_softlabel):
            if label >= threshold:
                multiverb_filtered_str.append(Wray_verb_class_keys_filtered[idx])

        multiverb_idx = []
        for label in multiverb_filtered_str:
            multiverb_idx.append(Wray_verb_class_keys_filtered.index(label))

        return cls(**dict_instance, wray_verblabel_str = wray_verblabel_str, wray_verblabel_idx = wray_verblabel_idx,
                wray_multiverb_softlabel = multiverb_filtered_softlabel, wray_multiverb_str = multiverb_filtered_str,
                wray_multiverb_idx = multiverb_idx)
    

@dataclass(frozen=True, order=True)
class BEOIDMultiVerb42Label(BEOIDClipLabel):
    """
    The Wray label (42 verbs).
    Using the verbs that exist in the Wray's 34 verb+noun suggestions.
    And from the 90 verbs, only extract classes with samples in BEOID.
    """
    wray_multiverb_softlabel: list[float]
    wray_multiverb_str: list[str]
    wray_multiverb_idx: list[int]


    @classmethod
    def from_BEOIDClipLabel(cls, instance: BEOIDClipLabel, /,
            multiverb_softlabel: list[float],
            threshold = 0.5):

        if instance.label_str in BEOID_class_keys_to_ignore:
            return None

        dict_instance = asdict(instance)
        del dict_instance['label_str']      # Remove non-init values.

        # Threshold soft labels
        multiverb_str = []
        for idx, label in enumerate(multiverb_softlabel):
            if label >= threshold:
                multiverb_str.append(Wray_verb_class_keys_thresholded[idx])

        multiverb_idx = []
        for label in multiverb_str:
            multiverb_idx.append(Wray_verb_class_keys_thresholded.index(label))

        return cls(**dict_instance,
                wray_multiverb_softlabel = multiverb_softlabel,
                wray_multiverb_str = multiverb_str,
                wray_multiverb_idx = multiverb_idx)


@lru_cache
def BEOID_class_key_to_Wray_class_key() -> MappingProxyType[str, str]:
    ret = {}
    for k, v in Wray_class_key_to_BEOID_class_keys.items():
        for beoid_class_key in v:
            ret[beoid_class_key] = k
    return MappingProxyType(ret)


def BEOID_class_key_to_Wray_verb_label(wray_annotations_root_dir: str):
    with open(os.path.join(wray_annotations_root_dir, 'BEOID.pkl'), 'rb') as f:
        wray_beoid_label = pickle.load(f)

    beoid_to_wray_key = BEOID_class_key_to_Wray_class_key()
    beoid_key_to_wray_label = {}
    for beoid_key, wray_key in beoid_to_wray_key.items():
        beoid_key_to_wray_label[beoid_key] = wray_beoid_label[wray_key]

    return beoid_key_to_wray_label


@lru_cache
def class_filter_indices(wray_annotations_root_dir: str) -> tuple[int]:
    """
    From wray labels (90 classes), return filtering indices that will have 23 verb classes that exist in BEOID.
    ('move', 'open', 'pull-out', 'plug', 'insert', 'press', 'pull', 'rotate', 'scan', 'switch-on', 'fill', 'hold-down', 'scoop', 'take', 'stir', 'pick-up', 'put', 'pour', 'turn', 'let-go', 'place', 'push', 'rinse')
    """
    _BEOID_all_verbs = set()
    for label in Wray_class_key_to_BEOID_class_keys:
        _BEOID_all_verbs.add(label.split('_')[0])

    class_keys = read_class_keys(wray_annotations_root_dir)
    filtered_class_keys = tuple(key for key in class_keys if key in _BEOID_all_verbs)
    filter_indices = tuple(idx for idx, key in enumerate(class_keys) if key in _BEOID_all_verbs)
    assert filtered_class_keys == Wray_verb_class_keys_filtered
    return filter_indices


def BEOID_class_key_to_Wray_verb_label_filtered(wray_annotations_root_dir: str):
    filter_indices = class_filter_indices(wray_annotations_root_dir)

    beoid_key_to_wray_label = BEOID_class_key_to_Wray_verb_label(wray_annotations_root_dir)

    for beoid_key, wray_label in beoid_key_to_wray_label.items():
        beoid_key_to_wray_label[beoid_key] = [wray_label[idx] for idx in filter_indices]

    return beoid_key_to_wray_label


def read_all_annotations_filtered(wray_annotations_root_dir: str, BEOID_annotations_root_dir: str):
    """
    23-verb annotations
    """
    beoid_key_to_wray_label = BEOID_class_key_to_Wray_verb_label_filtered(wray_annotations_root_dir)
    BEOID_all_labels = beoid_read_all_annotations(BEOID_annotations_root_dir)
    clip_labels = []
    for label in BEOID_all_labels:
        if label.label_str in beoid_key_to_wray_label:
            new_label = BEOIDMultiVerb23Label.from_BEOIDClipLabel(label, beoid_key_to_wray_label[label.label_str], threshold=0.2)
            clip_labels.append(new_label)

    return clip_labels


def BEOID_class_key_to_Wray_verb_label_thresholded(wray_annotations_root_dir: str):
    beoid_key_to_wray_label = BEOID_class_key_to_Wray_verb_label(wray_annotations_root_dir)

    for beoid_key, wray_label in beoid_key_to_wray_label.items():
        beoid_key_to_wray_label[beoid_key] = [wray_label[idx] for idx, exist in enumerate(classes_exist) if exist]

    return beoid_key_to_wray_label

def read_all_annotations_thresholded(wray_annotations_root_dir: str, BEOID_annotations_root_dir: str):
    """
    42-verb annotations
    """
    beoid_key_to_wray_label = BEOID_class_key_to_Wray_verb_label_thresholded(wray_annotations_root_dir)
    BEOID_all_labels = beoid_read_all_annotations(BEOID_annotations_root_dir)
    clip_labels = []
    for label in BEOID_all_labels:
        if label.label_str in beoid_key_to_wray_label:
            new_label = BEOIDMultiVerb42Label.from_BEOIDClipLabel(label, beoid_key_to_wray_label[label.label_str], threshold=0.5)
            clip_labels.append(new_label)

    return clip_labels

def main():
    annotations_root = '/home/s1884147/scratch2/datasets/Multi-Verb-Labels'
    beoid_key_to_wray_label = BEOID_class_key_to_Wray_verb_label_filtered(annotations_root)
    print(beoid_key_to_wray_label)
    print(Wray_verb_class_keys_filtered)
    print(len(Wray_verb_class_keys_filtered))

    for key, labels in beoid_key_to_wray_label.items():
        print(f'BEOID key: {key}')
        for idx, label in enumerate(labels):
            if label >= 0.2:
                print(Wray_verb_class_keys_filtered[idx], label)
        print()

    BEOID_all_labels = read_all_annotations_thresholded(annotations_root, '/home/s1884147/scratch2/datasets/BEOID/Annotations')
    for label in BEOID_all_labels:
        print(label)


    num_multiverbs = 0
    for label in BEOID_all_labels:
        num_multiverbs += len(label.wray_multiverb_str)
    num_multiverbs /= len(BEOID_all_labels)
    
    print(f'{num_multiverbs = }')


    num_multiverbs_except_originalverb = 0
    for label in BEOID_all_labels:
        multiverb_except_originalverb = set(label.wray_multiverb_str)
        multiverb_except_originalverb.discard(label.wray_verblabel_str)
        num_multiverbs_except_originalverb += len(multiverb_except_originalverb)
    num_multiverbs_except_originalverb /= len(BEOID_all_labels)
    
    print(f'{num_multiverbs_except_originalverb = }')


    num_segments_per_class = {}
    for label in Wray_verb_class_keys_filtered:
        num_segments_per_class[label] = 0
    for label in BEOID_all_labels:
        num_segments_per_class[label.wray_verblabel_str] += 1

    print(f"{num_segments_per_class = }")


if __name__ == '__main__':
    main()

