import math
from typing import Dict

import settings
import statsfmt
import text
from dataholders.mistake import Mistake, Mistakes


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
        is_headers_only = settings.is_headers_only(self.mistakes_count())
        is_compact = settings.is_compact(self.mistakes_count())
        skip_if_less = settings.skip_if_less(self.mistakes_count())
        mistakes_formatted = statsfmt.mistakes_formatted(
            self.mistakes, is_headers_only, is_compact, skip_if_less
        )
        statistics = text.exit_msg_stats.format(
            sybols_count=self.symbols_typed,
            error_count=self.mistakes_count(),
            score=self.score_formatted(),
        )
        return "{0}\n{1}\n{2}".format(text.exit_msg, mistakes_formatted, statistics)

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

    def score_formatted(self) -> str:
        if self.score() >= 0:
            return "{0}/{1}".format(self.score(), settings.max_score)
        else:
            return text.unavailable
