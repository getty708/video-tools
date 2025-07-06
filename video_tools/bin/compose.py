import click
from loguru import logger
from omegaconf import OmegaConf
from cattrs import structure

from video_tools.composer import add_thumbnail as add_thumbnail_core
from video_tools.composer import batch_add_thumbnail as batch_add_thumbnail_core
from video_tools.config_schema import AddThumbnailConfig, BatchAddThumbnailConfig


@click.group()
def cli():
    pass


@cli.command("add-thumbnail")
@click.argument("config_file", type=click.Path(exists=True))
@click.option(
    "--debug",
    is_flag=True,
    help="Enable debug mode (limit video generation to 30 seconds).",
)
def add_thumbnail(config_file: str, debug: bool) -> None:
    """
    Adds a thumbnail image to the beginning of a video with a fade transition and audio fade-in.
    """
    # Load config using OmegaConf
    conf = OmegaConf.load(config_file)
    # Convert to structured config using cattrs
    add_thumbnail_config_obj = structure(conf, AddThumbnailConfig)
    add_thumbnail_config_obj.debug = debug

    add_thumbnail_core(add_thumbnail_config_obj)
    logger.info(
        f"Video with thumbnail intro saved to: {add_thumbnail_config_obj.output_path}"
    )


@cli.command("batch-add-thumbnail")
@click.argument("config_file", type=click.Path(exists=True))
@click.option(
    "--debug",
    is_flag=True,
    help="Enable debug mode (limit video generation to 30 seconds).",
)
def batch_add_thumbnail(config_file: str, debug: bool) -> None:
    """
    Applies add_thumbnail to multiple videos based on a YAML configuration file.
    """
    # Load config using OmegaConf
    conf = OmegaConf.load(config_file)
    # Convert to structured config using cattrs
    batch_add_thumbnail_config_obj = structure(conf, BatchAddThumbnailConfig)

    # Override debug for each item in the batch if debug is set in CLI
    for item in batch_add_thumbnail_config_obj.items:
        item.debug = debug

    batch_add_thumbnail_core(batch_add_thumbnail_config_obj)
    logger.info("Batch operation completed.")


if __name__ == "__main__":
    cli()
