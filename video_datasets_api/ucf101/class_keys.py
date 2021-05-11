from .definitions import NUM_CLASSES
def get_class_keys(classind_txt_path: str) -> list:
    class_keys = []
    with open(classind_txt_path, "r") as f:
        for line in f.readlines():
            class_index, class_key = line.split(" ")
            class_keys.append(class_key.strip())

    assert len(class_keys) == NUM_CLASSES, f"Class keys have length len(class_keys) but it should be {NUM_CLASSES}. classInd.txt file may be corrupted."

    return class_keys

def get_class_keys_to_indices(classind_txt_path: str, label_offset:int = -1) -> list:
    """Return dict of class keys as keys and label indices as values.
    The official annotation counts from 1, so the label_offset makes it count from zero
    """
    class_keys_to_indices = {}
    with open(classind_txt_path, "r") as f:
        for line in f.readlines():
            class_index, class_key = line.split(" ")
            class_keys_to_indices[class_key.strip()] = int(class_index) + label_offset

    assert len(class_keys_to_indices) == NUM_CLASSES, f"Class keys have length len(class_keys_to_indices) but it should be {NUM_CLASSES}. classInd.txt file may be corrupted."

    return class_keys_to_indices

