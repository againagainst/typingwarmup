import curses
from typing import Callable, List

import settings
import text
from model import WarmupModel
from state import State
from stats import Stats

from ui.base import UI, CursesScreen, Padding


class WarmupUI(UI):
    def __init__(
        self, stdscr: CursesScreen, model: WarmupModel, state: State, stats: Stats
    ):
        super().__init__(stdscr)
        self.model = model
        self.state = state
        self.stats = stats
        self.page = 0

        self.padding = Padding(
            settings.header_padding,
            settings.right_padding,
            settings.bottom_padding + settings.status_bar_rows,
            settings.left_padding,
        )

    def start(self) -> None:
        super().start()
        # Causes exception if export xterm=color
        # curses.curs_set(1)

    def resize(self) -> None:
        super().resize()
        self.model.resize(self.cols_awailable())

    def render_model(self) -> None:
        self.clear()

        # render before cursor
        start_row = self.padding.top
        text_before_cursor = list(self.model.page_before_cursor())
        self.render_text(text_before_cursor, start_row, self.render_bright)

        # render after cursor
        start_row = self.padding.top + len(text_before_cursor) - 1
        start_col = self.padding.left + len(text_before_cursor[-1]) + 1
        text_after_cursor = list(self.model.page_after_cursor())
        self.render_text(text_after_cursor, start_row, self.render_dimmed, start_col)

        # render status bar
        status = text.status_bar(
            errors=self.stats.mistakes_count(),
            is_err_state=bool(self.state.wrong_input),
            progress=self.stats.progress(),
        )
        self.render_line_in_status_bar(status)

        # render cursor
        cursor_row = self.model.cursor_row + self.padding.top
        cursor_col = self.model.cursor_col + self.padding.left
        if self.state.wrong_input:
            self.render_wrong_input(cursor_row, cursor_col, self.state.wrong_input)
        else:
            self.render_cursor(cursor_row, cursor_col)

    def render_text(
        self,
        text: List[str],
        start_row: int,
        render_method: Callable,
        first_row_col: int = 0,
    ) -> None:
        for row, row_text in enumerate(text, start_row):
            if row > self.rows_awailable():
                break
            # TODO: render cursor line separately
            if first_row_col and row == start_row:
                start_col = first_row_col
            else:
                start_col = self.padding.left
            for col, char in enumerate(row_text, start_col):
                render_method(row, col, char)

    def render_dimmed(self, row: int, col: int, char: str) -> None:
        self.stdscr.addch(row, col, char, curses.A_DIM)

    def render_bright(self, row: int, col: int, char: str) -> None:
        self.stdscr.addch(row, col, char, curses.A_BOLD)

    def render_cursor(self, row: int, col: int) -> None:
        char: str = self.model.cursor_char()
        self.stdscr.addch(row, col, char, curses.A_DIM)
        self.stdscr.move(row, col)

    def render_wrong_input(self, row: int, col: int, wrong_input: str) -> None:
        self.stdscr.attron(curses.color_pair(UI.error_color_pair))
        self.stdscr.addch(row, col, wrong_input)
        self.stdscr.move(row, col)
        self.stdscr.attroff(curses.color_pair(UI.error_color_pair))

    def rows_awailable(self) -> int:
        return self.max_row - self.padding.top - self.padding.bottom

    def cols_awailable(self) -> int:
        return self.max_col - self.padding.left - self.padding.right - 1
