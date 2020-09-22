import random
import os


def read_exercise(ex_path: str, name: str) -> str:
    filename = os.path.join(ex_path, "exercises", name)
    with open(filename, "r") as fp:
        return fp.read()


def shuffle_exercise(text: str) -> str:
    result = text.split("\n\n")
    random.shuffle(result)
    return "\n\n".join(result)
