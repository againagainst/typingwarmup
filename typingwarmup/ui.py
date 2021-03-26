import curses


class UI:
    pair_status = 1

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.cursor_row = 0
        self.cursor_col = 0
        self.max_row, self.max_col = stdscr.getmaxyx()

    def start(self) -> None:
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

        # Start colors in curses
        curses.start_color()
        curses.init_pair(UI.pair_status, curses.COLOR_BLACK, curses.COLOR_WHITE)

        self.clear()
        self.stdscr.refresh()

    def stop(self) -> None:
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def clear(self) -> None:
        self.stdscr.clear()

    def refresh(self) -> None:
        self.stdscr.refresh()

    def next_row(self):
        self.cursor_row += 1
        self.cursor_col = 0

    def next_col(self):
        self.cursor_col += 1

    def render_bright(self, text: str):
        self.stdscr.addch(self.cursor_row, self.cursor_col, text, curses.A_BOLD)

    def render_highlighted(self, text: str, error: bool):
        self.stdscr.addch(self.cursor_row, self.cursor_col, text, curses.A_BLINK)
        self.stdscr.move(self.cursor_row, self.cursor_col)

    def render_dimmed(self, text: str):
        for (i, line) in enumerate(text.split("\n")):
            self.stdscr.addstr(i, 0, line, curses.A_DIM)

    def render_line_in_status_bar(self, text):
        self.stdscr.attron(curses.color_pair(UI.pair_status))
        self.stdscr.addstr(self.max_row - 1, 0, text)
        filler = " " * (self.max_col - len(text) - 1)
        self.stdscr.addstr(self.max_row - 1, len(text), filler)
        self.stdscr.attroff(curses.color_pair(UI.pair_status))

    def input(self) -> str:
        return self.stdscr.getkey()