import curses


def curses_menu(stdscr):
    k = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Loop where k is the last character pressed
    while k != curses.KEY_F10:

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Declaration of strings
        text = """asd asd asd asd asd asd asd asd asd asd 

kl; kl; kl; kl; kl; kl; kl; kl; kl; kl; 

fg fg fg fg fg fg fg fg fg fg fg fg fg 

jh jh jh jh jh jh jh jh jh jh jh jh jh
"""
        statusbarstr = "Press 'ESC' to exit"

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height - 1, 0, statusbarstr)
        stdscr.addstr(
            height - 1, len(statusbarstr), " " * (width - len(statusbarstr) - 1)
        )
        stdscr.attroff(curses.color_pair(3))

        # Rendering title
        stdscr.attron(curses.color_pair(1))
        render(stdscr, text, 0, 0)
        stdscr.attroff(curses.color_pair(1))

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()


def render(stdscr, text, start_y, start_x=0):
    for (i, line) in enumerate(text.split("\n")):
        stdscr.addstr(start_y + i, start_x, line)


def main():
    curses.wrapper(curses_menu)


if __name__ == "__main__":
    main()