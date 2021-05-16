import curses
import os
import pathlib

from app import typing_warmup
import settings
import text


def main():
    current_dir = pathlib.Path(__file__).parent.absolute()
    ex_path = os.environ.get(settings.env_ex_path, current_dir)
    stats = curses.wrapper(typing_warmup, ex_path)
    if stats:
        print(text.goodbye.format(error_count=stats.error_count()))
        print(stats.formatted())
    else:
        print(text.bye)


if __name__ == "__main__":
    main()
