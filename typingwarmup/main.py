import click
import curses

from app import typing_warmup
from model import Model
import text


@click.command()
@click.option("--random/--no-random", "-r", default=False)
@click.argument("name", default="1", nargs=1)
@click.argument("ex_path", envvar="WARMUP_EX_PATH", type=click.Path())
def main(random, name, ex_path) -> int:
    try:
        exercise = Model(ex_path, name, random)
    except OSError:
        click.echo(text.err_not_found.format(name))
        return 1

    errcount = curses.wrapper(typing_warmup, exercise)
    click.echo(text.goodbye.format(errors=errcount))
    return 0


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
