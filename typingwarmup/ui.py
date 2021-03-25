import curses


class UI:
    color_grey = 10
    pair_bright = 1
    pair_highlighted = 2
    pair_dimmed = 3

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.cursor_row = 0
        self.cursor_col = 0
        self.max_row, self.max_col = stdscr.getmaxyx()

    def start(self) -> None:
        curses.noecho()
        curses.cbreak()

        # Start colors in curses
        curses.start_color()
        curses.init_color(UI.color_grey, 400, 400, 400)
        curses.init_pair(UI.pair_bright, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(UI.pair_highlighted, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(UI.pair_dimmed, UI.color_grey, curses.COLOR_BLACK)

        self.clear()
        self.stdscr.refresh()
        self.stdscr.keypad(True)

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

    def next_col(self):
        self.cursor_col += 1

    def render_bright(self, text: str):
        self.render(text, UI.pair_bright, self.cursor_row, self.cursor_col)

    def render_highlighted(self, text: str, error: bool):
        self.render(text, UI.pair_highlighted, self.cursor_row, self.cursor_col)

    def render_dimmed(self, text: str):
        self.render(text, UI.pair_dimmed, self.cursor_row, self.cursor_col)

    def render(self, text: str, color: int, row: int, col: int = 0):
        for (i, line) in enumerate(text.split("\n")):
            self.render_line(line, color, row + i, col)

    def render_line(self, text: str, color: int, row: int, col: int) -> None:
        self.stdscr.attron(curses.color_pair(color))
        self.stdscr.addstr(row, col, text)
        self.stdscr.attroff(curses.color_pair(color))

    def render_line_in_status_bar(self, text):
        self.stdscr.attron(curses.color_pair(UI.pair_highlighted))
        self.stdscr.addstr(self.max_row - 1, 0, text)
        filler = " " * (self.max_col - len(text) - 1)
        self.stdscr.addstr(self.max_row - 1, len(text), filler)
        self.stdscr.attroff(curses.color_pair(UI.pair_highlighted))

    def input(self) -> str:
        return self.stdscr.getch()