"""Program for building GulpIO directory of frames for training
See :ref:`cli_tools_gulp_ingestor` for usage details 
Original code from https://github.com/epic-kitchens/C1-Action-Recognition-TSN-TRN-TSM
Modified by Kiyoon Kim for more generic use."""
import argparse
from multiprocessing import cpu_count
from pathlib import Path

from gulpio2 import GulpIngestor
from video_datasets_api.gulpio import GenericJpegDatasetAdapter, GenericGreyFlowDatasetAdapter, GlobPatternGreyFlowDatasetAdapter


parser = argparse.ArgumentParser(
    "Gulp video dataset allowing for faster read times during training."
)
parser.add_argument(
    "in_folder",
    type=Path,
    help="Directory where subdirectory is a segment name containing frames for that segment.",
)
parser.add_argument(
    "out_folder", type=Path, help="Directory to store the gulped files."
)
parser.add_argument("modality", choices=["flow", "rgb", "flow_onefolder"], help='flow_onefolder has x and y direction in a same folder.')
parser.add_argument("--class_folder", action='store_true', help="The directory structure is expected to have classes first and then segments.")
parser.add_argument("--flow_direction_x", default='u', help="Flow directory name for x direction.")
parser.add_argument("--flow_direction_y", default='v', help="Flow directory name for x direction.")
parser.add_argument("--flow_x_filename_pattern", default='flow_x_*.jpg', help="Flow filename pattern for x direction (flow_onefolder)")
parser.add_argument("--flow_y_filename_pattern", default='flow_y_*.jpg', help="Flow filename pattern for y direction (flow_onefolder)")
parser.add_argument("--frame_size", type=int, default=-1, help="Shorter side of the frame size. -1 bypasses resizing.")
parser.add_argument(
    "--segments_per_chunk",
    type=int,
    default=100,
    help="Number of action segments per chunk to save.",
)
parser.add_argument(
    "-j",
    "--num_workers",
    type=int,
    default=cpu_count(),
    help="Number of workers to run the task.",
)


def main(args):
    if args.modality.lower() == "flow":
        gulp_adapter = GenericGreyFlowDatasetAdapter(
            str(args.in_folder), args.frame_size, args.class_folder, args.flow_direction_x, args.flow_direction_y
        )
    elif args.modality.lower() == "flow_onefolder":
        gulp_adapter = GlobPatternGreyFlowDatasetAdapter(
            str(args.in_folder), args.frame_size, args.class_folder, args.flow_x_filename_pattern, args.flow_y_filename_pattern,
        )
    elif args.modality.lower() == "rgb":
        gulp_adapter = GenericJpegDatasetAdapter(
            str(args.in_folder), args.frame_size, args.class_folder, 
        )
    else:
        raise ValueError("Modality '{}' not supported".format(args.modality))
    ingestor = GulpIngestor(
        gulp_adapter, str(args.out_folder), args.segments_per_chunk, args.num_workers
    )
    ingestor()


if __name__ == "__main__":
    main(parser.parse_args())
