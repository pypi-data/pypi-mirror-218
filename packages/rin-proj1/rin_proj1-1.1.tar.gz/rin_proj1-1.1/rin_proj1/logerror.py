from typing import Callable
import logging
from functools import wraps
from os import environ
from rin_proj1.get_yaml import get_yaml

log_map = {
    "critical": logging.CRITICAL,
    "error": logging.ERROR,
    "warning": logging.WARNING,
    "info": logging.INFO,
    "debug": logging.DEBUG,
    "": logging.NOTSET
}


def error_branch(e):
    if isinstance(e, FileNotFoundError):
        if "config.yaml" in e.filename:
            logging.error("Config file can't be found in the current directory. "
                          f"Create a config.yaml file or run command in directory "
                          f"containing config.yaml")
        else:
            logging.error(f"{e.filename} can't be accessed. Check if it exists or if it has read "
                          f"permissions enabled.")
    elif isinstance(e, AttributeError):
        logging.error("config.yaml can't be read. Is the config file empty?")
    elif isinstance(e, KeyError):
        logging.error(f"KEY {e.args[0]} doesn't exist. Check config file")
    elif isinstance(e, TypeError):
        logging.error("Check values in csv/db file. TypeError encountered.")
    else:
        logging.error(f"Encountered error with message: {e}")


def log_error(func) -> Callable[[...], None]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> None:
        try:
            log_lvl = get_yaml("config.yaml").get("LOG_LEVEL", "")
        except Exception as e:
            error_branch(e)
            return

        try:
            logging.basicConfig(filename='mpj1_error.log', format='%(asctime)s - %(message)s',
                                encoding='utf-8', level=log_map[log_lvl])
            func(*args, **kwargs)
        except Exception as e:
            print("Ended abruptly. Check mpj1_error.log for more info.")
            error_branch(e)
            return
    return wrapper
