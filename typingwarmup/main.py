import curses

import text
from app import typing_warmup
from errors import ApplicationException


def main():
    try:
        stats = curses.wrapper(typing_warmup)
    except ApplicationException as error:
        print(error)
    else:
        print(text.exit_msg(stats))


if __name__ == "__main__":
    main()
