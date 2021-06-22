import os 
from scipy import io
from .definitions import NUM_CLASSES

from typing import Any, Dict, List, Iterator, Optional, Tuple

# modified from torchvision.datasets.imagenet
# label is obtained by sorting the WordNet IDs.
# index in the meta.mat is NOT the label.
def parse_meta_mat(meta_mat_path:str) -> Tuple[Dict[int, int], Dict[str, int], List[str]]:
    meta = io.loadmat(meta_mat_path, squeeze_me=True)['synsets']
    nums_children = list(zip(*meta))[4]
    meta = [meta[idx] for idx, num_children in enumerate(nums_children)
	    if num_children == 0]
    idcs, wnids, class_keys = list(zip(*meta))[:3]

    # sort with wnid
    sorted_classes = sorted(zip(idcs, wnids, class_keys), key=lambda tup: tup[1])
    val_idx_to_label = {}
    wnid_to_label = {}
    class_keys = []
    for label, (idc, wnid, class_key) in enumerate(sorted_classes):
        class_keys.append(class_key)
        wnid_to_label[wnid] = label
        val_idx_to_label[idc] = label


    return val_idx_to_label, wnid_to_label, class_keys
