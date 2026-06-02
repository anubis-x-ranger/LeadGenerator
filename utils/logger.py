
import logging
from config import config


def setup_logger(name: str = "lead_engine"):

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(config.logging.log_level)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    if config.logging.log_to_file:

        file_handler = logging.FileHandler(
            config.logging.log_file
        )

        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    return logger

