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
    ex_full_path = resolve_ex_path(stdscr)
    return warmup_screen(stdscr, ex_full_path) if ex_full_path else None


def warmup_screen(stdscr, excercise: Path) -> Stats:
    model = WarmupModel(excercise)
    state = State()
    stats = Stats()
    input_char = ""
    ui = WarmupUI(stdscr, model, state, stats)
    ui.start()

    while True:
        ui.render_model()
        input_char = ui.input()

        if input_char == settings.exit_key:
            break

        if state.wrong_input:
            if input_char == settings.clear_key:
                state.wrong_input = None
            else:
                continue
        elif is_skip_spaces(input_char, model):
            model.skip_spaces()
        elif is_input_correct(input_char, model):
            if model.is_cursor_at_the_end():
                break
            model.next()
        elif input_char == text.resize_event:
            pass
        else:
            stats.add_error(
                actual=input_char,
                expected=model.cursor_char(),
                is_eol=model.is_cursor_at_eol(),
            )
            state.wrong_input = text.escape_key(input_char)

    ui.stop()
    return stats


def is_skip_spaces(input_char: str, model: WarmupModel) -> bool:
    return (
        settings.tab_to_skip_spaces
        and input_char == settings.tab_key
        and model.cursor_char_equals(" ")
    )


def is_input_correct(input_char: str, model: WarmupModel) -> bool:
    if input_char == settings.skip_key:
        return True
    if settings.new_line_on_space and model.is_cursor_at_eol():
        return input_char in text.end_of_line_symbols
    return model.cursor_char_equals(input_char)


def resolve_ex_path(stdscr) -> Optional[Path]:
    ex_name = ex_name_from_args()
    if ex_name:
        ex_path = Path().resolve()  # cwd
    else:
        app_dir = Path(__file__).resolve().parents[1]
        ex_path = app_dir.joinpath(settings.exercise_dir_name)
        ex_name = MenyUI(stdscr, MenuModel.read_exercises(ex_path)).pick_name()
    return ex_path.joinpath(ex_name) if ex_name else None
