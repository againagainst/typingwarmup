from typing import Optional
import settings
from stats import Stats

app_name = "Typing Warmup"
expected_key_stat = "With '{0}' key, {1} errors:\n"
actual_key_stat = "  -> '{0}': {1} times\n"

unknown_symbol = "⍰"
end_of_line_symbols = {" ", "\t", "\n"}
resize_event = "KEY_RESIZE"

arg_description = (
    "Optional. Name of the exercise; if not provided shows a meny to select."
)


def menu_item(idx: int, name: str) -> str:
    return "{0:>2}. {1}".format(idx + 1, name)


def status_bar(errors: Optional[int] = None, is_err_state: bool = False):
    msg = "{name} | Press `{exit_key}` to exit".format(
        name=app_name, exit_key=settings.exit_key
    )
    if is_err_state:
        msg += " | Wrong key; press `{0}` to continue".format(settings.clear_key)
    elif errors:
        msg += " | {0} errors".format(errors)
    return msg


def exit_msg(stats: Optional[Stats]) -> str:
    if stats:
        return "Good job! Total errors: {error_count}\n{stats}".format(
            error_count=stats.error_count(), stats=stats.formatted()
        )
    else:
        return "Bye!"


def escape_key(key: str) -> str:
    if len(key) == 1 and key != "\n":
        return key
    return special_keymap.get(key, unknown_symbol)


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
    "\x1b": "⏎",
    "\n": "⏎",
}