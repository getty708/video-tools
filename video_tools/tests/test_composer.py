import tempfile
import unittest.mock
from pathlib import Path

from video_tools.composer import add_thumbnail, batch_add_thumbnail
from video_tools.config_schema import AddThumbnailConfig, BatchAddThumbnailConfig


@unittest.mock.patch("video_tools.composer.VideoFileClip")
@unittest.mock.patch("video_tools.composer.ImageClip")
@unittest.mock.patch("video_tools.composer.concatenate_videoclips")
def test_add_thumbnail(
    mock_concatenate_videoclips, mock_image_clip, mock_video_file_clip
) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        thumbnail_path = Path(tmpdir) / "thumb.png"
        thumbnail_path.touch()
        video_path = Path(tmpdir) / "video.mp4"
        video_path.touch()
        output_path = Path(tmpdir) / "output.mp4"

        # Create AddThumbnailConfig object
        config = AddThumbnailConfig(
            thumbnail_path=thumbnail_path,
            video_path=video_path,
            output_path=output_path,
            thumbnail_duration=2.0,
            fade_duration=0.5,
            audio_fade_duration=2.0,
            start_pos=0.0,
            debug=False,
        )

        # Mock moviepy objects
        mock_thumb = unittest.mock.MagicMock()
        mock_video = unittest.mock.MagicMock()
        mock_image_clip.return_value = mock_thumb
        mock_video_file_clip.return_value = mock_video

        mock_thumb.size = (1920, 1080)
        mock_video.size = (1920, 1080)
        mock_video.audio = True

        add_thumbnail(config)

        mock_image_clip.assert_called_once_with(str(thumbnail_path))
        mock_video_file_clip.assert_called_once_with(str(video_path))

        # Check that the final clip was written
        mock_concatenate_videoclips.return_value.write_videofile.assert_called_once_with(
            str(output_path), codec="libx264", audio_codec="aac"
        )


def test_batch_add_thumbnail() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        thumb1_path = tmp_path / "thumb1.png"
        video1_path = tmp_path / "video1.mp4"
        output1_path = tmp_path / "output1.mp4"
        thumb2_path = tmp_path / "thumb2.png"
        video2_path = tmp_path / "video2.mp4"
        output2_path = tmp_path / "output2.mp4"

        # Create dummy files
        thumb1_path.touch()
        video1_path.touch()
        thumb2_path.touch()
        video2_path.touch()

        # Create AddThumbnailConfig objects for the batch
        # item1_config will override some common parameters
        item1_config = AddThumbnailConfig(
            thumbnail_path=thumb1_path,
            video_path=video1_path,
            output_path=output1_path,
            thumbnail_duration=3.0,
            fade_duration=0.6,
            audio_fade_duration=2.5,
            start_pos=1.0,
            debug=True,
        )
        # item2_config will use common parameters
        item2_config = AddThumbnailConfig(
            thumbnail_path=thumb2_path,
            video_path=video2_path,
            output_path=output2_path,
        )

        # Create BatchAddThumbnailConfig object with common parameters
        batch_config = BatchAddThumbnailConfig(
            items=[item1_config, item2_config],
            thumbnail_duration=2.0,
            fade_duration=0.5,
            audio_fade_duration=2.0,
            start_pos=0.0,
            debug=False,
        )

        with unittest.mock.patch(
            "video_tools.composer.add_thumbnail"
        ) as mock_add_thumbnail:
            batch_add_thumbnail(batch_config)

            assert mock_add_thumbnail.call_count == 2

            # Expected merged config for item1
            expected_item1_config = AddThumbnailConfig(
                thumbnail_path=thumb1_path,
                video_path=video1_path,
                output_path=output1_path,
                thumbnail_duration=3.0,
                fade_duration=0.6,
                audio_fade_duration=2.5,
                start_pos=1.0,
                debug=True,
            )
            # Expected merged config for item2 (uses common params from batch_config)
            expected_item2_config = AddThumbnailConfig(
                thumbnail_path=thumb2_path,
                video_path=video2_path,
                output_path=output2_path,
                thumbnail_duration=2.0,
                fade_duration=0.5,
                audio_fade_duration=2.0,
                start_pos=0.0,
                debug=False,
            )

            mock_add_thumbnail.assert_any_call(expected_item1_config)
            mock_add_thumbnail.assert_any_call(expected_item2_config)
