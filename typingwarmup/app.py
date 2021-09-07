import os
import argparse
from pathlib import Path
from typing import List, Optional, Tuple
from state import State

import text
import settings
from errors import InvalidExcercisesDir
from model import Model
from ui import WarmupUI, MenyUI
from stats import Stats


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


def ex_name_from_args() -> Optional[str]:
    parser = argparse.ArgumentParser(description=text.app_name)
    parser.add_argument(
        "exercise",
        nargs="?",
        type=str,
        default=None,
        help=text.arg_description,
    )

    args = parser.parse_args()
    return args.exercise


def ex_name_from_menu(stdscr, ex_path: Path) -> Optional[str]:
    input_char = ""

    ui = MenyUI(stdscr, read_exercises(ex_path))
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


def read_exercises(ex_path: Path) -> List[str]:
    def create_time(f: os.DirEntry) -> float:
        return f.stat().st_ctime

    def file_name(f: os.DirEntry) -> str:
        return f.name

    try:
        exercises = os.scandir(ex_path)
        exercises = sorted(exercises, key=create_time, reverse=True)
        exercises = map(file_name, exercises)
        return list(exercises)
    except OSError:
        raise InvalidExcercisesDir(ex_path)


def warmup_screen(stdscr, excercise: Path) -> Stats:
    input_char = ""

    state = State()
    stats = Stats()
    model = Model(excercise)
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


def is_input_correct(input_char: str, model: Model) -> bool:
    if model.is_cursor_at_eol():
        return input_char in text.end_of_line_symbols
    return model.cursor_char_equals(input_char)


def page_size(stdscr) -> Tuple[int, int]:
    max_row, max_col = stdscr.getmaxyx()
    return (max_row - settings.interface_rows, max_col)
