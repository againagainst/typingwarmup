import shelve
from datetime import datetime
from pathlib import Path
from typing import Optional


import settings
from errors import NotAFileException
from stats import Stats


def read_exercise(excercise: Path) -> str:
    try:
        with open(excercise, "r") as fp:
            return fp.read()
    except OSError as oserr:
        raise NotAFileException(oserr.filename)


def exercise_dir() -> Path:
    return path(to=settings.exercise_dir_name)


def db_filename() -> str:
    return str(path(to=settings.db_filename))


def path(to: Optional[str] = None) -> Path:
    result = Path(__file__).resolve().parents[1]
    if to:
        result = result.joinpath(to)
    return result


def persist(stats: Stats) -> None:
    if not stats.records:
        return

    timestamp = datetime.now().strftime(r"%Y-%m-%dT%H:%M:%S")
    with shelve.open(db_filename()) as db:
        db[timestamp] = stats.records


def load():
    with shelve.open(db_filename()) as db:
        return db
