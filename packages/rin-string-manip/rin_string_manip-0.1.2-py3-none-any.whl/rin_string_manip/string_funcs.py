import os.path
from datetime import datetime as dt
import yaml
import logging

logger: logging.Logger = logging.getLogger(__name__)


def stair_case(string: str) -> str:
    new_str: str = ""
    for i in range(len(string)):
        if i % 2:
            new_str += string[i].lower()
        else:
            new_str += string[i].upper()
    return new_str


def prepend_number(string: str) -> str:
    new_arr = []
    for idx, line in enumerate(string.split("\n")):
        new_arr.append(str(idx+1)+" "+line)
    return "\n".join(new_arr)


def append_date(string: str) -> str:
    return string+" "+str(dt.now())


def get_stop_words() -> list:
    with open(os.path.dirname(__file__)+"/stopwords.yaml", 'r') as file:
        stop_words: list = yaml.safe_load(file)["stopwords"]
    logging.debug(stop_words)
    sw_lower = [word.lower() for word in stop_words]
    return sw_lower


def remove_stop_words(string: str) -> str:
    stop_words = get_stop_words()
    new_str = []
    for word in string.split(' '):
        if word.lower() not in stop_words:
            new_str.append(word)
    return " ".join(new_str)


def coalesce_spaces(string: str) -> str:
    new_str = []
    for word in string.split(' '):
        if new_str and new_str[-1] == " " and word == " ":
            continue
        new_str.append(word)
    return ' '.join(new_str)
