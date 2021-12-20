import math
from itertools import groupby, starmap
from typing import Dict, Iterable, List, Tuple

import text

from layout import Finger
from mistake import Mistake, key_expected, key_finger_expected


class Stats:
    def __init__(self, exercise_length: int):
        self.records: List[Mistake] = []
        self.symbols_typed = 0
        self.exercise_length = exercise_length

    def add_typed(self) -> None:
        self.symbols_typed += 1

    def add_mistake(self, actual: str, expected: str, is_eol: bool) -> None:
        key_actual = text.escape_key(actual)
        key_expected = text.EOL if is_eol else text.escape_key(expected)
        mistake = Mistake(key_actual, key_expected)
        self.records.append(mistake)

    def exit_msg(self) -> str:
        numbers = text.exit_msg.format(
            sybols_count=self.symbols_typed,
            error_count=self.error_count(),
            score=self.score(),
        )
        return numbers + "\n" + self.mistakes_formatted()

    def progress(self) -> Dict[str, int]:
        return {
            "position": self.symbols_typed,
            "total": self.exercise_length,
            "percent": math.floor(self.symbols_typed / self.exercise_length * 100),
        }

    def error_count(self) -> int:
        return len(self.records)

    def score(self) -> str:
        if self.symbols_typed == 0:
            return text.unavailable
        err_count = self.error_count()
        if err_count > self.symbols_typed:
            return "0/100"

        max_score = 100
        score = round((1 - math.log(err_count + 1, self.symbols_typed)) * max_score)
        return "{0}/{1}".format(score, max_score)

    def mistakes_formatted(self) -> str:
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


Mistakes = Iterable[Mistake]


def _group_by_finger(data: Mistakes) -> Iterable[Tuple[Finger, Mistakes]]:
    return groupby(sorted(data, key=key_finger_expected), key=key_finger_expected)


def _group_by_mistake(data: Mistakes) -> Iterable[Tuple[Mistake, int]]:
    return starmap(_count_in_group, groupby(sorted(data, key=key_expected)))


def _count_in_group(mistake: Mistake, group: Mistakes) -> Tuple[Mistake, int]:
    return (mistake, len(list(group)))
