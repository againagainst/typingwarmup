import os
from typing import Optional

import text
import settings
from model import Model
from ui import WarmupUI, MenyUI
from stats import Stats


def is_input_corect(model: Model, input_char: str) -> bool:
    if model.is_end_of_line():
        return input_char in text.end_of_line_symbols
    return model.current_char_is(input_char)


def escape_key(key: str) -> str:
    if len(key) == 1:
        return key
    return text.special_keymap.get(key, text.unknown_symbol)


def typing_warmup(stdscr, ex_path: str) -> Optional[Stats]:
    ex_name = menu_screen(stdscr, ex_path)
    return warmup_screen(stdscr, ex_name, ex_path) if ex_name else None


def menu_screen(stdscr, ex_path: str) -> Optional[str]:
    input_char = ""
    exercises = os.listdir(os.path.join(ex_path, settings.exercise_dir_name))
    exercises.remove("gen.py")
    exercises.remove("config.json")

    ui = MenyUI(stdscr, exercises)
    ui.start()

    while True:
        ui.render_model()
        input_char = ui.input()
        if input_char in settings.meny_enter_key:
            return ui.ex_name()
        elif input_char == settings.exit_key:
            return None
        elif input_char == settings.meny_up_key:
            ui.up()
        elif input_char == settings.meny_down_key:
            ui.down()
        else:
            pass


def warmup_screen(stdscr, name: str, ex_path: str) -> Stats:
    input_char = ""

    model = Model(ex_path, name)
    ui = WarmupUI(stdscr, model)
    ui.start()

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
        elif input_char == text.resize_event:
            model.is_to_render = True
        elif input_char == settings.exit_key:
            pass
        else:
            model.add_error(escape_key(input_char))

    ui.stop()
    return model.stats
