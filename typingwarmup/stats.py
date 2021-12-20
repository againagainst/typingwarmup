import math
from itertools import groupby, starmap
from typing import Dict, Iterable, List, Tuple

import text
import settings
from dataholders.finger import Finger
from dataholders.mistake import Mistake, key_expected, key_finger_expected


class Stats:
    def __init__(self, exercise_length: int):
        self.mistakes: List[Mistake] = []
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
        for finger, mistakes in _group_by_finger(self.mistakes):
            mistakes_list = list(mistakes)
            result += text.finger_key_stat.format(finger, len(mistakes_list))
            for mistake, count in _count_mistakes(mistakes_list):
                result += text.actual_expected_stat.format(
                    mistake.actual, mistake.expected, count
                )
            result += "\n"
        return result


Mistakes = Iterable[Mistake]


def _group_by_finger(data: Mistakes) -> Iterable[Tuple[Finger, Mistakes]]:
    return groupby(sorted(data, key=key_finger_expected), key=key_finger_expected)


def _count_mistakes(data: Mistakes) -> Iterable[Tuple[Mistake, int]]:
    return starmap(_count_in_group, groupby(sorted(data, key=key_expected)))


def _count_in_group(mistake: Mistake, group: Mistakes) -> Tuple[Mistake, int]:
    return (mistake, len(list(group)))
