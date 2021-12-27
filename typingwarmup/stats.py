import math
from itertools import groupby
from typing import Any, Dict, List, Tuple

import settings
import text
from dataholders.finger import Finger
from dataholders.mistake import (
    Mistake,
    Mistakes,
    key_actual,
    key_expected,
    key_expected_combined,
    key_expected_finger,
)


class Stats:
    def __init__(self, exercise_length: int):
        self.mistakes: Mistakes = []
        self.symbols_typed = 0
        self.exercise_length = exercise_length

    def add_typed(self) -> None:
        self.symbols_typed += 1

    def add_mistake(self, actual: str, expected: str, is_eol: bool) -> None:
        key_actual = text.escape_key(actual)
        key_expected = text.EOL if is_eol else text.escape_key(expected)
        mistake = Mistake(key_actual, key_expected)
        self.mistakes.append(mistake)

    def exit_msg(self) -> str:
        score_formatted = (
            "{0}/{1}".format(self.score(), settings.max_score)
            if self.score() >= 0
            else text.unavailable
        )
        statistics = text.exit_msg.format(
            sybols_count=self.symbols_typed,
            error_count=self.mistakes_count(),
            score=score_formatted,
        )
        return statistics + "\n" + self.mistakes_formatted()

    def progress(self) -> Dict[str, int]:
        return {
            "position": self.symbols_typed,
            "total": self.exercise_length,
            "percent": math.floor(self.symbols_typed / self.exercise_length * 100),
        }

    def mistakes_count(self) -> int:
        return len(self.mistakes)

    def score(self) -> int:
        if self.symbols_typed == 0:
            return -1
        err_count = self.mistakes_count()
        if err_count > self.symbols_typed:
            return 0
        return round(
            (1 - math.log(err_count + 1, self.symbols_typed)) * settings.max_score
        )

    def mistakes_formatted(self) -> str:
        result = ""
        headers_only = self.mistakes_count() > 100
        compact = 100 > self.mistakes_count() > 30
        for finger, mistakes in _group_by_finger(self.mistakes):
            header_message = (
                text.finger_key_stat_message
                if headers_only
                else text.finger_key_stat_header
            )
            result += header_message.format(finger, len(mistakes))
            if headers_only:
                continue
            for expected, group in _group_by_expected(mistakes):
                actual = set("'{0}'".format(mistake.actual) for mistake in group)
                result += text.expected_simple_stat.format(
                    actual=", ".join(actual), expected=expected, times=len(group)
                )
                if compact and len(group) == 1:
                    break
            result += "\n"
        return result


def _group_by_finger(data: Mistakes) -> List[Tuple[Finger, Mistakes]]:
    gpd = [
        (finger, list(mistakes))
        for finger, mistakes in groupby(
            sorted(data, key=key_expected_combined),
            key=key_expected_finger,
        )
    ]
    return sorted(gpd, key=_by_group_size, reverse=True)


def _group_by_mistake(data: Mistakes) -> List[Tuple[Mistake, Mistakes]]:

    gpd = [
        (mistake, list(group))
        for mistake, group in groupby(sorted(data, key=key_actual))
    ]
    return sorted(gpd, key=_by_group_size_and_expected, reverse=True)


def _group_by_expected(data: Mistakes) -> List[Tuple[str, Mistakes]]:
    gpd = [
        (mistake, list(group))
        for mistake, group in groupby(sorted(data, key=key_expected), key=key_expected)
    ]
    return sorted(gpd, key=_by_group_size, reverse=True)


def _by_group_size_and_expected(group: Tuple[Mistake, Mistakes]):
    return (len(group[1]), group[0].expected)


def _by_group_size(group: Tuple[Any, Mistakes]):
    return len(group[1])
