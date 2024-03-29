from collections import namedtuple
import curses
import settings
from errors import TerminalSizeRowsException, TerminalSizeColsException


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _curses import _CursesWindow

    CursesScreen = _CursesWindow
else:
    from typing import Any

    CursesScreen = Any

Padding = namedtuple("Padding", ["top", "right", "bottom", "left"])


class UI:
    status_color_pair = 1
    error_color_pair = 2

    def __init__(self, stdscr: CursesScreen):
        self.stdscr = stdscr

    def start(self) -> None:
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

        # Start colors in curses
        curses.start_color()
        curses.init_pair(UI.status_color_pair, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(UI.error_color_pair, curses.COLOR_WHITE, curses.COLOR_RED)

        self.clear()
        self.resize()

    def stop(self) -> None:
        self.clear()
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def clear(self) -> None:
        self.stdscr.clear()

    def resize(self) -> None:
        self.max_row, self.max_col = self.stdscr.getmaxyx()
        if self.max_row < settings.minimum_rows:
            raise TerminalSizeRowsException(self.max_row)
        if self.max_col < settings.minimum_cols:
            raise TerminalSizeColsException(self.max_col)

    def render_line_in_status_bar(self, text: str) -> None:
        self.stdscr.attron(curses.color_pair(UI.status_color_pair))
        self.stdscr.addstr(self.max_row - 1, 0, text)
        filler = " " * (self.max_col - len(text) - 1)
        self.stdscr.addstr(self.max_row - 1, len(text), filler)
        self.stdscr.attroff(curses.color_pair(UI.status_color_pair))

    def input(self) -> str:
        return self.stdscr.getkey()
