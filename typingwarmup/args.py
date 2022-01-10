import argparse
from pathlib import Path
from typing import Optional, Union

import text


parser = argparse.ArgumentParser(description=text.app_name)
parser.add_argument(
    "exercise",
    nargs="?",
    type=str,
    default=None,
    help=text.arg_description,
)
parser.parse_args()


def ex_name_from_args() -> Optional[Union[Path, str]]:
    args = parser.parse_args()
    return args.exercise
