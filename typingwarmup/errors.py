from pathlib import Path
from typing import Any

import settings


class ApplicationException(Exception):
    pass


class TerminalSizeRowsException(ApplicationException):
    def __init__(self, current_rows: int, *args: object) -> None:
        super().__init__(*args)
        self.current_rows = current_rows

    def __str__(self) -> str:
        return "Invalid terminal size. At least {0} rows required, got {1}.".format(
            settings.minimum_rows, self.current_rows
        )


class TerminalSizeColsException(ApplicationException):
    def __init__(self, current_cols: int, *args: object) -> None:
        super().__init__(*args)
        self.current_cols = current_cols

    def __str__(self) -> str:
        return "Invalid terminal size. At least {0} cols required, got {1}.".format(
            settings.minimum_cols, self.current_cols
        )


class InvalidExcercisesDir(ApplicationException):
    def __init__(self, path: Path, *args: object) -> None:
        super().__init__(*args)
        self.path = path

    def __str__(self) -> str:
        return ("Invalid path to the excercises directory: {0}\n").format(self.path)


class NotAFileException(ApplicationException):
    def __init__(self, path: Any, *args: object) -> None:
        super().__init__(*args)
        self.path = Path(str(path)).resolve()

    def __str__(self) -> str:
        return ("'{0}' is not a file or can not be open.").format(self.path)


class EmptyExcerciseException(ApplicationException):
    def __init__(self, path: Any, *args: object) -> None:
        super().__init__(*args)
        self.path = Path(str(path)).resolve()

    def __str__(self) -> str:
        return ("'{0}' is empty.").format(self.path)
