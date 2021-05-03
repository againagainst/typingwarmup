from model import Model
from ui import UI
import settings


def is_input_corect(model: Model, input_char: str) -> bool:
    if model.is_end_of_line():
        return input_char in {" ", "\t", "\n"}
    return model.current_char_is(input_char)


def typing_warmup(stdscr, name: str, ex_path: str, random: bool):
    input_char = ""

    model = Model(ex_path, name, random)
    ui = UI(stdscr, model)
    ui.start()
    ui.render_model()

    while not model.done() and input_char != settings.exit_key:
        ui.render_model()

        if model.current_char_is_new_line():
            model.next_row()
            continue

        input_char = ui.input()
        if model.wrong_input:
            if input_char == settings.clear_key:
                model.clear_wrong_input()
            else:
                continue

        elif is_input_corect(model, input_char):
            model.next_col()
        elif input_char == "KEY_RESIZE":
            model.is_to_render = True
        elif input_char == settings.exit_key:
            pass
        else:
            model.add_error(input_char)

    ui.stop()
    return model.stats
