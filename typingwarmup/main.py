import os

import click
import curses

from app import typing_warmup
import text
import settings


def list_command(ex_path, folder="exercises", sep="\n") -> None:
    exercises = os.listdir(os.path.join(ex_path, folder))
    exercises.remove("gen.py")
    exercises.remove("config.json")
    click.echo(sep.join(exercises))


def default_command(name: str, ex_path: str, random: bool) -> None:
    try:
        stats = curses.wrapper(typing_warmup, name, ex_path, random)
    except OSError:
        click.echo(text.err_not_found.format(name))
    else:
        click.echo(text.goodbye.format(error_count=stats.error_count()))
        click.echo(stats.formatted())


@click.command()
@click.option("--random/--no-random", "-r", default=False)
@click.argument("name", default="default", nargs=1)
@click.argument("ex_path", envvar="WARMUP_EX_PATH", type=click.Path())
def main(random, name, ex_path) -> int:
    if name.lower() in settings.list_command:
        list_command(ex_path)
    else:
        default_command(name, ex_path, random)


if __name__ == "__main__":
    main()
