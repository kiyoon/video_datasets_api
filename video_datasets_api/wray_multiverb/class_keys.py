from __future__ import annotations
from functools import lru_cache
import os

@lru_cache
def read_class_keys(wray_annotations_root_dir: str) -> tuple[str]:
    """
    Wray's 90 verbs
    """
    with open(os.path.join(wray_annotations_root_dir, 'class_order.csv'), 'r') as f:
        class_order = f.read()
    class_order = class_order[1:][:-2].replace('_', '-').split('","')
    return tuple(class_order)
