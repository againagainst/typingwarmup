import click
import curses

from app import typing_warmup
import text


@click.command()
@click.argument("ex_path", envvar="WARMUP_EX_PATH", type=click.Path())
def main(ex_path: click.Path):
    stats = curses.wrapper(typing_warmup, ex_path)
    if stats:
        click.echo(text.goodbye.format(error_count=stats.error_count()))
        click.echo(stats.formatted())
    else:
        click.echo(text.bye)


if __name__ == "__main__":
    main()
