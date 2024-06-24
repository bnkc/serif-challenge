import gzip
import json
import logging
import time
from typing import Any, Callable, Generator

import ijson  # type: ignore


def read_json(file_path: str) -> Generator[Any, Any, None]:
    logging.info(msg=f"Reading JSON file: {file_path}")
    with gzip.open(file_path, "rt") as f:
        for record in ijson.items(f, "reporting_structure.item"):
            yield record


def write_json(file_path: str, data: Any) -> None:
    logging.info(msg=f"Writing JSON URLS to file: {file_path}")
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)


def log_time(func) -> Callable[..., Any]:
    """
    Time the execution of a function.
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        logging.info(msg=f"Starting execution of {func.__name__}")
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logging.info(
            msg=f"Finished execution of {func.__name__} in {elapsed_time:.2f} seconds"
        )
        return result

    return wrapper
