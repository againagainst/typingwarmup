from pathlib import Path

import analysis
import disk
import settings
import text
from args import cli_args
from model import WarmupModel
from state import State
from stats import Stats
from ui import MenyUI, WarmupUI, CursesScreen


def typing_warmup(stdscr: CursesScreen) -> str:
    ex_name = cli_args.exercise
    ex_path = Path().resolve()  # cwd
    if not ex_name:
        menu = MenyUI(stdscr, disk.list_files(ex_path))
        ex_name = menu.pick_name()
        if not ex_name:
            return text.default_exit_msg
        ex_path = disk.exercise_dir()
    ex_full_path = ex_path.joinpath(ex_name)
    return warmup_screen(stdscr, ex_full_path)


def warmup_screen(stdscr: CursesScreen, excercise_path: Path) -> str:
    exercise_text = disk.read_exercise(excercise_path)
    model = WarmupModel(exercise_text)
    stats = Stats(exercise_length=len(exercise_text))
    state = State()
    ui = WarmupUI(stdscr, model, state, stats)
    ui.start()

    input_char = ""
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
        elif input_char == text.resize_event:
            ui.resize()
        elif is_skip_spaces(input_char, model):
            model.skip_spaces()
        elif is_input_correct(input_char, model):
            stats.add_typed()
            model.next()
            if model.is_cursor_at_the_end():
                break
        else:
            stats.add_mistake(
                actual=input_char,
                expected=model.cursor_char(),
                is_eol=model.is_cursor_at_eol(),
            )
            state.wrong_input = text.escape_key(input_char)
    ui.stop()
    if not cli_args.ignore_results:
        analysis.persist(excercise_path, exercise_text, stats)
    return stats.exit_msg()


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
        return input_char in settings.end_of_line_symbols
    return model.cursor_char_equals(input_char)
