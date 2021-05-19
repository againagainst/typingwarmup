import curses
import os
import pathlib

import settings
import text
from app import typing_warmup
from errors import ApplicationException


def main():
    current_dir = pathlib.Path(__file__).parent.absolute()
    ex_path = os.environ.get(settings.env_ex_path, current_dir)
    try:
        stats = curses.wrapper(typing_warmup, ex_path)
    except ApplicationException as error:
        print(error)
    else:
        print(text.exit_msg(stats))


if __name__ == "__main__":
    main()
