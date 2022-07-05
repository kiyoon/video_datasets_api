from __future__ import annotations
from .definitions import NUM_CLASSES, NUM_VIDEOS
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


def get_unique_video_id(filelist_txt_path = os.path.join(SCRIPT_DIR, 'hmdb_videos_list.txt')) -> tuple[dict[str, int], list[str]]:
    """
    Return:
        filename_to_video_id (dict), video_id_to_filename (list)
    """
    filenames = []
    filename_to_video_id = {}
    with open(filelist_txt_path) as f:
        filenames = f.read().splitlines()

    for idx, filename in enumerate(filenames):
        filename_to_video_id[filename] = idx

    assert len(filenames) == len(filename_to_video_id) == NUM_VIDEOS, f'Expected number of videos is {NUM_VIDEOS} but got {len(filenames)}'

    return filename_to_video_id, filenames




if __name__ == "__main__":
    class_keys = get_class_keys()

    print(class_keys)

