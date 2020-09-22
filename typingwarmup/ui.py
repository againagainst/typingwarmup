import click


def start() -> None:
    clear()


def stop() -> None:
    clear()
    # print("ui stopped")


def clear() -> None:
    click.clear()


def display_bright(text: str, nl: bool = False) -> None:
    click.secho(text, fg="white", nl=nl)


def display_highlighted(text: str, error: bool, nl: bool = False) -> None:
    bg = "red" if error else "white"
    click.secho(text, fg="black", bg=bg, nl=nl)


def display_dimmed(text: str, nl: bool = False) -> None:
    click.secho(text, fg="black", nl=nl)


def display_text(text: str) -> None:
    click.echo(text)
