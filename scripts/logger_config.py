"""
logger_config.py

Central logging setup, shared by every pipeline script (extract, transform, load).

Why this is its own file instead of being copy-pasted into every script:
If the logging format or destination ever needs to change, it changes in one place.
Every pipeline stage also ends up writing to the same log file, so someone debugging
a failed run can see the full end-to-end sequence of events in one place, instead of
three separate logs that do not line up with each other.
"""

import logging
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent / "reports"
LOG_FILE = LOG_DIR / "pipeline_run.log"


def get_logger(name: str) -> logging.Logger:
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid attaching duplicate handlers if this gets called more than once
    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
