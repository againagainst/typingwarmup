exit_key = "KEY_F(10)"
clear_key = "KEY_BACKSPACE"

meny_up_key = "KEY_UP"
meny_down_key = "KEY_DOWN"
meny_page_up_key = "KEY_NPAGE"
meny_page_down_key = "KEY_PPAGE"
meny_enter_key = {"\n", "\x1b"}
meny_header_padding = 1
meny_bottom_padding = 2

env_ex_path = "WARMUP_EX_PATH"
exercise_dir_name = "exercises"

skip_empty_rows = True

header_padding = 2
minimum_text_rows = 2
bottom_padding = 1
status_bar_rows = 1
# App won't start if r,c = stdscr.getmaxyx(); r < minimum_rows
minimum_rows = header_padding + minimum_text_rows + bottom_padding + status_bar_rows
