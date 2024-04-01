import logging

from logger.handlers import file_handler


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    return logger
