import curses
import text
from app import typing_warmup
from errors import ApplicationException


def main() -> None:
    try:
        exit_msg = curses.wrapper(typing_warmup)
        print(exit_msg)
    except ApplicationException as error:
        print(error)
    except KeyboardInterrupt:
        print(text.default_exit_msg)


if __name__ == "__main__":
    main()
