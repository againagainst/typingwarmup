goodbye = "Good job! Errors: {errors}"
err_not_found = "The excercise `{0}` is not found"


def status_bar(exit_key="F10", errors=None):
    msg = "Typing Warmup | Press `{0}` to exit ".format(exit_key)
    if errors:
        msg += "| {0} errors".format(errors)
    return msg
