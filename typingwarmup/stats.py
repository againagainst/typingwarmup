from collections import defaultdict
from typing import List, Tuple

import text


class Stats:
    def __init__(self):
        self.data = defaultdict(lambda: defaultdict(int))

    def add_error(self, expected: str, actual: str) -> None:
        self.data[expected][actual] += 1

    def error_count(self) -> int:
        return sum(map(lambda d: sum(d.values()), self.data.values()))

    def formatted(self) -> str:
        result = ""
        for exp, errors_on_key, act_dict in self.sorted():
            result += text.expected_key_stat.format(exp, errors_on_key)
            for act, count in act_dict:
                result += text.actual_key_stat.format(act, count)
            result += "\n"
        return result

    def sorted(self) -> List[Tuple[str, int, List[Tuple[str, int]]]]:
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
        for exp, act_dict in self.data.items():
            act_list = sorted(act_dict.items(), key=lambda k: k[1], reverse=True)
            errors_on_key = sum(map(lambda k: k[1], act_list))
            result.append((exp, errors_on_key, act_list))
        result.sort(key=lambda k: k[1], reverse=True)
        return result
