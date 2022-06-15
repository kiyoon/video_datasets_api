from pathlib import Path
from typing import Any
from typing import Dict
from typing import Iterator
from typing import List

from gulpio2.adapters import AbstractDatasetAdapter
from gulpio2.utils import resize_images

from simplejpeg import decode_jpeg_header

import os
import glob
from natsort import natsorted

import logging
logger = logging.getLogger(__name__)

Result = Dict[str, Any]


class GenericJpegDatasetAdapter(AbstractDatasetAdapter):
    """Gulp Dataset Adapter for Gulping RGB frames.
    The meta data will NOT contain labels. It will only have num_frames and frame_size.
    Use this when you want to use Gulp as a way of accessing frames, and you'll have to read annotations separately on your own.
    """

    def __init__(
        self,
        video_segment_dir: str,
        frame_size: int = -1,
        class_folder: bool = False,
    ) -> None:
        """
        Args:
            video_segment_dir:
                Root directory containing segmented frames::

                    video_segment_dir/
                    ├── segment_1 
                    │   ├── frame_0000000001.jpg
                    │   ...
                    │   ├── frame_0000012345.jpg
                    │   ...

                "segment_1" will be the gulp key, and frames can be in any name. It will just sort all the jpegs and use them in order.

            frame_size:
                Size of shortest edge of the frame, if not already this size then it will
                be resized.

            class_folder:
                If set to True, the directory structure is expected to have classes.
                The gulp key would be class_name/segment_name.

                    video_segment_dir/
                    ├── brush_hair 
                    │   ├── segment_1
                    │   │   ├── frame_0000000001.jpg
                    │   │   ...
                    │   │   ├── frame_0000012345.jpg
                    │   ├── segment_2
                    │   │   ├── frame_0000000001.jpg
                    │   │   ...
                    │   │   ├── frame_0000012345.jpg
                    ├── catch 
                    │   ├── segment_3
                    │   │   ├── frame_0000000001.jpg
                    │   │   ...
                    │   │   ├── frame_0000012345.jpg
                    │   ├── segment_4
                    │   │   ├── frame_0000000001.jpg
                    │   │   ...
                    │   │   ├── frame_0000012345.jpg
                    │   ...

        """
        self.video_segment_dir = video_segment_dir
        self.frame_size = int(frame_size)
        self.class_folder = class_folder
        self.segment_ids = GenericJpegDatasetAdapter._iterate_and_generate_keys(video_segment_dir, class_folder)


    def iter_data(self, slice_element=None) -> Iterator[Result]:
        """Get frames and metadata corresponding to segment

        Args:
            slice_element (optional): If not specified all frames for the segment will be returned

        Yields:
            dict: dictionary with the fields

            * ``meta``: All metadata corresponding to the segment, this is the same as the data
              in the labels csv
            * ``frames``: list of :class:`PIL.Image.Image` corresponding to the frames specified
              in ``slice_element``
            * ``id``: UID corresponding to segment
        """
        slice_element = slice_element or slice(0, len(self))

        for segment_id in self.segment_ids[slice_element]:
            meta = {}
            folder = (
                Path(self.video_segment_dir) / segment_id
            )
            # Without glob.escape, it gives error when filename contains [ or ].
            paths = natsorted(glob.glob(str(Path(glob.escape(folder)) / '*.jpg')))
            if self.frame_size > 0:
                frames = list(resize_images(map(str, paths), self.frame_size))
                meta["frame_size"] = frames[0].shape
            else:
                frames = paths
                # Load only one file to check the frame size.
                with open(str(paths[0]), 'rb') as f:
                    first_frame_jpeg = f.read()
                h, w, colour, _ = decode_jpeg_header(first_frame_jpeg)
                meta["frame_size"] = (h, w, 3) if colour == 'rgb' else (h, w)
            meta["num_frames"] = len(frames)

            result = {"meta": meta, "frames": frames, "id": segment_id}
            yield result


    def __len__(self):
        return len(self.segment_ids)


    @staticmethod
    def _iterate_and_generate_keys(video_segment_dir: str, class_folder: bool = False) -> List[str]:
        data = []
        dirs = os.listdir(video_segment_dir)
        for dirname in dirs:
            dirpath = os.path.join(video_segment_dir, dirname)
            if not os.path.isdir(dirpath):
                logger.warning(f'Skipping non-directory {dirname}')
                continue

            if class_folder:
                segment_dirs = os.listdir(dirpath)
                for segment_dirname in segment_dirs:
                    segment_dirpath = os.path.join(dirpath, segment_dirname)
                    if not os.path.isdir(segment_dirpath):
                        logger.warning(f'Skipping non-directory {segment_dirpath}')
                        continue

                    data.append(os.path.join(dirname, segment_dirname))
            else:
                data.append(dirname)

        return data


