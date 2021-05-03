from collections import defaultdict


class Stats:
    def __init__(self):
        self.data = defaultdict(lambda: defaultdict(int))

    def add_error(self, expected: str, actual: str) -> None:
        self.data[expected][actual] += 1

    def error_count(self) -> int:
        return sum(map(lambda d: sum(d.values()), self.data.values()))

    def formatted(self) -> str:
        result = ""
        for act, exp_dict in self.data.items():
            for exp, count in exp_dict.items():
                #                                  {2:02d}
                result += "'{1}' instead of '{0}': {2}\n".format(act, exp, count)
        return result
