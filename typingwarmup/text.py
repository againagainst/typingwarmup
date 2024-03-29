import unicodedata
from typing import Dict, Optional

import settings

app_name = "Typing Warmup"
finger_header_semicolon = "With {0}, {1} errors:\n"
finger_header_dot = "With {0}, {1} errors.\n"
mistakes_detailed_stat = "  '{actual}' instead of '{expected}', {times} times\n"
mistakes_compact_stat = "{times: 3} errors typing '{expected}'\n"
skip_if_less_indication = "  ...\n"
ellipsis = "…"
unknown_symbol = "⍰"
resize_event = "KEY_RESIZE"
unavailable = "unavailable"

help_exercise = (
    "Optional. Name of the exercise; if not provided shows a meny to select."
)
help_nodb = (
    "Optional. Do not store stats in history. Default is false."
)

exit_msg = "All done!"
default_exit_msg = "Bye!"
exit_msg_stats = "Typed: {sybols_count}, errors: {error_count}, score: {score}"


def is_control_char(ch: str) -> bool:
    return unicodedata.category(ch[0]) == "Cc"


def menu_item(idx: int, name: str) -> str:
    return "{0:>2}. {1}".format(idx + 1, name)


def status_bar(
    errors: Optional[int] = None,
    is_err_state: bool = False,
    progress: Optional[Dict] = None,
) -> str:
    messages = [
        app_name,
    ]
    if progress:
        messages.append("{position}:{total} {percent}%".format(**progress))
    if errors:
        messages.append("{0} errors".format(errors))
    if is_err_state:
        messages.append("Wrong key; press `{0}` to continue".format(settings.clear_key))
    messages.append("Press `{0}` to exit".format(settings.exit_key))
    return " | ".join(messages)


def escape_key(key: str) -> str:
    default_escape_symbol = key
    if is_control_char(key) or len(key) > 1:
        default_escape_symbol = unknown_symbol
    return special_keymap.get(key, default_escape_symbol)


EOL = "⏎"
special_keymap = {
    "KEY_UP": "⇧",
    "KEY_DOWN": "⇩",
    "KEY_LEFT": "⇦",
    "KEY_RIGHT": "⇨",
    "KEY_HOME": "⇤",
    "KEY_END": "⇥",
    "KEY_BACKSPACE": "⌫",
    "KEY_IC": "⎀",
    "KEY_DC": "⌦",
    "KEY_PPAGE": "⤒",
    "KEY_NPAGE": "⤓",
    "KEY_BREAK": "⎊",
    "\x1b": EOL,
    "\n": EOL,
    "\t": "↹",
    "KEY_BTAB": "↹",
}
