import logging
import sys
from pathlib import Path


def setup_logger(verbose: bool = False, log_file: Path | None = None) -> logging.Logger:
    logger = logging.getLogger("transcribe_and_diarize")
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    logger.handlers.clear()
    h = logging.StreamHandler(sys.stdout)
    h.setLevel(logging.DEBUG if verbose else logging.INFO)
    h.setFormatter(
        logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s" if verbose else "%(message)s"
        )
    )
    logger.addHandler(h)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
        logger.addHandler(fh)
    return logger
