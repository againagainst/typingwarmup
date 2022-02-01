import os
from pathlib import Path
from typing import List, Optional

import settings
from errors import EmptyExcerciseException, InvalidExcercisesDir, NotAFileException


def read_exercise(excercise: Path) -> str:
    try:
        with open(excercise, "r") as fp:
            content = fp.read()
            if not content:
                raise EmptyExcerciseException(excercise)
            return content
    except OSError as oserr:
        raise NotAFileException(oserr.filename)


def list_files(ex_path: Path) -> List[str]:
    def create_time(f: os.DirEntry) -> float:
        return f.stat().st_ctime

    def file_name(f: os.DirEntry) -> str:
        return f.name

    try:
        exercises = os.scandir(ex_path)
        exercises = sorted(exercises, key=create_time, reverse=True)
        exercises = map(file_name, exercises)
        return list(exercises)
    except OSError:
        raise InvalidExcercisesDir(ex_path)


def exercise_dir() -> Path:
    return path(to=settings.exercise_dir_name)


def db_filename() -> str:
    return str(path(to=settings.db_filename))


def path(to: Optional[str] = None) -> Path:
    result = Path(__file__).resolve().parents[1]
    if to:
        result = result.joinpath(to)
    return result
