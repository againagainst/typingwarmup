import math
import shelve
from copy import copy
from datetime import datetime
from itertools import groupby, starmap
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import text
from layout import Finger
from mistake import Mistake, key_expected, key_finger_expected


class Stats:
    def __init__(self, exercise_length: int, db_filename: Path):
        self.records: List[Mistake] = []
        self.symbols_typed = 0
        self.exercise_length = exercise_length
        self.db_filename = str(db_filename)

    def add_typed(self) -> None:
        self.symbols_typed += 1

    def add_mistake(self, actual: str, expected: str, is_eol: bool) -> None:
        key_actual = text.escape_key(actual)
        key_expected = text.EOL if is_eol else text.escape_key(expected)
        mistake = Mistake(key_actual, key_expected)
        self.records.append(mistake)

    def error_count(self) -> int:
        return len(self.records)

    def score(self) -> str:
        if self.symbols_typed == 0:
            return "unavailable"
        err_count = self.error_count()
        if err_count > self.symbols_typed:
            return "0/100"

        max_score = 100
        score = round((1 - math.log(err_count + 1, self.symbols_typed)) * max_score)
        return "{0}/{1}".format(score, max_score)

    def formatted(self) -> str:
        result = ""
        for finger, mistakes in _group_by_finger(self.records):
            mistakes_list = list(mistakes)
            result += text.finger_key_stat.format(finger, len(mistakes_list))
            for mistake, count in _group_by_mistake(mistakes_list):
                result += text.actual_expected_stat.format(
                    mistake.actual, mistake.expected, count
                )
            result += "\n"
        return result

    def persist(self) -> None:
        timestamp = datetime.now().strftime(r"%Y-%m-%dT%H:%M:%S")
        with shelve.open(self.db_filename) as db:
            db[timestamp] = copy(self.records)

    def load(self) -> Dict[str, List[Mistake]]:
        with shelve.open(self.db_filename) as db:
            return db


Mistakes = Iterable[Mistake]


def _group_by_finger(data: Mistakes) -> Iterable[Tuple[Finger, Mistakes]]:
    return groupby(sorted(data, key=key_finger_expected), key=key_finger_expected)


def _group_by_mistake(data: Mistakes) -> Iterable[Tuple[Mistake, int]]:
    return starmap(_count_in_group, groupby(sorted(data, key=key_expected)))


def _count_in_group(mistake: Mistake, group: Mistakes) -> Tuple[Mistake, int]:
    return (mistake, len(list(group)))
