from pathlib import Path
from typing import Any
from typing import Dict
from typing import Iterator

from dataclasses import asdict

from gulpio2.adapters import AbstractDatasetAdapter
from gulpio2.utils import resize_images

from simplejpeg import decode_jpeg_header

from .beoid import BEOIDMultiVerb23Label

import logging
logger = logging.getLogger(__name__)

Result = Dict[str, Any]


class WrayBEOIDAdapter(AbstractDatasetAdapter):
    def __init__(
        self,
        video_segment_dir: str,
        segment_infos: list[BEOIDMultiVerb23Label],
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
                list of BEOIDMultiVerb23Label that contains all information about frames, labels etc. This will be included in the meta data.

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
