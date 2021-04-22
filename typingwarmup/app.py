from model import Model
from ui import UI


def is_input_corect(exercise: Model, input_char: str) -> bool:
    if exercise.is_end_of_line():
        return input_char in {" ", "\t", "\n"}
    return exercise.current_char_is(input_char)


def typing_warmup(stdscr, name: str, ex_path: str, random: bool, exit_key="KEY_F(10)"):
    input_char = ""

    model = Model(ex_path, name, random)
    ui = UI(stdscr, model)
    ui.start()
    ui.render_model()

    while not model.done() and input_char != exit_key:
        ui.render_model()

        if model.current_char_is_new_line():
            model.next_row()
            continue

        input_char = ui.input()
        if is_input_corect(model, input_char):
            model.next_col()
        elif input_char == "KEY_RESIZE":
            model.is_to_render = True
        elif input_char == exit_key:
            pass
        else:
            model.add_error()

    ui.stop()
    return model.errors
