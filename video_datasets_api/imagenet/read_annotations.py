import os 
_SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

def class_id_to_label():
    classid_to_label = {}
    with open(os.path.join(_SCRIPT_DIR, 'class_id.txt'), 'r') as f:
        for i, line in enumerate(f.read().splitlines()):
            classid_to_label[line] = i
    return classid_to_label

