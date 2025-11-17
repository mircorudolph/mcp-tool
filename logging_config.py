import logging
import os


def setup_logger() -> None:
    """
    Configure the root logger based on the LOG_LEVEL environment variable.

    LOG_LEVEL can be one of the standard logging levels (e.g. DEBUG, INFO, WARNING).
    Defaults to INFO if unset or invalid.
    """
    env_level = os.getenv("LOG_LEVEL", "INFO").upper().strip()
    level = getattr(logging, env_level, logging.INFO)

    logging.basicConfig(
        level=level,
        format="%(asctime)s %(filename)s:%(lineno)d - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True,
    )
