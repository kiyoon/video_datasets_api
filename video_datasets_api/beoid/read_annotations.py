import os
from dataclasses import dataclass
from .definitions import NUM_VIDEOS, NUM_CLIPS

@dataclass(frozen=True)
class BEOIDClipLabel:
    filename_wo_ext: str
    clip_id_str: str
    clip_id: int
    start_frame: int
    end_frame: int
    verb_label: str
    noun_labels: list[str]


def read_all_annotations(annotations_root_dir: str) -> list[BEOIDClipLabel]:
    """
    As well as reading all labels, it will assign unique clip ID in string and integer form.

    Example: first clip of the 00_Desk1.csv file
    clip_id_str = 00_Desk1_00
    clip_id = 0

    first clip of the 00_Desk2.csv file
    clip_id_str = 00_Desk2_00
    clip_id = 6
    """

    label_files = sorted(os.listdir(annotations_root_dir))
    assert len(label_files) == NUM_VIDEOS, f'Some label files seem to be missing or you have too many files. You should have {NUM_VIDEOS} but you have {len(label_files)} files.'

    BEOID_all_labels = []

    clip_id = 0
    for label_file in label_files:
        filename = os.path.splitext(label_file)[0]

        with open(os.path.join(annotations_root_dir, label_file), 'r') as f:
            lines = f.readlines()

        for clip_idx, line in enumerate(lines):
            fields = line.split(',')
            start_frame = int(fields[0])
            end_frame = int(fields[1])
            verb_label = fields[2].split('.v.')[0]
            noun_label = fields[3:]
            noun_label = [noun.strip() for noun in noun_label]
            if noun_label[-1] == '':
                del noun_label[-1]

            BEOID_all_labels.append(BEOIDClipLabel(filename, f'{filename}_{clip_idx:02d}', clip_id, start_frame, end_frame, verb_label, noun_label))
            clip_id += 1

    assert len(BEOID_all_labels) == NUM_CLIPS, f'Some label files seem to be missing or corrupted. You should have {NUM_CLIPS} video clips but it read {len(BEOID_all_labels)} clips.'
    return BEOID_all_labels


if __name__ == '__main__':

    BEOID_all_labels = read_all_annotations('/home/s1884147/scratch2/datasets/BEOID/Annotations')
    for BEOID_clip_label in BEOID_all_labels:
        print(BEOID_clip_label)

    