class GenericGreyFlowDatasetAdapter(GenericJpegDatasetAdapter):
    """
    Gulp directory with flow greyscale images. Note that all jpeg files have to be single channel.
    X and Y direction have to be separated into different folders.
    """
    def __init__(
        self,
        video_segment_dir: str,
        frame_size: int = -1,
        class_folder: bool = False,
        flow_direction_x = 'u',
        flow_direction_y = 'v'
    ) -> None:
        """
        Args:
            video_segment_dir:
                Root directory containing segmented frames::

                    video_segment_dir/
                    ├── segment_1 
                    │   ├── u
                    │   │   ├── frame_0000000001.jpg
                    │   │   ...
                    │   │   ├── frame_0000012345.jpg
                    │   ├── v
                    │   │   ├── frame_0000000001.jpg
                    │   │   ...
                    │   │   ├── frame_0000012345.jpg
                    │   ...

                "segment_1" will be the gulp key, and frames can be in any name. It will just sort all the jpegs and use them in order.

            frame_size:
                Size of shortest edge of the frame, if not already this size then it will
                be resized.

            class_folder:
                If set to True, the directory structure is expected to have classes.
                The gulp key would be class_name/segment_name.

            flow_direction_x:
                The directory name of the x direction flow frames.

            flow_direction_y:
                The directory name of the y direction flow frames.
        """
        super().__init__(video_segment_dir, frame_size, class_folder)
        self.flow_direction_x = flow_direction_x
        self.flow_direction_y = flow_direction_y


    def iter_data(self, slice_element=None) -> Iterator[Result]:
        slice_element = slice_element or slice(0, len(self))
        for segment_id in self.segment_ids[slice_element]:
            meta = {}

            folder = Path(self.video_segment_dir) / segment_id 
            paths = {
                # Without glob.escape, it gives error when filename contains [ or ].
                axis: natsorted(glob.glob(str(Path(glob.escape(folder)) / axis / '*.jpg')))
                for axis in [self.flow_direction_x, self.flow_direction_y]
            }

            basenames = {
                axis: [os.path.basename(path) for path in paths[axis]]
                for axis in [self.flow_direction_x, self.flow_direction_y]
            }

            assert basenames[self.flow_direction_x] == basenames[self.flow_direction_y], f'{folder} does not contain the same frames for {self.flow_direction_x} and {self.flow_direction_y}.'

            frames = {}
            if self.frame_size > 0:
                for axis in self.flow_direction_x, self.flow_direction_y:
                    frames[axis] = list(resize_images(map(str, paths[axis]), self.frame_size))
                meta["frame_size"] = frames[self.flow_direction_x][0].shape
            else:
                for axis in self.flow_direction_x, self.flow_direction_y:
                    frames[axis] = paths[axis]
                # Load only one file to check the frame size.
                with open(str(paths[self.flow_direction_x][0]), 'rb') as f:
                    first_frame_jpeg = f.read()
                h, w, colour, _ = decode_jpeg_header(first_frame_jpeg)
                assert colour == 'Gray', f'The colourspace of the image {paths[self.flow_direction_x][0]} is {colour}, but it needs to be "gray"'
                meta["frame_size"] = (h, w)

            meta["num_frames"] = len(frames[self.flow_direction_x])
            result = {
                "meta": meta,
                "frames": list(_intersperse(frames[self.flow_direction_x], frames[self.flow_direction_y])),
                "id": segment_id,
            }
            yield result


