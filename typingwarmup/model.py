import random
import os
from functools import wraps
from pathlib import Path

import text
from stats import Stats


def render(method):
    @wraps(method)
    def wrapper(self, *args):
        self.is_to_render = True
        return method(self, *args)

    return wrapper


class Model:
    def __init__(self, ex_path: Path, name: str, shuffle=False):
        text = read_exercise(ex_path, name)
        if shuffle:
            text = shuffle_exercise(text)
        self.rows = [row + " " for row in text.split("\n")]

        self.is_to_render = True

        self.cursor_row = 0
        self.cursor_col = 0

        self.stats = Stats()
        self.wrong_input = None

    @render
    def next(self) -> None:
        if self.is_cursor_at_last_col():
            self.next_row()
        else:
            self.next_col()

    @render
    def next_col(self) -> None:
        self.cursor_col += 1

    @render
    def next_row(self) -> None:
        self.cursor_row += 1
        self.cursor_col = 0

    @render
    def add_error(self, wrong_input: str) -> None:
        expected = text.EOL if self.is_cursor_at_last_col() else self.cursor_char()
        actual = text.escape_key(wrong_input)
        self.stats.add_error(expected=expected, actual=actual)
        self.wrong_input = wrong_input

    @render
    def clear_wrong_input(self) -> None:
        self.wrong_input = None

    def cursor_char(self) -> str:
        return self.rows[self.cursor_row][self.cursor_col]

    def cursor_char_equals(self, input_char: str) -> bool:
        if self.is_cursor_at_last_col():
            return input_char in text.end_of_line_symbols
        return self.cursor_char() == input_char

    def last_row_idx(self) -> int:
        return len(self.rows) - 1

    def last_col_idx(self) -> int:
        return len(self.rows[self.cursor_row]) - 1

    def is_cursor_at_last_row(self) -> bool:
        return self.cursor_row >= self.last_row_idx()

    def is_cursor_at_last_col(self) -> bool:
        return self.cursor_col >= self.last_col_idx()

    def is_before_cursor(self, row: int, col: int) -> bool:
        return (row < self.cursor_row) or (
            row == self.cursor_row and col < self.cursor_col
        )

    def is_cursor_row_empty(self) -> bool:
        return self.rows[self.cursor_row] == " "


def read_exercise(ex_path: Path, name: str) -> str:
    filename = os.path.join(ex_path, name)
    with open(filename, "r") as fp:
        return fp.read()


def shuffle_exercise(text: str) -> str:
    result = text.split("\n\n")
    random.shuffle(result)
    return "\n\n".join(result)