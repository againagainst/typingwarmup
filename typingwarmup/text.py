import unicodedata

from typing import Optional
from model.warmup import WarmupModel
import settings
from stats import Stats

app_name = "Typing Warmup"
finger_key_stat = "With {0}, {1} errors:\n"
actual_expected_stat = "  '{0}' instead of '{1}', {2} times\n"

unknown_symbol = "⍰"
end_of_line_symbols = {" ", "\t", "\n"}
resize_event = "KEY_RESIZE"

arg_description = (
    "Optional. Name of the exercise; if not provided shows a meny to select."
)


def is_control_char(ch: str) -> bool:
    return unicodedata.category(ch[0]) == "Cc"


def menu_item(idx: int, name: str) -> str:
    return "{0:>2}. {1}".format(idx + 1, name)


def status_bar(
    errors: Optional[int] = None,
    is_err_state: bool = False,
    model: Optional[WarmupModel] = None,
):
    messages = [
        app_name,
    ]
    if model:
        messages.append("{position}:{total} {percent}%".format(**model.progress()))
    if errors:
        messages.append("{0} errors".format(errors))
    if is_err_state:
        messages.append("Wrong key; press `{0}` to continue".format(settings.clear_key))
    messages.append("Press `{0}` to exit".format(settings.exit_key))
    return " | ".join(messages)


def exit_msg(stats: Optional[Stats]) -> str:
    if stats:
        return (
            "All done! Typed: {sybols_count}, errors: {error_count}, score: {score}\n"
            + "{stats}"
        ).format(
            sybols_count=stats.symbols_typed,
            error_count=stats.error_count(),
            stats=stats.formatted(),
            score=stats.score(),
        )
    else:
        return "Bye!"


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
