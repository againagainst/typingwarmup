import click
import curses


stdscr = curses.initscr()


def start() -> None:
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    # clear()
    return stdscr


def stop() -> None:
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()


def clear() -> None:
    stdscr.clear()


def display_header(text: str) -> None:
    stdscr.addstr(0, 0, text, curses.A_REVERSE)


def display_bright(text: str, nl: bool = False) -> None:
    click.secho(text, fg="white", nl=nl)


def display_highlighted(text: str, error: bool, nl: bool = False) -> None:
    bg = "red" if error else "white"
    click.secho(text, fg="black", bg=bg, nl=nl)


def display_dimmed(text: str, nl: bool = False) -> None:
    click.secho(text, fg="black", nl=nl)


def display_text(text: str) -> None:
    stdscr.addstr(0, 0, text)
    # click.echo(text)


def getkey() -> str:
    return stdscr.getkey()
