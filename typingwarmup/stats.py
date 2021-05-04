from collections import defaultdict

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
        for exp, act_dict in self.data.items():
            errors_on_key = sum(act_dict.values())
            result += text.expected_key_stat.format(exp, errors_on_key)
            for act, count in act_dict.items():
                result += text.actual_key_stat.format(act, count)
            result += "\n"
        return result
