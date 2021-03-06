import os
import argparse
from pathlib import Path
from typing import List, Optional

import text
import settings
from errors import InvalidExcercisesDir
from model import Model
from ui import WarmupUI, MenyUI
from stats import Stats


def typing_warmup(stdscr) -> Optional[Stats]:
    current_dir = Path(__file__).parent.absolute()
    ex_path = Path(os.environ.get(settings.env_ex_path, current_dir))
    ex_name = ex_name_from_args() or ex_name_from_menu(stdscr, ex_path)
    return warmup_screen(stdscr, ex_name, ex_path) if ex_name else None


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
    def is_excercise(f: os.DirEntry) -> bool:
        return f.name not in {"gen.py", "config.json"}

    def create_time(f: os.DirEntry) -> float:
        return f.stat().st_ctime

    def file_name(f: os.DirEntry) -> str:
        return f.name

    try:
        full_path = os.path.join(ex_path, settings.exercise_dir_name)
        exercises = filter(is_excercise, os.scandir(full_path))
        exercises = sorted(exercises, key=create_time, reverse=True)
        exercises = map(file_name, exercises)
        return list(exercises)
    except OSError:
        raise InvalidExcercisesDir(ex_path)


def warmup_screen(stdscr, name: str, ex_path: Path) -> Stats:
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
            model.add_error(text.escape_key(input_char))

    ui.stop()
    return model.stats


def is_input_corect(model: Model, input_char: str) -> bool:
    if model.is_end_of_line():
        return input_char in text.end_of_line_symbols
    return model.current_char_is(input_char)
