import click
import text

import ui
import util


def typing_warmup(exercise) -> None:
    idx = 0
    highlight_error = False
    errors = 0
    while idx < len(exercise):
        if exercise[idx] == "\n":
            idx += 1
            continue

        ui.clear()
        ui.display_text(text.header)
        ui.display_bright(exercise[:idx], nl=False)
        ui.display_highlighted(exercise[idx], error=highlight_error, nl=False)
        ui.display_dimmed(exercise[idx + 1 :], nl=True)

        next_char = click.getchar(echo=False)
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
        click.echo("The excercise `{0}` is not found".format(name))
        return 1

    if random:
        exercise = util.shuffle_exercise(exercise)
    try:
        ui.start()
        errcount = typing_warmup(exercise)
    except KeyboardInterrupt:
        ui.stop()
        click.echo(text.goodbye)
    else:
        ui.stop()
        click.echo(text.cheers.format(errors=errcount))
    return 0


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
