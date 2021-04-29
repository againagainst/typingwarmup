import curses

import text
from model import Model


class UI:
    pair_status = 1

    def __init__(self, stdscr, model: Model):
        self.stdscr = stdscr
        self.max_row, self.max_col = stdscr.getmaxyx()
        self.model = model

    def start(self) -> None:
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

        # Start colors in curses
        curses.start_color()
        curses.init_pair(UI.pair_status, curses.COLOR_BLACK, curses.COLOR_WHITE)

        self.clear()
        self.stdscr.refresh()

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
            errors=self.model.errors, is_err_state=self.model.is_error
        )
        self.render_line_in_status_bar(status)
        self.render_cursor()
        self.model.is_to_render = False

    def render_dimmed(self, row, col, char) -> None:
        self.stdscr.addch(row, col, char, curses.A_DIM)

    def render_bright(self, row, col, char) -> None:
        self.stdscr.addch(row, col, char, curses.A_BOLD)

    def render_cursor(self) -> None:
        self.stdscr.addch(
            self.model.cursor_row,
            self.model.cursor_col,
            self.model.current_char(),
            curses.A_BLINK,
        )
        self.stdscr.move(self.model.cursor_row, self.model.cursor_col)

    def render_line_in_status_bar(self, text) -> None:
        self.stdscr.attron(curses.color_pair(UI.pair_status))
        self.stdscr.addstr(self.max_row - 1, 0, text)
        filler = " " * (self.max_col - len(text) - 1)
        self.stdscr.addstr(self.max_row - 1, len(text), filler)
        self.stdscr.attroff(curses.color_pair(UI.pair_status))

    def stop(self) -> None:
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def clear(self) -> None:
        self.stdscr.clear()
        self.max_row, self.max_col = self.stdscr.getmaxyx()

    def refresh(self) -> None:
        self.stdscr.refresh()

    def input(self) -> str:
        return self.stdscr.getkey()