from argparse import ArgumentParser, Namespace

import text


parser = ArgumentParser(description=text.app_name)
parser.add_argument(
    "exercise",
    nargs="?",
    type=str,
    default=None,
    help=text.help_exercise,
)
parser.add_argument(
    "-N",
    "--nodb",
    action="store_true",
    default=False,
    dest="ignore_results",
    help=text.help_nodb,
)

cli_args: Namespace = parser.parse_args()
