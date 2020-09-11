import click
import text
import random
import os


def read_exercise(ex_path: str, name: str) -> str:
    filename = os.path.join(ex_path, "exercises", name)
    with open(filename, "r") as fp:
        return fp.read()


def shuffle_exercise(text: str) -> str:
    result = text.split("\n\n")
    random.shuffle(result)
    return "\n\n".join(result)


def typing_warmup(exercise) -> None:
    idx = 0
    highlight_error = False
    errors = 0
    while idx < len(exercise):
        if exercise[idx] == "\n":
            idx += 1
            continue

        click.clear()
        click.echo(text.header)
        click.echo(
            click.style(exercise[:idx], fg="white")
            + click.style(
                exercise[idx], fg="black", bg="red" if highlight_error else "white"
            )
            + click.style(exercise[idx + 1 :], fg="black")
        )
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
def main(random, name, ex_path) -> None:
    try:
        exercise = read_exercise(ex_path, name)
        if random:
            exercise = shuffle_exercise(exercise)
        click.clear()
        errcount = typing_warmup(exercise)
    except KeyboardInterrupt:
        click.echo(text.goodbye)
    except OSError:
        click.echo("The excercise `{0}` is not found".format(name))
    else:
        click.echo(text.cheers.format(errors=errcount))


if __name__ == "__main__":
    main()
