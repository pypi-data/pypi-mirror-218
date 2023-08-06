import os

import typer
import logging
from rin_string_manip.string_funcs import stair_case, prepend_number, append_date, remove_stop_words, coalesce_spaces
from rin_string_manip.log_error import error_log, get_yaml

app = typer.Typer()
logger: logging.Logger = logging.getLogger(__name__)


@app.command()
@error_log
def apply_pipline(config_path: str = os.path.dirname(__file__) + "/config.yaml", file_path: str = "file.txt") -> None:
    pipeline = get_yaml(config_path)
    with open(file_path, "r") as read_file:
        content = read_file.read()
    read_file.close()

    for func in pipeline["pipeline"]:
        logger.info(f"Executing {func} function.")
        content = globals()[func](content)
        logger.debug(str(globals()[func]) + str(type(globals()[func])))

    with open("new_file.txt", "w") as write_file:
        write_file.write(content)
    write_file.close()
    logger.debug("Finished executing pipeline")


if __name__ == "__main__":
    app()
