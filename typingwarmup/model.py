import random
from typing import Iterable, List, Tuple

import settings


class WarmupModel:
    def __init__(self, exercise_text: str, shuffle: bool = False):
        self.exercise = exercise_text
        if shuffle:
            self.exercise = shuffle_exercise(self.exercise)
        self.position = 0
        self.exercise_model: List[Tuple[int, int]] = []
        self.rows = 0
        self.cursor_row = 0
        self.cursor_col = 0

    def next(self) -> None:
        self.position += 1
        self.cursor_col += 1
        if self.is_cursor_at_the_end_of_line():
            self.cursor_col = 0
            self.cursor_row += 1

    def cursor_char(self) -> str:
        return self.exercise[self.position]

    def cursor_line(self) -> str:
        start, end = self.exercise_model[self.cursor_row]
        return self.exercise[start:end]

    def lines_before_cursor(self, offset: int = 0) -> Iterable[str]:
        for start, end in self.exercise_model[offset : self.cursor_row]:
            yield self.exercise[start:end]
        full_cursor_line = self.cursor_line()
        yield full_cursor_line[: self.cursor_col]

    def lines_after_cursor(self) -> Iterable[str]:
        full_cursor_line = self.cursor_line()
        yield full_cursor_line[self.cursor_col + 1 :]
        for start, end in self.exercise_model[self.cursor_row + 1 :]:
            yield self.exercise[start:end]

    def cursor_char_equals(self, input_char: str) -> bool:
        return self.cursor_char() == input_char

    def is_cursor_at_the_end_of_line(self) -> bool:
        start, end = self.exercise_model[self.cursor_row]
        cursor_line_length = end - start
        return self.cursor_col == cursor_line_length

    def is_cursor_at_the_end(self) -> bool:
        return self.position >= len(self.exercise)

    def is_cursor_at_eol(self) -> bool:
        return self.cursor_char_equals("\n")

    def skip_spaces(self) -> None:
        while self.cursor_char_equals(" "):
            self.next()

    def resize(self, size: int) -> None:
        self.exercise_model.clear()
        unwrapped_rows = self.exercise.split("\n")
        offset = 0
        for line in unwrapped_rows:
            line_with_eol = line + "\n"
            wrapped_idx = self.wrap(line_with_eol, size, offset)
            self.exercise_model.extend(wrapped_idx)
            _, offset = self.exercise_model[-1]

        last_start, last_end = self.exercise_model[-1]
        self.exercise_model[-1] = (last_start, last_end - 1)
        self.rows = len(self.exercise_model)
        self.restore_cursor_position()

    def restore_cursor_position(self) -> None:
        for row, (start, end) in enumerate(self.exercise_model):
            if end > self.position >= start:
                self.cursor_row = row
                self.cursor_col = self.position - start
                break

    @staticmethod
    def wrap(line: str, to_size: int, offset: int) -> List[Tuple[int, int]]:
        wrap_symbols = settings.end_of_line_symbols
        total = len(line)
        start = 0
        result: List[Tuple[int, int]] = []
        while start < total:
            end = min(start + to_size, total)
            while line[end - 1] not in wrap_symbols and total - start > to_size:
                end -= 1
                if end <= start:
                    end = min(start + to_size, total)
                    break
            result.append((start + offset, end + offset))
            start = end
        return result


def shuffle_exercise(text: str) -> str:
    result = text.split("\n")
    random.shuffle(result)
    return "\n".join(result)
