import curses
import math
from typing import List, Optional
from contextlib import suppress


import settings
import text

from ui.base import UI, CursesScreen, Padding


class MenyUI(UI):
    def __init__(self, stdscr: CursesScreen, exercises: List[str]):
        super().__init__(stdscr)
        self.model = exercises
        self.cursor = 0
        self.page = 0
        self.padding = Padding(
            settings.meny_header_padding,
            settings.meny_right_padding,
            settings.meny_bottom_padding,
            settings.meny_left_padding,
        )

    def start(self) -> None:
        super().start()
        with suppress(Exception):
            curses.curs_set(0)

    def pick_name(self) -> Optional[str]:
        input_char = ""
        self.start()
        while True:
            self.render_model()
            input_char = self.input()
            if input_char in settings.meny_enter_key:
                return self.model[self.model_idx(page_idx=self.cursor)]
            elif input_char == settings.exit_key:
                return None
            elif input_char == settings.meny_up_key:
                self.up()
            elif input_char == settings.meny_down_key:
                self.down()
            elif input_char == settings.meny_page_up_key:
                self.up(page=True)
            elif input_char == settings.meny_page_down_key:
                self.down(page=True)
            else:
                pass

    def render_model(self) -> None:
        self.clear()
        self.resize()

        last_line = self.padding.top
        for idx, name in enumerate(self.meny_items()):
            if idx == self.cursor:
                self.stdscr.attron(curses.color_pair(UI.status_color_pair))
            item = text.menu_item(self.model_idx(idx), name)
            self.stdscr.addstr(idx + self.padding.top, self.padding.left, item)
            if idx == self.cursor:
                self.stdscr.attroff(curses.color_pair(UI.status_color_pair))
            last_line += 1
        if self.page != self.pages() - 1:
            self.stdscr.addstr(last_line, self.padding.left, text.ellipsis)

        status = text.status_bar()
        self.render_line_in_status_bar(status)
        self.stdscr.move(self.cursor + self.padding.top, self.padding.left)

    def up(self, page: bool = False) -> None:
        step = self.page_size() if page else 1

        if self.cursor - step < 0:
            if self.page - 1 < 0:
                self.page = self.pages() - 1
            else:
                self.page -= 1
            self.cursor = self.meny_length() - 1
        else:
            self.cursor -= step

    def down(self, page: bool = False) -> None:
        step = self.page_size() if page else 1

        if self.cursor + step >= self.meny_length():
            if self.page + 1 >= self.pages():
                self.page = 0
            else:
                self.page += 1
            self.cursor = 0
        else:
            self.cursor += 1

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
            - self.padding.top
            - self.padding.bottom
            - settings.status_bar_rows
        )

    def pages(self) -> int:
        return math.ceil(len(self.model) / self.page_size())
