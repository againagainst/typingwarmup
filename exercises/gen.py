import json
import click
from pprint import pprint


def read_config(filename: str) -> dict:
    try:
        with open(filename, "r") as fp:
            print("Config is:")
            config = json.load(fp)
            pprint(config)
            return config
    except OSError:
        return dict()


def generate_text(
    aplhabet: str, repeat_words: int, repeat_lines: int, newline: str
) -> str:
    def repeat_word(word: str) -> str:
        return " ".join([word] * repeat_words)

    def repeat_line(line: str) -> str:
        return ((line + newline) * repeat_lines)[:-1]

    words = aplhabet.split(" ")
    lines = map(repeat_word, words)
    repeated_lines = map(repeat_line, lines)
    return newline.join(repeated_lines)[:-1]


@click.command()
@click.option("--config", "filename", default="config.json")
def main(filename):
    config = read_config(filename)
    print()
    print(generate_text(**config))


if __name__ == "__main__":
    main()