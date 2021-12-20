from pathlib import Path
from typing import Optional

import settings
from errors import EmptyExcerciseException, NotAFileException


def read_exercise(excercise: Path) -> str:
    try:
        with open(excercise, "r") as fp:
            content = fp.read()
            if not content:
                raise EmptyExcerciseException(excercise)
            return content
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
