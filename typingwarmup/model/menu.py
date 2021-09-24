import os
from pathlib import Path
from typing import List

from errors import InvalidExcercisesDir


class MenuModel:
    @staticmethod
    def read_exercises(ex_path: Path) -> List[str]:
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
