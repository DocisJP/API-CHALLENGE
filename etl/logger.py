import logging
import colorlog

def setup_logger():
    """Set up a colored logger for more visually appealing output."""
    logger = colorlog.getLogger()
    logger.setLevel(logging.DEBUG)

    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(levelname)-8s%(reset)s %(blue)s%(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    ))

    logger.addHandler(handler)
    return logger

logger = setup_logger()