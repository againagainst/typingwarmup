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
        self.length = len(self.text)

    def done(self) -> bool:
        return self.position == self.length

    def current_char(self) -> str:
        return self.text[self.position]

    def current_char_is(self, input_char: str) -> bool:
        return self.current_char() == input_char

    def current_char_is_new_line(self) -> bool:
        return self.current_char_is("\n")

    def is_end_of_line(self) -> bool:
        return self.current_char_is("\t")

    def next_char(self, step=1) -> None:
        self.position += step


def read_exercise(ex_path: str, name: str) -> str:
    filename = os.path.join(ex_path, "exercises", name)
    with open(filename, "r") as fp:
        return fp.read()


def shuffle_exercise(text: str) -> str:
    result = text.split("\n\n")
    random.shuffle(result)
    return "\n\n".join(result)