from pathlib import Path

import settings


class ApplicationException(Exception):
    pass


class TerminalSizeException(ApplicationException):
    def __init__(self, current_rows: int, *args: object) -> None:
        super().__init__(*args)
        self.current_rows = current_rows

    def __str__(self) -> str:
        return "Invalid terminal size. At least {0} rows required, got {1}.".format(
            settings.minimum_rows, self.current_rows
        )


class InvalidExcercisesDir(ApplicationException):
    def __init__(self, path: Path, *args: object) -> None:
        super().__init__(*args)
        self.path = path

    def __str__(self) -> str:
        return (
            "Invalid path to the excercises directory: {0}\n"
            + "Check {1} env variable."
        ).format(self.path, settings.env_ex_path)
