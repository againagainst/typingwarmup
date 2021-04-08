import click
import curses

import text
from ui import UI
import util


def typing_warmup(stdscr, exercise, exit_key="KEY_F(10)"):
    next_char = ""
    idx = 0
    highlight_error = False
    errors = 0

    ui = UI(stdscr)
    ui.start()
    ui.render_line_in_status_bar(text.status_bar(errors=errors))
    ui.render_dimmed(exercise)

    while idx < len(exercise) and next_char != exit_key:
        if exercise[idx] == "\n":
            idx += 1
            ui.next_row()
            continue

        ui.render_highlighted(exercise[idx], error=highlight_error)

        next_char = ui.input()
        if next_char == exercise[idx]:
            ui.render_bright(exercise[idx])
            idx += 1
            ui.next_col()
            highlight_error = False
        elif next_char == "KEY_RESIZE":
            pass  # fix later
        elif next_char == exit_key:
            pass
        else:
            highlight_error = True
            errors += 1
        ui.render_line_in_status_bar(text.status_bar(errors=errors))

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

    errcount = curses.wrapper(typing_warmup, exercise)
    click.echo(text.goodbye.format(errors=errcount))
    return 0


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
