# video-tools

This project provides a collection of tools for video manipulation, now featuring structured configuration for enhanced clarity and maintainability. Configuration is defined using Python classes with `attrs`, loaded via `omegaconf`, and validated using `cattrs`.

## Usage

The tools are accessible via command-line interfaces.

### `trim-video`

This command trims a video file based on a YAML configuration file.

**Arguments:**

- `CONFIG_FILE`: The path to the YAML configuration file.

**Example:**

```bash
trim-video data/configs/trim_config.yaml
```

### Sample `trim-video` Configuration

The `CONFIG_FILE` should be a YAML file with the following structure:

```yaml
input_video_path: data/inputs/your_video.mp4
output_dir: data/outputs/trimmed_videos # New: Output directory is now part of the config
clips:
  - start_time: 00:00:10
    end_time: 00:00:20
    output_filename: clip1.mp4
  - start_time: 00:01:30
    end_time: 00:01:45
    output_filename: clip2.mp4
```

### `compose`

This command provides subcommands for composing video elements, such as adding thumbnails.

#### `compose add-thumbnail`

This subcommand adds a thumbnail image to the beginning of a video with a fade transition and audio fade-in, based on a YAML configuration file.

**Arguments:**

- `CONFIG_FILE`: The path to the YAML configuration file.

**Example:**

```bash
compose add-thumbnail data/configs/add_thumbnail_config.yaml
```

#### Sample `add-thumbnail` Configuration

The `CONFIG_FILE` should be a YAML file with the following structure:

```yaml
thumbnail_path: data/inputs/thumbnails/your_thumnail.png
video_path: data/outputs/your_trimmed_video.mp4
output_path: final_video.mp4
thumbnail_duration: 2.0 # Optional: Duration to display the thumbnail in seconds (default: 2.0)
fade_duration: 0.5 # Optional: Duration of the fade transition in seconds (default: 0.5)
audio_fade_duration: 2.0 # Optional: Duration of the audio fade-in for the main video (default: 2.0)
start_pos: 0.0 # Optional: Start position of the main video in seconds (default: 0.0)
debug: False # Optional: Enable debug mode (limit video generation to 30 seconds) (default: False)
```

#### `compose batch-add-thumbnail`

This subcommand applies `add-thumbnail` to multiple videos based on a YAML configuration file. Common parameters can be defined at the batch level and will be applied to individual items unless overridden.

**Arguments:**

- `CONFIG_FILE`: The path to the YAML configuration file.

**Example:**

```bash
compose batch-add-thumbnail data/configs/batch_thumbnail_config.yaml
```

#### Sample `batch-add-thumbnail` Configuration

The `CONFIG_FILE` for `compose batch-add-thumbnail` should be a YAML file containing a list of configurations. Common parameters can be specified at the top level, and individual items can override them.

```yaml
# Common parameters for all items in this batch (optional)
thumbnail_duration: 2.0
fade_duration: 0.5
audio_fade_duration: 2.0
start_pos: 0.0
debug: False

items: # List of individual add-thumbnail configurations
  - thumbnail_path: data/inputs/thumbnails/video1_thumb.png
    video_path: data/outputs/video1.mp4
    output_path: final_video1.mp4
    # Individual parameters can override common ones
    thumbnail_duration: 3.0
    fade_duration: 1.0
  - thumbnail_path: data/inputs/thumbnails/video2_thumb.png
    video_path: data/outputs/video2.mp4
    output_path: final_video2.mp4
    # Optional parameters will use common values or their default values if not specified
```
