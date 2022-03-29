import argparse
from pathlib import Path
import random

from video_datasets_api.wray_multiverb.beoid import read_all_annotations


parser = argparse.ArgumentParser(
    "Generate splits of BEOID dataset (Wray)"
)
parser.add_argument(
    "out_folder", type=Path, help="Directory to store the gulped files."
)
parser.add_argument(
    "wray_annotations_root_dir",
    type=Path,
)
parser.add_argument(
    "BEOID_annotations_root_dir",
    type=Path,
)
parser.add_argument("--train_ratio", default=70)
parser.add_argument("--num_splits", default=5)
parser.add_argument("--seed", default=12)



def main(args):
    assert 1 < args.train_ratio < 100
    random.seed(args.seed)
    segments_info = read_all_annotations(str(args.wray_annotations_root_dir), str(args.BEOID_annotations_root_dir))
    verb_to_segments = {}
    for segment_info in segments_info:
        verb = segment_info.wray_verblabel_str
        if verb in verb_to_segments.keys():
            verb_to_segments[verb].append(segment_info.clip_id_str)
        else:
            verb_to_segments[verb] = [segment_info.clip_id_str]

    args.out_folder.mkdir(exist_ok=True, parents=True)

    for split in range(args.num_splits):
        with open(args.out_folder / f'split{split}_train.txt', 'w') as train_split:
            with open(args.out_folder / f'split{split}_val.txt', 'w') as val_split:
                for verb, segments in verb_to_segments.items():
                    num_train_samples = round(len(segments) * args.train_ratio / 100)
                    random.shuffle(segments)
                    
                    train_split.writelines(line + '\n' for line in segments[:num_train_samples])
                    val_split.writelines(line + '\n' for line in segments[num_train_samples:])


if __name__ == "__main__":
    main(parser.parse_args())
