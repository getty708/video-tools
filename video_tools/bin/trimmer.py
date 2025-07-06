import click
from pathlib import Path
from loguru import logger
from omegaconf import OmegaConf
from cattrs import structure

from video_tools.trim import trim_video as trim_video_core
from video_tools.config_schema import TrimConfig

_DEFAULT_CONFIG_PATH = Path("data/configs/trim_config.yaml")


@click.command("trim-video")
@click.option(
    "-c",
    "--config",
    default=str(_DEFAULT_CONFIG_PATH),
    type=click.Path(exists=True, file_okay=True),
)
def trim_video(config: str) -> None:
    """
    Trims a video based on a YAML configuration file.
    """
    # Load config using OmegaConf
    conf = OmegaConf.load(config)
    # Convert to structured config using cattrs
    trim_config_obj = structure(conf, TrimConfig)

    trim_video_core(trim_config_obj)
    logger.info("Trim operation completed.")


if __name__ == "__main__":
    trim_video()
