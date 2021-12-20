import curses
from typing import Tuple

import settings
import text
from model import WarmupModel
from state import State
from stats import Stats

from ui.base import UI


class WarmupUI(UI):
    def __init__(self, stdscr, model: WarmupModel, state: State, stats: Stats):
        super().__init__(stdscr)
        self.model = model
        self.state = state
        self.stats = stats
        self.page = 0

    def start(self) -> None:
        super().start()
        # Causes exception if export xterm=color
        # curses.curs_set(1)

    def render_model(self) -> None:
        self.clear()
        self.resize()

        row = 0
        col = 0
        for char in self.model.page_before_cursor():
            self.render_bright(row, col, char)
            row, col = self.move_render_cursor(row, col, char)

        cursor_row = row
        cursor_col = col
        row, col = self.move_render_cursor(row, col, self.model.cursor_char())

        for char in self.model.page_after_cursor():
            self.render_dimmed(row, col, char)
            row, col = self.move_render_cursor(row, col, char)
            if row > self.rows_awailable():
                break

        status = text.status_bar(
            errors=self.stats.error_count(),
            is_err_state=bool(self.state.wrong_input),
            progress=self.stats.progress(),
        )
        self.render_line_in_status_bar(status)

        if self.state.wrong_input:
            self.render_wrong_input(cursor_row, cursor_col, self.state.wrong_input)
        else:
            self.render_cursor(cursor_row, cursor_col, self.model.cursor_char())

    def render_dimmed(self, row: int, col: int, char: str) -> None:
        self.stdscr.addch(row, col, char, curses.A_DIM)

    def render_bright(self, row: int, col: int, char: str) -> None:
        self.stdscr.addch(row, col, char, curses.A_BOLD)

    def render_cursor(self, row: int, col: int, char: str) -> None:
        self.stdscr.addch(row, col, char, curses.A_DIM)
        self.stdscr.move(row, col)

    def render_wrong_input(self, row: int, col: int, wrong_input: str) -> None:
        self.stdscr.attron(curses.color_pair(UI.error_color_pair))
        self.stdscr.addch(row, col, wrong_input)
        self.stdscr.move(row, col)
        self.stdscr.attroff(curses.color_pair(UI.error_color_pair))

    def rows_awailable(self) -> int:
        return self.max_row - settings.interface_rows

    def cols_awailable(self) -> int:
        return self.max_col - 1

    def move_render_cursor(self, row: int, col: int, char: str) -> Tuple[int, int]:
        if char == "\n" or col == self.cols_awailable():
            return (row + 1, 0)
        else:
            return (row, col + 1)
