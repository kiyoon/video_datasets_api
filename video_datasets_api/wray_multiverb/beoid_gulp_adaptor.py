import os
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Iterator

from dataclasses import asdict

from gulpio2.adapters import AbstractDatasetAdapter
from gulpio2.utils import resize_images

from simplejpeg import decode_jpeg_header

from .beoid import BEOIDMultiVerb42Label

import logging
logger = logging.getLogger(__name__)

Result = Dict[str, Any]


class WrayBEOIDAdapter(AbstractDatasetAdapter):
    def __init__(
        self,
        video_segment_dir: str,
        segment_infos: list[BEOIDMultiVerb42Label],
        frame_size: int = -1,
        filename_format = '{:05d}.jpg'
    ) -> None:
        """
        Args:
            video_segment_dir:
                Root directory containing segmented frames::

                    video_segment_dir/
                    ├── Videos_Desk 
                    │   ├── 00_Desk1
                    │   │   ├── 00001.jpg
                    │   │   ...
                    │   │   ├── 12345.jpg
                    │   ...

                "segment_1" will be the gulp key, and frames can be in any name. It will just sort all the jpegs and use them in order.

            segment_infos:
                list of BEOIDMultiVerb42Label that contains all information about frames, labels etc. This will be included in the meta data.

            frame_size:
                Size of shortest edge of the frame, if not already this size then it will
                be resized.
        """
        self.video_segment_dir = video_segment_dir
        self.frame_size = int(frame_size)
        self.segment_infos = segment_infos
        self.filename_format = filename_format

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

        for segment_info in self.segment_infos[slice_element]:
            video_dir = segment_info.filename_wo_ext[3:-1]
            video_dir = f'Videos_{video_dir}'
            meta = asdict(segment_info)
            folder = (
                Path(self.video_segment_dir) / video_dir / segment_info.filename_wo_ext
            )
            paths = [folder / self.filename_format.format(idx) for idx in range(segment_info.start_frame, segment_info.end_frame + 1)]
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

            result = {"meta": meta, "frames": frames, "id": segment_info.clip_id_str}
            yield result

    def __len__(self):
        return len(self.segment_infos)


class WrayBEOIDFlowDatasetAdapter(WrayBEOIDAdapter):
    """
    Gulp directory with flow greyscale images. Note that all jpeg files have to be single channel.
    Detect x, y direction by glob pattern instead of separate folders.
    """
    def __init__(
        self,
        video_segment_dir: str,
        segment_infos: list[BEOIDMultiVerb42Label],
        frame_size: int = -1,
        filename_format = 'flow_{direction}_{index:05d}.jpg',
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
        super().__init__(video_segment_dir, segment_infos, frame_size, filename_format)


    def iter_data(self, slice_element=None) -> Iterator[Result]:
        slice_element = slice_element or slice(0, len(self))
        for segment_info in self.segment_infos[slice_element]:
            video_dir = segment_info.filename_wo_ext[3:-1]
            video_dir = f'Videos_{video_dir}'
            meta = asdict(segment_info)

            folder = (
                Path(self.video_segment_dir) / video_dir / segment_info.filename_wo_ext
            )
            paths = {
                'x': [folder / self.filename_format.format(direction = 'x', index = idx) for idx in range(segment_info.start_frame-1, segment_info.end_frame-1)],
                'y': [folder / self.filename_format.format(direction = 'y', index = idx) for idx in range(segment_info.start_frame-1, segment_info.end_frame-1)]
            }

            basenames = {
                axis: [os.path.basename(path) for path in paths[axis]]
                for axis in ['x', 'y']
            }

            assert len(basenames['x']) == len(basenames['y']), f'{folder} does not contain the same number of frames for x and y.'

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
                "id": segment_info.clip_id_str,
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
