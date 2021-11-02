import math
import shelve
from collections import defaultdict, namedtuple
from typing import List, Tuple, cast
from copy import copy
from pathlib import Path

import text
from layout import Finger, ISO as LayoutISO


TypingError = namedtuple("TypingError", ["expected", "actual"])


class Stats:
    def __init__(self, exercise_length: int, db_filename: Path):
        self.records = defaultdict(lambda: defaultdict(int))
        self.symbols_typed = 0
        self.exercise_length = exercise_length
        self.db_filename = str(db_filename)

    def add_typed(self) -> None:
        self.symbols_typed += 1

    def add_error(self, actual: str, expected: str, is_eol: bool) -> None:
        key_actual = text.escape_key(actual)
        key_expected = text.EOL if is_eol else text.escape_key(expected)
        finger = LayoutISO.get(key_expected, Finger.other)
        self.records[finger][TypingError(key_expected, key_actual)] += 1

    def error_count(self) -> int:
        return sum(map(lambda d: sum(d.values()), self.records.values()))

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
        for finger, errors_on_key, exp_act_dict in self.sorted():
            result += text.finger_key_stat.format(finger, errors_on_key)
            for keys, count in exp_act_dict:
                result += text.actual_expected_stat.format(
                    keys.actual, keys.expected, count
                )
            result += "\n"
        return result

    def sorted(self) -> List[Tuple[str, int, List[Tuple[TypingError, int]]]]:
        """
        {
            a: {b: 1, c: 2},
            d: {b: 1, c: 1}
        } -> [
            (a, 3, [(b, 1), (c, 2)]),
            (d, 2, [(b, 1), (c, 1)])
        ]
        """
        result = []
        for finger, exp_act_dict in self.records.items():
            exp_act_list = sorted(
                exp_act_dict.items(), key=lambda k: k[1], reverse=True
            )
            errors_on_key = sum(map(lambda k: k[1], exp_act_list))
            result.append((finger.value, errors_on_key, exp_act_list))
        result.sort(key=lambda k: k[1], reverse=True)
        return result

    def persist(self) -> None:
        current_records = cast(dict, copy(self.records))
        with shelve.open(self.db_filename) as db:
            previous_records = cast(dict, db.get("records", dict()))
            for finger, typing_error_count in previous_records:
                for typing_error, count in typing_error_count:
                    current_records[finger][typing_error] += count
            db["records"] = current_records

            previous_exercise_length = cast(int, db.get("exercise_length", 0))
            db["exercise_length"] = previous_exercise_length + self.exercise_length

    def load(self) -> None:
        with shelve.open(self.db_filename) as db:
            previous_records = cast(dict, db.get("records", dict()))
            for finger, typing_error_count in previous_records:
                for typing_error, count in typing_error_count:
                    self.records[finger][typing_error] = count

            self.exercise_length = cast(int, db.get("exercise_length", 0))
