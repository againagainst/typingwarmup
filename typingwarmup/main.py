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
        exit_msg = stats.exit_msg() if stats else text.default_exit_msg
        print(exit_msg)


if __name__ == "__main__":
    main()
