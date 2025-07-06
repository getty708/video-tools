import moviepy.audio.fx as afx
from moviepy import ImageClip, VideoFileClip, concatenate_videoclips, vfx

from video_tools.config_schema import AddThumbnailConfig, BatchAddThumbnailConfig


def add_thumbnail(config: AddThumbnailConfig) -> None:
    """
    Adds a thumbnail image to the beginning of a video with a fade transition and audio fade-in.
    """
    # Use config object directly
    thumbnail_path = config.thumbnail_path
    video_path = config.video_path
    output_path = config.output_path
    thumbnail_duration = config.thumbnail_duration
    fade_duration = config.fade_duration
    audio_fade_duration = config.audio_fade_duration
    start_pos = config.start_pos
    debug = config.debug

    # Ensure output directory exists
    output_dir = output_path.parent
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    # Load the thumbnail image and video clip
    thumbnail_clip = ImageClip(str(thumbnail_path)).with_duration(thumbnail_duration)
    video_clip = VideoFileClip(str(video_path)).subclipped(start_pos)

    # Resize thumbnail to match video dimensions if necessary
    if thumbnail_clip.size != video_clip.size:
        thumbnail_clip = thumbnail_clip.resized(new_size=video_clip.size)

    # Apply audio fade-in to the main video's audio
    if video_clip.audio:
        video_clip = video_clip.with_effects([afx.AudioFadeIn(audio_fade_duration)])

    # Concatenate thumbnail and video with a fade transition
    final_clip = concatenate_videoclips(
        [
            thumbnail_clip.with_effects([vfx.FadeOut(fade_duration)]),
            video_clip.with_effects([vfx.FadeIn(fade_duration)]),
        ]
    )

    # Write the result to a file
    if debug:
        final_clip = final_clip.subclipped(0, 30)

    final_clip.write_videofile(str(output_path), codec="libx264", audio_codec="aac")


def batch_add_thumbnail(config: BatchAddThumbnailConfig) -> None:
    """
    Applies add_thumbnail to multiple videos based on a YAML configuration file.
    """
    for item_config in config:
        add_thumbnail(item_config)
