from typing import Callable
import logging
from functools import wraps
from os import environ

log_map = {
    "critical": logging.CRITICAL,
    "error": logging.ERROR,
    "warning": logging.WARNING,
    "info": logging.INFO,
    "debug": logging.DEBUG,
    "": logging.NOTSET
}


def log_error(func) -> Callable[[...], None]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> None:
        try:
            logging.basicConfig(filename='mpj1_errors.log', filemode='w',
                                encoding='utf-8', level=log_map[environ.get("LOG_LEVEL")],
                                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            func(*args, **kwargs)
        except FileNotFoundError as no_file:
            if "config.yaml" in no_file.filename:
                logging.error("Config file can't be found in the current directory. "
                              f"Create a config.yaml file or run command in directory "
                              f"containing config.yaml")
                return
            else:
                logging.error(f"{no_file.filename} can't be accessed. Check if it exists or if it has read "
                              f"permissions enabled.")
                return
        except AttributeError:
            logging.error("config.yaml can't be read. Is the config file empty?")
            return
        except KeyError as key_error:
            if key_error.args[0] in ['production', 'development', 'testing']:
                logging.error(f"{key_error.args[0]} doesn't exist. Check config file")
            return
        except Exception as e:
            logging.error(f"Encountered error. Traceback:\n{e.__traceback__}")

    return wrapper
