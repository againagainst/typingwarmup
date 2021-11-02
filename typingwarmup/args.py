import argparse
from pathlib import Path
from typing import Optional

import text


def ex_name_from_args() -> Optional[Path]:
    parser = argparse.ArgumentParser(description=text.app_name)
    parser.add_argument(
        "exercise",
        nargs="?",
        type=str,
        default=None,
        help=text.arg_description,
    )

    args = parser.parse_args()
    return args.exercise