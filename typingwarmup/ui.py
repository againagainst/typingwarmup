import curses
from typing import List

import text
import settings
from model import Model


class UI:
    status_color_pair = 1
    error_color_pair = 2

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.max_row, self.max_col = stdscr.getmaxyx()

    def start(self) -> None:
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

        # Start colors in curses
        curses.start_color()
        curses.init_pair(UI.status_color_pair, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(UI.error_color_pair, curses.COLOR_WHITE, curses.COLOR_RED)

        self.clear()

    def stop(self) -> None:
        self.clear()
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def clear(self) -> None:
        self.stdscr.clear()
        # self.stdscr.refresh()
        self.max_row, self.max_col = self.stdscr.getmaxyx()

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
        self.model = sorted(exercises)
        self.choice = 0

    def start(self) -> None:
        super().start()
        curses.curs_set(0)

    def render_model(self) -> None:
        self.clear()
        for idx, name in enumerate(self.list_of_names()):
            if idx == self.choice:
                self.stdscr.attron(curses.color_pair(UI.status_color_pair))
            self.stdscr.addstr(idx, 0, text.menu_item(idx, name))
            if idx == self.choice:
                self.stdscr.attroff(curses.color_pair(UI.status_color_pair))

        status = text.status_bar()
        self.render_line_in_status_bar(status)

    def up(self):
        if self.choice <= 0:
            self.choice = len(self.model) - 1
        else:
            self.choice -= 1

    def down(self):
        if self.choice >= len(self.model) - 1:
            self.choice = 0
        else:
            self.choice += 1

    def ex_name(self) -> str:
        return self.model[self.model_idx(page=0, page_idx=self.choice)]

    def list_of_names(self, page: int = 0) -> List[str]:
        start = page * self.page_size()
        end = start + self.page_size()
        return self.model[start:end]

    def model_idx(self, page: int, page_idx: int) -> int:
        return page * self.page_size() + page_idx

    def page_size(self) -> int:
        return min(settings.menu_page_limit, self.max_row)


class WarmupUI(UI):
    def __init__(self, stdscr, model: Model):
        super().__init__(stdscr)
        self.model = model

    def start(self) -> None:
        super().start()
        curses.curs_set(1)

    def render_model(self) -> None:
        if not self.model.is_to_render:
            return

        self.clear()

        for (row, line) in enumerate(self.model.text.split("\n")):
            for (col, char) in enumerate(line):
                if self.model.is_before_curent(row, col):
                    self.render_bright(row, col, char)
                else:
                    self.render_dimmed(row, col, char)

        status = text.status_bar(
            errors=self.model.stats.error_count(),
            is_err_state=bool(self.model.wrong_input),
        )
        self.render_line_in_status_bar(status)
        if self.model.wrong_input:
            self.render_wrong_input(self.model.wrong_input)
        else:
            self.render_cursor()
        self.model.is_to_render = False

    def render_dimmed(self, row: int, col: int, char: str) -> None:
        self.stdscr.addch(row, col, char, curses.A_DIM)

    def render_bright(self, row: int, col: int, char: str) -> None:
        self.stdscr.addch(row, col, char, curses.A_BOLD)

    def render_cursor(self) -> None:
        self.stdscr.addch(
            self.model.cursor_row,
            self.model.cursor_col,
            self.model.current_char(),
            curses.A_DIM,
        )
        self.stdscr.move(self.model.cursor_row, self.model.cursor_col)

    def render_wrong_input(self, wrong_input: str) -> None:
        self.stdscr.attron(curses.color_pair(UI.error_color_pair))
        self.stdscr.addch(self.model.cursor_row, self.model.cursor_col, wrong_input)
        self.stdscr.move(self.model.cursor_row, self.model.cursor_col)
        self.stdscr.attroff(curses.color_pair(UI.error_color_pair))
