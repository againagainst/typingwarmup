import json
import random
import click


def read_config(filename: str) -> dict:
    try:
        with open(filename, "r") as fp:
            return json.load(fp)
    except OSError:
        return dict()


def generate_text(
    aplhabet: str,
    repeat_letters: int,
    repeat_lines: int,
    shuffle_lines: bool,
) -> str:
    def repeat_letter(letter: str) -> str:
        return "".join(list(letter + " ") * repeat_letters)

    def repeat_line(line: str) -> str:
        return ((line + "\n") * repeat_lines)[:-1]

    letters = list(aplhabet)
    if shuffle_lines:
        random.shuffle(letters)
    lines = map(repeat_letter, letters)
    repeated_lines = map(repeat_line, lines)
    return "\n\n".join(repeated_lines)[:-1]


@click.command()
@click.option("--config", "filename", default="config.json")
def main(filename):
    config = read_config(filename)
    print(generate_text(**config))
