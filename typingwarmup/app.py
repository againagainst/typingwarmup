import text
from model import Model
from ui import UI


def typing_warmup(stdscr, exercise: Model, exit_key="KEY_F(10)"):
    next_char = ""
    highlight_error = False
    errors = 0

    ui = UI(stdscr)
    ui.start()
    ui.render_line_in_status_bar(text.status_bar(errors=errors))
    ui.render_dimmed(exercise.text)

    while not exercise.done() and next_char != exit_key:
        if exercise.current_char_is_new_line():
            exercise.next_char()
            ui.next_row()
            continue

        ui.render_highlighted(exercise.current_char(), error=highlight_error)

        next_char = ui.input()
        if exercise.current_char_is(next_char):
            ui.render_bright(exercise.current_char())
            exercise.next_char()
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