import subprocess
from pathlib import Path
from typing import List

from loguru import logger

from video_tools.config_schema import TrimConfig


def trim_video(config: TrimConfig) -> None:
    """
    Trims a video based on a YAML configuration file.
    """
    input_video: Path = config.input_video_path
    output_dir: Path = config.output_dir

    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    for clip in config.clips:
        start_time: str = clip.start_time
        end_time: str = clip.end_time
        output_filename: str = clip.output_filename
        output_path = output_dir / output_filename

        logger.info(f"Export {output_path}")
        command: List[str] = [
            "ffmpeg",
            "-i",
            str(input_video),
            "-ss",
            start_time,
            "-to",
            end_time,
            "-c",
            "copy",
            str(output_path),
        ]

        subprocess.run(command, check=True)
