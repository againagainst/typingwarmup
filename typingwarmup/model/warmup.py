import math
import random
from pathlib import Path
from typing import Dict, List

import settings
from errors import NotAFileException


class WarmupModel:
    def __init__(self, excercise: Path, shuffle=False):
        exercise_text = read_exercise(excercise)
        if shuffle:
            exercise_text = shuffle_exercise(exercise_text)
        header = "\n" * settings.header_padding
        self.exercise = header + exercise_text
        self.position = settings.header_padding
        self.length = len(exercise_text)

        self.offset = 0
        self.offset_queue = self.init_offset_queue()
        self.exercise_length = len(exercise_text)

    def next(self) -> None:
        self.position += 1
        if self.exercise[self.position - 1] == "\n":
            self.offset = self.enqueue_offset(self.position)

    def page_before_cursor(self) -> str:
        return self.exercise[self.offset : self.position]

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

    def enqueue_offset(self, new_offset: int) -> int:
        self.offset_queue.append(new_offset)
        return self.offset_queue.pop(0)

    def skip_spaces(self) -> None:
        while self.cursor_char_equals(" "):
            self.next()

    def progress(self) -> Dict[str, int]:
        position = self.position - settings.header_padding
        percent = math.floor(position / self.length * 100) if self.length else 100
        return {"position": position, "total": self.length, "percent": percent}

    @staticmethod
    def init_offset_queue() -> List[int]:
        start = 1
        return list(range(start, settings.header_padding + start))


def read_exercise(excercise: Path) -> str:
    try:
        with open(excercise, "r") as fp:
            return fp.read()
    except OSError as oserr:
        raise NotAFileException(oserr.filename)


def shuffle_exercise(text: str) -> str:
    result = text.split("\n")
    random.shuffle(result)
    return "\n".join(result)
