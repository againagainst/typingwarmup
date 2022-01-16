import random
from typing import Iterable, List, Tuple

import settings


class WarmupModel:
    def __init__(self, exercise_text: str, shuffle: bool = False):
        if shuffle:
            exercise_text = shuffle_exercise(exercise_text)
        self.length = len(exercise_text)

        self.exercise = exercise_text
        self.position = 0
        self.exercise_model: List[Tuple[int, int]] = []
        self.cursor_row = 0
        self.cursor_col = 0

    def next(self) -> None:
        self.position += 1
        self.cursor_col += 1
        if self.is_cursor_at_the_end_of_line():
            self.cursor_col = 0
            self.cursor_row += 1

    def cursor_char(self) -> str:
        return self.cursor_line()[self.cursor_col]

    def cursor_line(self) -> str:
        start, end = self.exercise_model[self.cursor_row]
        return self.exercise[start:end]

    def page_before_cursor(self, offset: int = 0) -> Iterable[str]:
        for start, end in self.exercise_model[offset : self.cursor_row]:
            yield self.exercise[start:end]
        yield self.cursor_line()[: self.cursor_col]

    def page_after_cursor(self) -> Iterable[str]:
        yield self.cursor_line()[self.cursor_col + 1 :]
        for start, end in self.exercise_model[self.cursor_row + 1 :]:
            yield self.exercise[start:end]

    def cursor_char_equals(self, input_char: str) -> bool:
        return self.cursor_char() == input_char

    def is_cursor_at_the_last_line(self) -> bool:
        return self.cursor_row == len(self.exercise_model)

    def is_cursor_at_the_end_of_line(self) -> bool:
        start, end = self.exercise_model[self.cursor_row]
        cursor_line_length = end - start
        return self.cursor_col == cursor_line_length

    def is_cursor_at_the_end(self) -> bool:
        return self.is_cursor_at_the_last_line() and self.is_cursor_at_the_end_of_line()

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
        self.restore_cursor_position()

    def restore_cursor_position(self) -> None:
        for row, (start, end) in enumerate(self.exercise_model):
            if end >= self.position >= start:
                self.cursor_row = row
                self.cursor_col = self.position - start
                break

    @staticmethod
    def wrap(line: str, to_size: int, offset: int) -> List[Tuple[int, int]]:
        start = 0
        result: List[Tuple[int, int]] = []
        while start < len(line):
            end = min(start + to_size, len(line))
            while line[end - 1] not in settings.end_of_line_symbols:
                end -= 1
                if end <= start:
                    end = min(start + to_size, len(line))
                    break
            result.append((start + offset, end + offset))
            start = end
        return result


def shuffle_exercise(text: str) -> str:
    result = text.split("\n")
    random.shuffle(result)
    return "\n".join(result)
