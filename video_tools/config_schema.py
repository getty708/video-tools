from pathlib import Path
from typing import List, Optional

from attrs import define


@define
class ClipConfig:
    start_time: str
    end_time: str
    output_filename: str


@define
class TrimConfig:
    input_video_path: Path
    clips: List[ClipConfig]
    output_dir: Path


@define
class AddThumbnailConfig:
    thumbnail_path: Path
    video_path: Path
    output_path: Path
    thumbnail_duration: Optional[float] = None
    fade_duration: Optional[float] = None
    audio_fade_duration: Optional[float] = None
    start_pos: Optional[float] = None
    debug: Optional[bool] = None


@define(slots=False)
class BatchAddThumbnailConfig:
    items: List[AddThumbnailConfig]
    thumbnail_duration: float = 2.0
    fade_duration: float = 0.5
    audio_fade_duration: float = 2.0
    start_pos: float = 0.0
    debug: bool = False

    def __iter__(self):
        self._current_item_index = 0
        return self

    def __next__(self) -> AddThumbnailConfig:
        if self._current_item_index < len(self.items):
            item = self.items[self._current_item_index]
            self._current_item_index += 1

            # Create a new AddThumbnailConfig with merged parameters
            return AddThumbnailConfig(
                thumbnail_path=item.thumbnail_path,
                video_path=item.video_path,
                output_path=item.output_path,
                thumbnail_duration=item.thumbnail_duration
                if item.thumbnail_duration is not None
                else self.thumbnail_duration,
                fade_duration=item.fade_duration
                if item.fade_duration is not None
                else self.fade_duration,
                audio_fade_duration=item.audio_fade_duration
                if item.audio_fade_duration is not None
                else self.audio_fade_duration,
                start_pos=item.start_pos
                if item.start_pos is not None
                else self.start_pos,
                debug=item.debug if item.debug is not None else self.debug,
            )
        else:
            raise StopIteration
            raise StopIteration
            raise StopIteration
