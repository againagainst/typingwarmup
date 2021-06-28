import random
import os
from pathlib import Path


class Model:
    def __init__(self, ex_path: Path, name: str, shuffle=False):
        exercise_text = read_exercise(ex_path, name)
        if shuffle:
            exercise_text = shuffle_exercise(exercise_text)
        self.rows = [row + " " for row in exercise_text.split("\n")]

        self.cursor_row = 0
        self.cursor_col = 0

    def next(self) -> None:
        if self.is_cursor_at_last_col():
            self.next_row()
        else:
            self.next_col()

    def next_col(self) -> None:
        self.cursor_col += 1

    def next_row(self) -> None:
        self.cursor_row += 1
        self.cursor_col = 0

    def cursor_char(self) -> str:
        return self.rows[self.cursor_row][self.cursor_col]

    def cursor_char_equals(self, input_char: str) -> bool:
        return self.cursor_char() == input_char

    def last_row_idx(self) -> int:
        return len(self.rows) - 1

    def last_col_idx(self) -> int:
        return len(self.rows[self.cursor_row]) - 1

    def is_cursor_at_last_row(self) -> bool:
        return self.cursor_row >= self.last_row_idx()

    def is_cursor_at_last_col(self) -> bool:
        return self.cursor_col >= self.last_col_idx()

    def is_cursor_at_the_end(self) -> bool:
        return self.is_cursor_at_last_row() and self.is_cursor_at_last_col()

    def is_before_cursor(self, row: int, col: int) -> bool:
        return (row < self.cursor_row) or (
            row == self.cursor_row and col < self.cursor_col
        )

    def is_cursor_row_empty(self) -> bool:
        return self.rows[self.cursor_row] == " "

    def skip_empty_rows(self) -> None:
        while self.is_cursor_row_empty():
            self.next_row()


def read_exercise(ex_path: Path, name: str) -> str:
    filename = os.path.join(ex_path, name)
    with open(filename, "r") as fp:
        return fp.read()


def shuffle_exercise(text: str) -> str:
    result = text.split("\n\n")
    random.shuffle(result)
    return "\n\n".join(result)