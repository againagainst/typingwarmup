exit_key = "KEY_F(10)"
clear_key = "KEY_BACKSPACE"
tab_key = "\t"
skip_key = "KEY_RIGHT"
end_of_line_symbols = {" ", "\t", "\n"}

meny_up_key = "KEY_UP"
meny_down_key = "KEY_DOWN"
meny_page_up_key = "KEY_NPAGE"
meny_page_down_key = "KEY_PPAGE"
meny_enter_key = {"\n", "\x1b"}
meny_header_padding = 1
meny_bottom_padding = 2

exercise_dir_name = "exercises"

max_score = 100
mistakes_limit_headers_only = 100
mistakes_limit_compact = 30
mistakes_skip_if_less_compact = 3
mistakes_skip_if_less_detailed = 0

# skip_empty_rows = True # do we want this?
tab_to_skip_spaces = True
new_line_on_space = False

header_padding = 2
bottom_padding = 1
left_padding = 1
right_padding = 2
status_bar_rows = 1
interface_rows = header_padding + bottom_padding + status_bar_rows
minimum_text_rows = 2
history_rows = 2
# App won't start
# if r < minimum_rows or c < minimum_cols
# where r,c = stdscr.getmaxyx();
minimum_rows = interface_rows + minimum_text_rows
minimum_cols = 120

# persistance
db_filename = "db/stats.shelve"


# shortcuts
def is_headers_only(mistakes_count: int) -> bool:
    return mistakes_count > mistakes_limit_headers_only


def is_compact(mistakes_count: int) -> bool:
    return mistakes_limit_headers_only > mistakes_count > mistakes_limit_compact


def skip_if_less(mistakes_count: int) -> int:
    if is_compact(mistakes_count):
        return mistakes_skip_if_less_compact
    else:
        return mistakes_skip_if_less_detailed
