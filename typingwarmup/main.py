import curses

from app import typing_warmup
from errors import ApplicationException


def main() -> None:
    try:
        exit_msg = curses.wrapper(typing_warmup)
        print(exit_msg)
    except ApplicationException as error:
        print(error)


if __name__ == "__main__":
    main()
