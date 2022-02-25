import os
from .definitions import NUM_VERB_CLASSES, NUM_NOUN_CLASSES

def get_head_tail_classes(annotations_root_dir: str, verbnoun = 'verb'):
    assert verbnoun in ['verb', 'noun']
    num_classes = NUM_VERB_CLASSES if verbnoun == 'verb' else NUM_NOUN_CLASSES

    tail_classes_file = os.path.join(annotations_root_dir, f'EPIC_100_tail_{verbnoun}s.csv')

    with open(tail_classes_file, 'r') as f:
        tail_classes = list(map(int, f.readlines()[1:]))

    head_classes = [x for x in range(num_classes) if x not in tail_classes]

    return head_classes, tail_classes
