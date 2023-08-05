import time
from datetime import datetime
import configparser
from pathlib import Path
DEFAULT_CONFIG_FILE_PATH = Path.home().joinpath(".cpc_cli.ini")


def start_timmer(tag, _config_path=DEFAULT_CONFIG_FILE_PATH):
    config = configparser.ConfigParser()
    with _config_path.open("r") as f:
        config.read_file(f)
    try:
        config["time"]
    except:
        config["time"] = {}
    config["time"][tag+"_timmer"] = str(time.time())
    with _config_path.open("w") as f:
        config.write(f)
    return config


def stop_timmer(tag, _config_path=DEFAULT_CONFIG_FILE_PATH):
    config = configparser.ConfigParser()
    with _config_path.open("r") as f:
        config.read_file(f)
    return time.time() - float(config["time"][tag+"_timmer"])
