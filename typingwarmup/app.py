import os
from pathlib import Path
from typing import Optional

import settings
import text
from args import ex_name_from_args
from model import MenuModel, WarmupModel
from state import State
from stats import Stats
from ui import MenyUI, WarmupUI


def typing_warmup(stdscr) -> Optional[Stats]:
    current_dir = Path(__file__).parent.absolute()
    ex_path = Path(os.environ.get(settings.env_ex_path, current_dir))
    ex_path = ex_path.joinpath(settings.exercise_dir_name)
    ex_name = ex_name_from_args() or ex_name_from_menu(stdscr, ex_path)
    if ex_name:
        ex_full_path = ex_path.joinpath(ex_name)
        return warmup_screen(stdscr, ex_full_path)
    else:
        return None


def ex_name_from_menu(stdscr, ex_path: Path) -> Optional[str]:
    input_char = ""

    ui = MenyUI(stdscr, MenuModel.read_exercises(ex_path))
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
        elif input_char == settings.meny_page_up_key:
            ui.up(page=True)
        elif input_char == settings.meny_page_down_key:
            ui.down(page=True)
        else:
            pass


def warmup_screen(stdscr, excercise: Path) -> Stats:
    input_char = ""

    state = State()
    stats = Stats()
    model = WarmupModel(excercise)
    ui = WarmupUI(stdscr, model, state, stats)
    ui.start()

    while True:
        ui.render_model()
        input_char = ui.input()

        if state.wrong_input:
            if input_char == settings.clear_key:
                state.wrong_input = None
            else:
                continue
        elif is_input_correct(input_char, model):
            if model.is_cursor_at_the_end():
                break
            model.next()
        elif input_char == text.resize_event:
            pass
        elif input_char == settings.exit_key:
            break
        else:
            stats.add_error(
                actual=input_char,
                expected=model.cursor_char(),
                is_eol=model.is_cursor_at_eol(),
            )
            state.wrong_input = input_char

    ui.stop()
    return stats


def is_input_correct(input_char: str, model: WarmupModel) -> bool:
    if model.is_cursor_at_eol():
        return input_char in text.end_of_line_symbols
    return model.cursor_char_equals(input_char)
