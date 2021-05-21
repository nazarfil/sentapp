import logging


def setup_custom_logger(name):
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)8s] --- %(message)s (%(filename)s:%(lineno)s)",
                                  "%Y-%m-%d %H:%M:%S")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    logger.setLevel(logging.ERROR)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger


def setup_default_logger():
    name = "logger"
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)8s] --- %(message)s (%(filename)s:%(lineno)s)",
                                  "%Y-%m-%d %H:%M:%S")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    logger.setLevel(logging.ERROR)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger


def_logger = setup_default_logger()
