import random
from pathlib import Path


class Model:
    def __init__(self, excercise: Path, shuffle=False):
        exercise_text = read_exercise(excercise)
        if shuffle:
            exercise_text = shuffle_exercise(exercise_text)
        self.exercise = exercise_text

        self.row_limit = 0
        self.col_limit = 0
        self.position = 0

    def next(self) -> None:
        self.position += 1

    def page_before_cursor(self) -> str:
        return self.exercise[: self.position]

    def cursor_char(self) -> str:
        return self.exercise[self.position]

    def page_after_cursor(self) -> str:
        return self.exercise[self.position + 1 :]

    def cursor_char_equals(self, input_char: str) -> bool:
        return self.cursor_char() == input_char

    def is_cursor_at_the_end(self) -> bool:
        return self.position == len(self.exercise) - 1

    def is_cursor_at_eol(self) -> bool:
        return self.cursor_char_equals("\n")


def read_exercise(excercise: Path) -> str:
    with open(excercise, "r") as fp:
        return fp.read()


def shuffle_exercise(text: str) -> str:
    result = text.split("\n")
    random.shuffle(result)
    return "\n".join(result)
