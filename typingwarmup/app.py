import text
from ui import UI


def typing_warmup(stdscr, exercise, exit_key="KEY_F(10)"):
    next_char = ""
    idx = 0
    highlight_error = False
    errors = 0

    ui = UI(stdscr)
    ui.start()
    ui.render_line_in_status_bar(text.status_bar(errors=errors))
    ui.render_dimmed(exercise)

    while idx < len(exercise) and next_char != exit_key:
        if exercise[idx] == "\n":
            idx += 1
            ui.next_row()
            continue

        ui.render_highlighted(exercise[idx], error=highlight_error)

        next_char = ui.input()
        if next_char == exercise[idx]:
            ui.render_bright(exercise[idx])
            idx += 1
            ui.next_col()
            highlight_error = False
        elif next_char == "KEY_RESIZE":
            pass  # fix later
        elif next_char == exit_key:
            pass
        else:
            highlight_error = True
            errors += 1
        ui.render_line_in_status_bar(text.status_bar(errors=errors))

    return errors