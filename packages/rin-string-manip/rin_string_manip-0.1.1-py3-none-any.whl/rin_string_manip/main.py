import os

import typer
import logging
from rin_string_manip.string_funcs import stair_case, prepend_number, append_date, remove_stop_words, coalesce_spaces
from rin_string_manip.log_error import error_log, get_yaml

app = typer.Typer()
logger: logging.Logger = logging.getLogger(__name__)


def pipe_func(*args, func, write_path):
    func = globals()[func]
    with open(write_path, "w") as write_file:
        write_file.write(func(*args))
    write_file.close()


@app.command()
@error_log
def apply_pipline(config_path: str = os.path.dirname(__file__) + "/config.yaml", file_path: str = "file.txt") -> None:
    pipeline = get_yaml(config_path)
    for func in pipeline["pipeline"]:
        with open(file_path, "r") as read_file:
            content = read_file.read()
        read_file.close()
        logger.info(f"Executing {func} function.")
        pipe_func(content, func=func, write_path=file_path)
        logger.debug(str(globals()[func]) + str(type(globals()[func])))
    logger.debug("Finished executing pipeline")


if __name__ == "__main__":
    app()
