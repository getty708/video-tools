import os
import tempfile
import unittest.mock
from pathlib import Path

from video_tools.trim import trim_video
from video_tools.config_schema import TrimConfig, ClipConfig


def test_trim_video() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a dummy video file
        video_path = Path(tmpdir) / "test_video.mp4"
        with open(video_path, "w") as f:
            f.write("dummy video data")

        output_dir = Path(tmpdir) / "outputs"
        output_dir.mkdir()

        # Create structured config objects
        clip1 = ClipConfig(
            start_time="00:00:01",
            end_time="00:00:02",
            output_filename="clip1.mp4",
        )
        clip2 = ClipConfig(
            start_time="00:00:03",
            end_time="00:00:04",
            output_filename="clip2.mp4",
        )
        trim_config = TrimConfig(
            input_video_path=video_path,
            clips=[clip1, clip2],
            output_dir=output_dir,
        )

        with unittest.mock.patch("subprocess.run") as mock_run:
            trim_video(trim_config)

            # Check that ffmpeg was called with the correct arguments
            assert mock_run.call_count == 2
            mock_run.assert_any_call(
                [
                    "ffmpeg",
                    "-i",
                    str(video_path),
                    "-ss",
                    "00:00:01",
                    "-to",
                    "00:00:02",
                    "-c",
                    "copy",
                    os.path.join(str(output_dir), "clip1.mp4"),
                ],
                check=True,
            )
            mock_run.assert_any_call(
                [
                    "ffmpeg",
                    "-i",
                    str(video_path),
                    "-ss",
                    "00:00:03",
                    "-to",
                    "00:00:04",
                    "-c",
                    "copy",
                    os.path.join(str(output_dir), "clip2.mp4"),
                ],
                check=True,
            )
