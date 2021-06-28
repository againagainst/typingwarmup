exit_key = "KEY_F(10)"
clear_key = "KEY_BACKSPACE"

meny_up_key = "KEY_UP"
meny_down_key = "KEY_DOWN"
meny_page_up_key = "KEY_NPAGE"
meny_page_down_key = "KEY_PPAGE"
meny_enter_key = {"\n", "\x1b"}

env_ex_path = "WARMUP_EX_PATH"
exercise_dir_name = "exercises"

skip_empty_rows = True

# App won't start if r,c = stdscr.getmaxyx(); r < minimum_rows
top_padding_rows = 2
minimum_content_rows = 2
bottom_padding_rows = 1
status_bar_rows = 1
minimum_rows = (
    top_padding_rows + minimum_content_rows + bottom_padding_rows + status_bar_rows
)
