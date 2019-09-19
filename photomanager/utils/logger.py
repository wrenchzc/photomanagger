import logging

logger = logging.getLogger("photomanager")


def __init_logger(logger):
    logger.setLevel(level=logging.INFO)
    handler = logging.FileHandler("photomanager.txt")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)

    logger.addHandler(handler)
    logger.addHandler(console)


__init_logger(logger)
