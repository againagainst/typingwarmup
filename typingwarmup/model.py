import random
import os


class Model:
    def __init__(self, ex_path: str, name: str, shuffle=False):
        self.text = read_exercise(ex_path, name)
        # TODO: Temp hack replace with proper modeling
        self.text = self.text.replace("\n", "\t\n").replace("\t\n\t\n", "\t\n\n")
        if shuffle:
            self.text = shuffle_exercise(self.text)

        self.position = 0
        self.cursor_row = 0
        self.cursor_col = 0
        self.errors = 0
        self.is_error = False
        self.is_to_render = True

    def done(self) -> bool:
        return self.position == len(self.text)

    def current_char(self) -> str:
        return self.text[self.position]

    def current_char_is(self, input_char: str) -> bool:
        return self.current_char() == input_char

    def current_char_is_new_line(self) -> bool:
        return self.current_char_is("\n")

    def is_end_of_line(self) -> bool:
        return self.current_char_is("\t")

    def is_before_curent(self, row, col) -> bool:
        return (row < self.cursor_row) or (row == self.cursor_row and col < self.cursor_col)

    def next_row(self) -> None:
        self.cursor_row += 1
        self.cursor_col = 0
        self.position += 1
        self.is_to_render = True

    def next_col(self) -> None:
        self.cursor_col += 1
        self.position += 1
        self.is_to_render = True

    def add_error(self) -> None:
        self.errors += 1
        self.is_to_render = True


def read_exercise(ex_path: str, name: str) -> str:
    filename = os.path.join(ex_path, "exercises", name)
    with open(filename, "r") as fp:
        return fp.read()


def shuffle_exercise(text: str) -> str:
    result = text.split("\n\n")
    random.shuffle(result)
    return "\n\n".join(result)