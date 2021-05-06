import settings

app_name = "Typing Warmup"
goodbye = "\nGood job! Errors, total: {error_count}\n"
err_not_found = "The excercise `{0}` is not found"
expected_key_stat = "With '{0}' key, {1} errors:\n"
actual_key_stat = "  -> '{0}': {1} times\n"


def status_bar(errors=None, is_err_state=False):
    msg = "{name} | Press `{exit_key}` to exit".format(
        name=app_name, exit_key=settings.exit_key
    )
    if is_err_state:
        msg += " | Wrong key; press `{0}` to continue".format(settings.clear_key)
    elif errors:
        msg += " | {0} errors".format(errors)
    return msg


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
    "\x1b": "⎋"
}