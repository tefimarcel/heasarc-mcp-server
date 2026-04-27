import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Base directory for astronomical data
# Can be overridden with the ASTRO_DATA_DIR environment variable
_default_data_dir = Path.home() / "astro_data"
_env_data_dir = os.environ.get("ASTRO_DATA_DIR")

if _env_data_dir:
    ASTRO_DATA_DIR = Path(_env_data_dir)
    if not ASTRO_DATA_DIR.exists():
        logger.warning(
            f"ASTRO_DATA_DIR is set to '{ASTRO_DATA_DIR}' but this directory does not exist. "
            f"It will be created automatically when needed."
        )
    elif not ASTRO_DATA_DIR.is_dir():
        raise ValueError(
            f"ASTRO_DATA_DIR is set to '{ASTRO_DATA_DIR}' but this path is not a directory."
        )
    else:
        logger.info(f"Using custom data directory: {ASTRO_DATA_DIR}")
else:
    ASTRO_DATA_DIR = _default_data_dir
    logger.info(f"Using default data directory: {ASTRO_DATA_DIR}")

# Standard subdirectories created for each object workspace
OBJECT_SUBDIRS = ["obsid", "scripts", "plots"]

# Scientific notes filename inside each object folder
NOTES_FILENAME = "notes.md"
