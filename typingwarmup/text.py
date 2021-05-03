import settings

app_name = "Typing Warmup"
goodbye = "Good job! Errors, total: {error_count}, statistics:"
err_not_found = "The excercise `{0}` is not found"


def status_bar(errors=None, is_err_state=False):
    msg = "{name} | Press `{exit_key}` to exit".format(
        name=app_name, exit_key=settings.exit_key
    )
    if is_err_state:
        msg += " | Wrong key; press `{0}` to continue".format(settings.clear_key)
    elif errors:
        msg += " | {0} errors".format(errors)
    return msg
