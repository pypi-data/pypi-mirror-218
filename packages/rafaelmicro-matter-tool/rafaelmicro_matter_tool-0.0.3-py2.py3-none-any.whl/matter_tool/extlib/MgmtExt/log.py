import logging
import configparser
from pathlib import Path
DEFAULT_CONFIG_FILE_PATH = Path.home().joinpath(".cpc_cli.ini")
log_map = {}


class ExitOnExceptionHandler(logging.StreamHandler):
    def emit(self, record):
        # super().emit(record)
        if record.levelno in (logging.ERROR, logging.CRITICAL):
            raise SystemExit(-1)


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;21m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format_sty = "%(name).3s:%(levelname).1s %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format_sty + reset,
        logging.INFO: blue + format_sty + reset,
        logging.WARNING: yellow + format_sty + reset,
        logging.ERROR: red + format_sty + reset,
        logging.CRITICAL: bold_red + format_sty + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_logger(tag):
    global log_map
    return log_map[tag]


def set_logger(tag):
    config = read_config()
    logger = logging.getLogger(tag)
    if not logger.hasHandlers():
        ch = logging.StreamHandler()
        ch.setLevel(config['log']['log_level'])
        ch.setFormatter(CustomFormatter())
        logger.addHandler(ch)
        logger.addHandler(ExitOnExceptionHandler())
        logger.setLevel(config['log']['log_level'])
    return logger


def set_log_level(log_level, _config_path=DEFAULT_CONFIG_FILE_PATH):
    global log_map
    config = configparser.ConfigParser()
    config = read_config()
    config['log']['log_level'] = log_level
    with _config_path.open("w") as f:
        config.write(f)
    log_map = {
        "APP": set_logger("APP"),
        "CMD": set_logger("CMD"),
        "DM": set_logger("DM"),
    }


def read_config(_config_path=DEFAULT_CONFIG_FILE_PATH):
    config = configparser.ConfigParser()
    try:
        with _config_path.open("r") as f:
            config.read_file(f)
    except FileNotFoundError:
        config['log'] = {}
        config['log']['log_level'] = "INFO"
        with _config_path.open("w") as f:
            config.write(f)
    return config
