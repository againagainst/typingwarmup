import curses

import settings
import text
from model import WarmupModel
from state import State
from stats import Stats

from ui.base import UI, CursesScreen


class WarmupUI(UI):
    def __init__(
        self, stdscr: CursesScreen, model: WarmupModel, state: State, stats: Stats
    ):
        super().__init__(stdscr)
        self.model = model
        self.state = state
        self.stats = stats
        self.page = 0

    def start(self) -> None:
        super().start()
        # Causes exception if export xterm=color
        # curses.curs_set(1)

    def resize(self) -> None:
        super().resize()
        self.model.resize(self.max_col)

    def render_model(self) -> None:
        self.clear()

        for row, row_text in enumerate(self.model.page_before_cursor()):
            for col, char in enumerate(row_text):
                self.render_bright(row, col, char)

        cursor_row = self.model.cursor_row
        cursor_col = self.model.cursor_col

        for row, row_text in enumerate(self.model.page_after_cursor(), cursor_row):
            if row > self.rows_awailable():
                break
            start_col = cursor_col + 1 if row == cursor_row else 0
            for col, char in enumerate(row_text, start_col):
                self.render_dimmed(row, col, char)

        status = text.status_bar(
            errors=self.stats.mistakes_count(),
            is_err_state=bool(self.state.wrong_input),
            progress=self.stats.progress(),
        )
        self.render_line_in_status_bar(status)

        if self.state.wrong_input:
            self.render_wrong_input(cursor_row, cursor_col, self.state.wrong_input)
        else:
            self.render_cursor(cursor_row, cursor_col)

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
        return self.max_row - settings.interface_rows

    def cols_awailable(self) -> int:
        return self.max_col - 1
