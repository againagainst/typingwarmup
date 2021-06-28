from collections import defaultdict, namedtuple
from typing import List, Tuple

import text
from layout import Finger, ISO as LayoutISO


TypingError = namedtuple("TypingError", ["expected", "actual"])


class Stats:
    def __init__(self):
        self.data = defaultdict(lambda: defaultdict(int))

    def add_error(self, actual: str, expected: str, is_eol: bool) -> None:
        key_actual = text.escape_key(actual)
        key_expected = text.EOL if is_eol else text.escape_key(expected)
        finger = LayoutISO.get(key_expected, Finger.other)
        self.data[finger][TypingError(key_expected, key_actual)] += 1

    def error_count(self) -> int:
        return sum(map(lambda d: sum(d.values()), self.data.values()))

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
        for finger, exp_act_dict in self.data.items():
            exp_act_list = sorted(
                exp_act_dict.items(), key=lambda k: k[1], reverse=True
            )
            errors_on_key = sum(map(lambda k: k[1], exp_act_list))
            result.append((finger.value, errors_on_key, exp_act_list))
        result.sort(key=lambda k: k[1], reverse=True)
        return result
