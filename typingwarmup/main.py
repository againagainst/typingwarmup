import click
import curses

import text
from ui import UI
import util


def curses_main(stdscr, exercise):
    k = 0

    ui = UI(stdscr)
    ui.start()

    # Loop where k is the last character pressed
    while k != curses.KEY_F10:
        ui.clear()
        ui.render_line_in_status_bar(text.status_bar)
        ui.render(exercise, UI.pair_bright, 0)
        # Refresh the screen
        ui.refresh()
        # Wait for next input
        k = ui.input()
    return 1


def typing_warmup(stdscr, exercise):
    next_char = 0
    idx = 0
    highlight_error = False
    errors = 0
    ui = UI(stdscr)
    ui.start()

    while idx < len(exercise) or next_char != curses.KEY_F10:
        if exercise[idx] == "\n":
            idx += 1
            continue

        ui.clear()
        ui.render_bright(exercise[:idx], nl=False)
        ui.render_highlighted(exercise[idx], error=highlight_error, nl=False)
        ui.render_dimmed(exercise[idx + 1 :], nl=True)

        next_char = ui.input()
        if next_char == exercise[idx]:
            idx += 1
            highlight_error = False
        else:
            highlight_error = True
            errors += 1
    return errors


@click.command()
@click.option("--random/--no-random", "-r", default=False)
@click.argument("name", default="1", nargs=1)
@click.argument("ex_path", envvar="WARMUP_EX_PATH", type=click.Path())
def main(random, name, ex_path) -> int:
    try:
        exercise = util.read_exercise(ex_path, name)
    except OSError:
        click.echo(text.err_not_found.format(name))
        return 1

    if random:
        exercise = util.shuffle_exercise(exercise)

    errcount = curses.wrapper(curses_main, exercise)
    click.echo(text.goodbye.format(errors=errcount))


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
