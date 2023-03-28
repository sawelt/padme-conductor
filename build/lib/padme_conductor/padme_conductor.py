import atexit
import json
import logging
import os
from pathlib import Path
from typing import Any, Callable, Dict, List, Union

import padme_conductor.constants as constants
from padme_conductor.Query import Query
from padme_conductor.Separation import Separation
from padme_conductor.TrainLogger import TrainLogger


# Helpers
# ________________
def _run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)

    wrapper.has_run = False
    return wrapper


@_run_once
def _increment_station_once_per_run():
    if not constants._save_metadata_path.exists():
        _create_save_metadata()

    with open(constants._save_metadata_path, "r") as f:
        save_metadata = json.load(f)

    save_metadata["runs"] += 1

    station_id = get_environment_vars([constants._STATION_ID])[constants._STATION_ID]
    save_metadata["visited_stations"].append(station_id)

    with open(constants._save_metadata_path, "w") as f:
        json.dump(save_metadata, f)


def _convert_to_path(file_path: Union[str, Path]):
    if isinstance(file_path, str):
        file_path = Path(file_path)
        return file_path
    else:
        return file_path


def is_first_execution(separate_by: Separation = Separation.NO_SEPARATION):
    if separate_by == Separation.NO_SEPARATION:
        if _get_save_metadata()["runs"] == 0:
            return True
        return False
    elif separate_by == Separation.STATION:
        station_name = get_environment_vars(["STATION_ID"])["STATION_ID"]
        visited = _get_save_metadata()["visited_stations"]
        if station_name in visited:
            return False
        return True
    elif separate_by == Separation.RUN:
        return True


# Environment Variables
# ________________
def get_environment_vars(keys: List[str]) -> Dict[str, str]:
    env_dict = {}
    for key in keys:
        val = os.getenv(key)
        str_val = str(val)
        env_dict[key] = str_val

    return env_dict


# Query
# ________________
Queries = Union[Query, List[Query]]
QueryResult = Any

# if len(default_queries) == 0:"no default queries registered and station name does not match any query."
# if len(default_queries) > 1: "There are more than one default queries registered, and only the first will be condiserd.\n"


def query(queries: Queries, station_name: Union[str, None] = None) -> QueryResult:
    # TODO: maybe verify that the parameters are correct? probably in each plugin?
    # TODO create test case for each case
    # Wrap in list if single Query
    if isinstance(queries, Query):
        queries = [queries]

    # Set station_name to default if there is no query for it
    reg_station_names = [q.station_name for q in queries]
    if station_name not in reg_station_names:
        station_name = None

    # Find query for the station_name or take the first default query
    for query in queries:
        if query.station_name == station_name:
            return query.plugin._query(query.query)

    raise Exception("Query Not Found")


# TODO: maybe return a connection in case it makes sense
# def get_connection(plugin: DatabasePlugin, username, password):
#     return plugin.connect(username, password)

# Save Result
# ________________


@_run_once
def _create_save_metadata():
    if not constants._save_metadata_path.exists():
        constants._save_dir.mkdir(parents=True, exist_ok=True)
        with open(constants._save_metadata_path, "w") as f:
            json.dump(constants._SAVE_METADATA_DEFAULT, f)


def _get_save_metadata():
    if not constants._save_metadata_path.exists():
        _create_save_metadata()

    with open(constants._save_metadata_path, "r+") as f:
        save_metadata = json.load(f)

    return save_metadata


def get_save_path(
    save_path: Union[str, Path, None] = None,
    separate_by: Separation = Separation.NO_SEPARATION,
):
    if save_path == None:
        save_path = constants._save_dir
    save_path = _convert_to_path(save_path)

    # append station number if separating
    if separate_by == Separation.STATION:
        station_name = get_environment_vars(["STATION_ID"])["STATION_ID"]
        save_path = save_path / station_name
    elif separate_by == Separation.RUN:
        run_id = int(_get_save_metadata()["runs"])
        save_path = save_path / str(run_id)

    return save_path


def save(
    content: str,
    file_name: str,
    save_path: Union[str, Path, None] = None,
    separate_by: Separation = Separation.NO_SEPARATION,
    append=False,
):
    save_path = get_save_path(save_path, separate_by)
    # create a save folder
    save_path.mkdir(parents=True, exist_ok=True)

    # Write or append content to file
    file_path = save_path / file_name
    write_mode = "a" if append else "w"
    with open(file_path, write_mode) as f:
        f.write(content)


# Retrieve previous Result
# ________________
def get_prev_save_path(
    separate_by: Separation = Separation.NO_SEPARATION,
    save_path: Union[str, Path, None] = None,
):
    if save_path == None:
        save_path = constants._save_dir
    save_path = _convert_to_path(save_path)

    # append station number if separating
    if separate_by == Separation.STATION:
        station_name = get_environment_vars(["STATION_ID"])["STATION_ID"]
        save_path = save_path / station_name
    elif separate_by == Separation.RUN:
        run_id = _get_save_metadata()["runs"] - 1
        save_path = save_path / str(run_id)

    return save_path


def retrieve_prev_result(
    file_name: str,
    save_path: Union[str, Path, None] = None,
    separate_by: Separation = Separation.NO_SEPARATION,
):
    save_path = get_prev_save_path(separate_by=separate_by, save_path=save_path)

    # read and return file content
    prev_result_file = save_path / file_name

    if not save_path.is_dir() or not prev_result_file.exists():
        log_warning(
            "Previous Result File could not be found. (Consider that the results might be saved for each station separately)"
        )
        return None

    with open(prev_result_file) as f:
        content = f.read()

    return content


# Execution
# ________________
def execute_analysis(analysis: Callable, *args, **kwargs):
    return analysis(*args, **kwargs)


# Logging
# ________________
def log(msg: object, *args: object, extra=None):
    log_info(msg, *args, extra=extra)


def log_critical(msg: object, *args: object, extra=None):
    logger.log(logging.CRITICAL, msg, *args, extra=extra)


def log_error(msg: object, *args: object, extra=None):
    logger.log(logging.ERROR, msg, *args, extra=extra)


def log_warning(msg: object, *args: object, extra=None):
    logger.log(logging.WARNING, msg, *args, extra=extra)


def log_info(msg: object, *args: object, extra=None):
    logger.log(logging.INFO, msg, *args, extra=extra)


def log_debug(msg: object, *args: object, extra=None):
    logger.log(logging.DEBUG, msg, *args, extra=extra)


def log_ml_model(message):
    print(message)


logger = TrainLogger()

atexit.register(_increment_station_once_per_run)
