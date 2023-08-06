import os

import typer
import logging
from rin_string_manip.string_funcs import stair_case, prepend_number, append_date, remove_stop_words, coalesce_spaces
from rin_string_manip.log_error import error_log, get_yaml

app = typer.Typer()
logger: logging.Logger = logging.getLogger(__name__)


@app.command()
@error_log
def call_stair_case(string: str) -> None:
    """converts letters to upper/lower case alternatively.
    Takes string input and prints modified string (returns None)"""
    print(stair_case(string))


@app.command()
@error_log
def call_prepend_number(string: str) -> None:
    """
    Adds/prepends a number (line number) to the start of each line.
    Takes string input and prints string (returns None)
    """
    print(prepend_number(string))


@app.command()
@error_log
def call_append_date(string: str) -> None:
    """
    Adds/suffixes current date+time to end of string.
    Takes string input and prints modified string (returns None)
    """
    print(append_date(string))


@app.command()
@error_log
def call_remove_sw(string: str) -> None:
    """
    Removes stop words from string.
    Takes string input and prints modified string (returns None).
    Stop words are taken from stopword.yaml, ensure file exists.
    """
    print(remove_stop_words(string))


@app.command()
@error_log
def call_coalesce_spaces(string: str) -> None:
    print(coalesce_spaces(string))


def pipe_func(*args, func, write_path):
    func = globals()[func]
    with open(write_path, "w") as write_file:
        write_file.write(func(*args))
    write_file.close()
    # return func(*args)


@app.command()
@error_log
def apply_pipline(config_path: str = os.path.dirname(__file__) + "/config.yaml", file_path: str = "file.txt") -> None:
    pipeline = get_yaml(config_path)
    for func in pipeline["pipeline"]:
        with open(file_path, "r") as read_file:
            content = read_file.read()
        read_file.close()
        pipe_func(content, func=func, write_path=file_path)
        logger.debug(str(globals()[func]) + str(type(globals()[func])))
    logger.debug("Finished executing pipeline")


if __name__ == "__main__":
    app()
