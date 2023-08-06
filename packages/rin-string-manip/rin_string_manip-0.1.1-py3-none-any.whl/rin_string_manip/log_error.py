import logging
import logging.config
import yaml
import os
from typing import Callable
from functools import wraps


with open(os.path.dirname(__file__) + "/logging.yaml", "r") as f:
    log_cf = yaml.safe_load(f.read())
    logging.config.dictConfig(log_cf)
logger: logging.Logger = logging.getLogger(__name__)


def error_log(func) -> Callable[[...], None]:
    @wraps(func)
    def log_wrapper(*args, **kwargs) -> None:
        try:
            func(*args, **kwargs)
        except Exception as e:
            logging.error(e)
            return
        logger.debug("Finished execution")
    return log_wrapper


def get_yaml(path: str) -> dict:
    with open(path, "r") as file:
        config = yaml.safe_load(file.read())
    return config
