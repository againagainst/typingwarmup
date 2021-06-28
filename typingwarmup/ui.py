import curses
import math
from typing import List

import text
import settings
from errors import TerminalSizeException
from model import Model
from state import State
from stats import Stats


class UI:
    status_color_pair = 1
    error_color_pair = 2

    def __init__(self, stdscr):
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
            raise TerminalSizeException(self.max_row)

    def render_line_in_status_bar(self, text: str) -> None:
        self.stdscr.attron(curses.color_pair(UI.status_color_pair))
        self.stdscr.addstr(self.max_row - 1, 0, text)
        filler = " " * (self.max_col - len(text) - 1)
        self.stdscr.addstr(self.max_row - 1, len(text), filler)
        self.stdscr.attroff(curses.color_pair(UI.status_color_pair))

    def input(self) -> str:
        return self.stdscr.getkey()


class MenyUI(UI):
    def __init__(self, stdscr, exercises: List[str]):
        super().__init__(stdscr)
        self.model = exercises
        self.cursor = 0
        self.page = 0

    def start(self) -> None:
        super().start()
        curses.curs_set(0)

    def render_model(self) -> None:
        self.clear()
        self.resize()

        last_line = settings.meny_header_padding
        for idx, name in enumerate(self.meny_items()):
            if idx == self.cursor:
                self.stdscr.attron(curses.color_pair(UI.status_color_pair))
            item = text.menu_item(self.model_idx(idx), name)
            self.stdscr.addstr(idx + settings.meny_header_padding, 0, item)
            if idx == self.cursor:
                self.stdscr.attroff(curses.color_pair(UI.status_color_pair))
            last_line += 1
        if self.page != self.pages() - 1:
            self.stdscr.addstr(last_line, 0, "...")

        status = text.status_bar(errors=self.model_idx(self.cursor))
        self.render_line_in_status_bar(status)

    def up(self, page: bool = False):
        step = self.page_size() if page else 1

        if self.cursor - step < 0:
            if self.page - 1 < 0:
                self.page = self.pages() - 1
            else:
                self.page -= 1
            self.cursor = self.meny_length() - 1
        else:
            self.cursor -= step

    def down(self, page: bool = False):
        step = self.page_size() if page else 1

        if self.cursor + step >= self.meny_length():
            if self.page + 1 >= self.pages():
                self.page = 0
            else:
                self.page += 1
            self.cursor = 0
        else:
            self.cursor += 1

    def ex_name(self) -> str:
        return self.model[self.model_idx(page_idx=self.cursor)]

    def meny_items(self) -> List[str]:
        start = self.page * self.page_size()
        end = start + self.page_size()
        return self.model[start:end]

    def meny_length(self) -> int:
        return len(self.meny_items())

    def model_idx(self, page_idx: int) -> int:
        return self.page * self.page_size() + page_idx

    def page_size(self) -> int:
        """
        All available rows - header_padding, bottom_padding, and status bar.
        """
        return (
            self.max_row
            - settings.meny_header_padding
            - settings.meny_bottom_padding
            - settings.status_bar_rows
        )

    def pages(self) -> int:
        return math.ceil(len(self.model) / self.page_size())


class WarmupUI(UI):
    def __init__(self, stdscr, model: Model, state: State, stats: Stats):
        super().__init__(stdscr)
        self.model = model
        self.state = state
        self.stats = stats
        self.page = 0

    def start(self) -> None:
        super().start()
        curses.curs_set(1)

    def render_model(self) -> None:
        self.clear()
        self.resize()

        start = self.page * self.page_size()
        end = start + self.page_size()
        rows = enumerate(self.model.page(start, end), settings.header_padding)

        for (row, line) in rows:
            for (col, char) in enumerate(line):
                if self.model.is_before_cursor(row - settings.header_padding, col):
                    self.render_bright(row, col, char)
                else:
                    self.render_dimmed(row, col, char)

        status = text.status_bar(
            errors=self.stats.error_count(),
            is_err_state=bool(self.state.wrong_input),
        )
        self.render_line_in_status_bar(status)
        if self.state.wrong_input:
            self.render_wrong_input(self.state.wrong_input)
        else:
            self.render_cursor()

    def render_dimmed(self, row: int, col: int, char: str) -> None:
        self.stdscr.addch(row, col, char, curses.A_DIM)

    def render_bright(self, row: int, col: int, char: str) -> None:
        self.stdscr.addch(row, col, char, curses.A_BOLD)

    def render_cursor(self) -> None:
        self.stdscr.addch(
            self.ui_row(),
            self.ui_col(),
            self.model.cursor_char(),
            curses.A_DIM,
        )
        self.stdscr.move(self.ui_row(), self.model.cursor_col)

    def render_wrong_input(self, wrong_input: str) -> None:
        self.stdscr.attron(curses.color_pair(UI.error_color_pair))
        self.stdscr.addch(self.ui_row(), self.ui_col(), wrong_input)
        self.stdscr.move(self.ui_row(), self.ui_col())
        self.stdscr.attroff(curses.color_pair(UI.error_color_pair))

    def ui_row(self) -> int:
        return self.model.cursor_row + settings.header_padding

    def ui_col(self) -> int:
        return self.model.cursor_col

    def page_size(self) -> int:
        return (
            self.max_row
            - settings.header_padding
            - settings.bottom_padding
            - settings.status_bar_rows
        )

    def pages(self) -> int:
        return math.ceil(len(self.model.rows) / self.page_size())