class GlobPatternGreyFlowDatasetAdapter(GenericJpegDatasetAdapter):
    """
    Gulp directory with flow greyscale images. Note that all jpeg files have to be single channel.
    Detect x, y direction by glob pattern instead of separate folders.
    """
    def __init__(
        self,
        video_segment_dir: str,
        frame_size: int = -1,
        class_folder: bool = False,
        flow_x_filename_pattern = 'flow_x_*.jpg',
        flow_y_filename_pattern = 'flow_y_*.jpg',   # Default value for open-mmlab/denseflow
    ) -> None:
        """
        Args:
            video_segment_dir:
                Root directory containing segmented frames::

                    video_segment_dir/
                    ├── segment_1 
                    │   ├── flow_x_00000.jpg
                    │   ...
                    │   ├── flow_x_12345.jpg
                    │   ...
                    │   ├── flow_y_00000.jpg
                    │   ...
                    │   ├── flow_y_12345.jpg

                "segment_1" will be the gulp key, and frames can be in any name. It will just sort all the jpegs and use them in order.

            frame_size:
                Size of shortest edge of the frame, if not already this size then it will
                be resized.

            class_folder:
                If set to True, the directory structure is expected to have classes.
                The gulp key would be class_name/segment_name.

            flow_x_filename_pattern, flow_y_filename_pattern:
                File names in bash pattern to search.
        """
        super().__init__(video_segment_dir, frame_size, class_folder)
        self.flow_x_filename_pattern = flow_x_filename_pattern
        self.flow_y_filename_pattern = flow_y_filename_pattern


    def iter_data(self, slice_element=None) -> Iterator[Result]:
        slice_element = slice_element or slice(0, len(self))
        for segment_id in self.segment_ids[slice_element]:
            meta = {}

            folder = Path(self.video_segment_dir) / segment_id 
            paths = {
                # Without glob.escape, it gives error when filename contains [ or ].
                'x': natsorted(glob.glob(str(Path(glob.escape(folder)) / self.flow_x_filename_pattern))),
                'y': natsorted(glob.glob(str(Path(glob.escape(folder)) / self.flow_y_filename_pattern))),
            }

            basenames = {
                axis: [os.path.basename(path) for path in paths[axis]]
                for axis in ['x', 'y']
            }

            assert basenames['x'] == basenames['y'], f'{folder} does not contain the same frames for x and y.'

            frames = {}
            if self.frame_size > 0:
                for axis in ['x', 'y']:
                    frames[axis] = list(resize_images(map(str, paths[axis]), self.frame_size))
                meta["frame_size"] = frames['x'][0].shape
            else:
                for axis in ['x', 'y']:
                    frames[axis] = paths[axis]
                # Load only one file to check the frame size.
                with open(str(paths['x'][0]), 'rb') as f:
                    first_frame_jpeg = f.read()
                h, w, colour, _ = decode_jpeg_header(first_frame_jpeg)
                assert colour == 'Gray', f'The colourspace of the image {paths["x"][0]} is {colour}, but it needs to be "gray"'
                meta["frame_size"] = (h, w)

            meta["num_frames"] = len(frames['x'])
            result = {
                "meta": meta,
                "frames": list(_intersperse(frames['x'], frames['y'])),
                "id": segment_id,
            }
            yield result


def _intersperse(*lists):
    """
    Args:
        *lists:

    Examples:
        >>> list(_intersperse(['a', 'b']))
        ['a', 'b']
        >>> list(_intersperse(['a', 'c'], ['b', 'd']))
        ['a', 'b', 'c', 'd']
        >>> list(_intersperse(['a', 'd'], ['b', 'e'], ['c', 'f']))
        ['a', 'b', 'c', 'd', 'e', 'f']
        >>> list(_intersperse(['a', 'd', 'g'], ['b', 'e'], ['c', 'f']))
        ['a', 'b', 'c', 'd', 'e', 'f']

    """
    i = 0
    min_length = min(map(len, lists))
    total_element_count = len(lists) * min_length
    for i in range(0, total_element_count):
        list_index = i % len(lists)
        element_index = i // len(lists)
        yield lists[list_index][element_index]
