import time
from kandinsky import fill_rect, draw_string
from gint import *
from random import randint, choice

L_WINDOW = 320
H_WINDOW = 224

H_FONT = 10
LNUM_FONT = 8

GRID_SIZE = 8
CELL_SIZE = 28
PREVIEW_CELL_SIZE = 14

GRID_X = 0
GRID_Y = 0
BLOCK_AREA_X = GRID_X + GRID_SIZE * CELL_SIZE + 5

SMALL_LABEL_BLOCK_PADDING = 2
FIXED_GAP_BETWEEN_BLOCKS = 5

SCORE_DISPLAY_Y = 2
BLOCKS_DISPLAY_START_Y = SCORE_DISPLAY_Y + H_FONT + 20

MENU_WIDTH = 150
MENU_HEIGHT_MAIN = 100
MENU_HEIGHT_SUB = 80
MENU_X = (L_WINDOW - MENU_WIDTH) // 2
MENU_Y = (H_WINDOW - MENU_HEIGHT_MAIN) // 2
MENU_BG_COLOR = (60, 60, 60)
MENU_TEXT_COLOR = (255, 255, 255)
MENU_HIGHLIGHT_COLOR = (100, 100, 200)

MAIN_MENU = 0
MODE_SELECTION_MENU = 1
SETTINGS_MENU = 2
PLAYING = 3
GAME_OVER = 4
PAUSED = 5

current_game_state = MAIN_MENU
main_menu_selection_index = 0
mode_menu_selection_index = 0
settings_menu_selection_index = 0
menu_selection_index = 0

BACKGROUND_COLOR = (40, 40, 40)
BORDER_COLOR = (255, 255, 255)
GROUND_COLOR = (180, 232, 232)
CLEAR_HIGHLIGHT_COLOR = (200, 255, 200)
POTENTIAL_CLEAR_COLOR = (100, 200, 255)
TEXT_COLOR = (255, 255, 255)

is_dark_theme = True

def update_theme_colors():
    global BACKGROUND_COLOR, BORDER_COLOR, TEXT_COLOR, MENU_BG_COLOR, MENU_TEXT_COLOR, MENU_HIGHLIGHT_COLOR
    if is_dark_theme:
        BACKGROUND_COLOR = (40, 40, 40)
        BORDER_COLOR = (255, 255, 255)
        TEXT_COLOR = (255, 255, 255)
        MENU_BG_COLOR = (60, 60, 60)
        MENU_TEXT_COLOR = (255, 255, 255)
        MENU_HIGHLIGHT_COLOR = (100, 100, 200)
    else:
        BACKGROUND_COLOR = (200, 200, 200)
        BORDER_COLOR = (0, 0, 0)
        TEXT_COLOR = (0, 0, 0)
        MENU_BG_COLOR = (180, 180, 180)
        MENU_TEXT_COLOR = (0, 0, 0)
        MENU_HIGHLIGHT_COLOR = (150, 150, 250)

update_theme_colors()

combo_chain = 0
is_easy_mode = True
is_normal_mode = False

PREDEFINED_COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 165, 0),
    (128, 0, 128),
    (255, 255, 0)
]

SHAPES = [
    [[1, 1, 1],
     [1, 1, 1],
     [1, 1, 1]],
    [[1, 1, 1],
     [1, 1, 1],
     [0, 0, 0]],
    [[1, 1, 0],
     [1, 1, 0],
     [1, 1, 0]],
    [[1, 1, 0],
     [1, 1, 0],
     [0, 0, 0]],
    [[1, 1, 0],
     [0, 0, 0],
     [0, 0, 0]],
    [[1, 0, 0],
     [1, 0, 0],
     [0, 0, 0]],
    [[1, 0, 0],
     [1, 0, 0],
     [1, 0, 0]],
    [[1, 1, 1],
     [0, 0, 0],
     [0, 0, 0]],
    [[1, 0, 0],
     [0, 0, 0],
     [0, 0, 0]],
    [[1, 0, 0],
     [1, 0, 0],
     [1, 1, 0]],
    [[1, 1, 0],
     [1, 0, 0],
     [1, 0, 0]],
    [[1, 1, 1],
     [1, 0, 0],
     [0, 0, 0]],
    [[1, 1, 1],
     [0, 0, 1],
     [0, 0, 0]],
    [[1, 1, 0],
     [0, 1, 1],
     [0, 0, 0]],
    [[0, 1, 1],
     [1, 1, 0],
     [0, 0, 0]],
    [[1, 0, 0],
     [1, 1, 0],
     [0, 1, 0]],
    [[0, 1, 0],
     [1, 1, 0],
     [1, 0, 0]],
    [[1, 0, 0],
     [1, 1, 0],
     [1, 0, 0]],
    [[0, 1, 0],
     [1, 1, 1],
     [0, 0, 0]],
    [[0, 1, 0],
     [1, 1, 0],
     [0, 1, 0]],
    [[1, 1, 1],
     [0, 1, 0],
     [0, 0, 0]],
    [[1, 1, 1],
     [1, 0, 0],
     [1, 0, 0]],
    [[1, 0, 0],
     [1, 0, 0],
     [1, 1, 1]],
    [[1, 1, 1],
     [0, 0, 1],
     [0, 0, 1]],
    [[0, 0, 1],
     [0, 0, 1],
     [1, 1, 1]],
    [[0, 0, 1],
     [0, 1, 0],
     [1, 0, 0]],
    [[1, 0, 0],
     [0, 1, 0],
     [0, 0, 1]],
    [[1, 0, 0],
     [0, 1, 0],
     [0, 0, 0]],
    [[0, 1, 0],
     [1, 0, 0],
     [0, 0, 0]],
    [[0, 0, 1],
     [0, 1, 0],
     [0, 0, 0]],
    [[0, 1, 0],
     [0, 0, 1],
     [0, 0, 0]],
]

EASY_SHAPES_INDICES = [3, 4, 5, 6, 7, 8]

grid = [[BACKGROUND_COLOR for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
score = 0
cursor_x, cursor_y = 0, 0
prev_cursor_x, prev_cursor_y = 0, 0
game_over = False

available_blocks = []
active_block_shape = None
active_block_color = None
selected_block_idx = -1

highlighted_rows = []
highlighted_cols = []

prev_block_preview_pos_x = -1
prev_block_preview_pos_y = -1
prev_active_block_shape = None

def generate_random_color():
    return choice(PREDEFINED_COLORS)

def get_lightened_color(rgb_tuple, amount=100):
    r, g, b = rgb_tuple
    new_r = min(255, r + amount)
    new_g = min(255, g + amount)
    new_b = min(255, b + amount)
    return (new_r, new_g, new_b)

def draw_prect(x, y, w, h, c):
    fill_rect(x, y, w, h, c)

def draw_grid_cell(row, col, color=None):
    cell_color = grid[row][col] if color is None else color
    draw_prect(GRID_X + col * CELL_SIZE + 1, GRID_Y + row * CELL_SIZE + 1,
               CELL_SIZE - 2, CELL_SIZE - 2, cell_color)

def draw_initial_grid():
    fill_rect(GRID_X, GRID_Y, GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE, BACKGROUND_COLOR)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            draw_prect(GRID_X + j * CELL_SIZE, GRID_Y + i * CELL_SIZE,
                       CELL_SIZE, CELL_SIZE, BORDER_COLOR)

def draw_current_block_preview(block, row, col, color):
    if block is None:
        return
    for i in range(3):
        for j in range(3):
            if i < len(block) and j < len(block[i]) and block[i][j]:
                grid_pos_x = col + j
                grid_pos_y = row + i
                if 0 <= grid_pos_y < GRID_SIZE and 0 <= grid_pos_x < GRID_SIZE:
                    draw_prect(GRID_X + grid_pos_x * CELL_SIZE + 1, GRID_Y + grid_pos_y * CELL_SIZE + 1,
                               CELL_SIZE - 2, CELL_SIZE - 2, color)

def draw_block(block, x, y, color, cell_size_override=None):
    size = CELL_SIZE if cell_size_override is None else cell_size_override
    for i in range(3):
        for j in range(3):
            if i < len(block) and j < len(block[i]) and block[i][j]:
                draw_prect(x + j * size + 1, y + i * size + 1,
                           size - 2, size - 2, color)

def draw_score():
    fill_rect(BLOCK_AREA_X, SCORE_DISPLAY_Y, L_WINDOW - BLOCK_AREA_X, H_FONT + 10, BACKGROUND_COLOR)
    score_str_val = str(score)
    full_score_text = score_str_val
    draw_string(full_score_text, BLOCK_AREA_X, SCORE_DISPLAY_Y, TEXT_COLOR, BACKGROUND_COLOR)

def draw_game_over():
    global score
    if game_over:
        fill_rect(0, 0, L_WINDOW, H_WINDOW, BACKGROUND_COLOR)
        game_over_text = "Game Over!"
        reset_text = "[MENU] to reset"
        score_text = "Score: " + str(score)
        line_spacing = H_FONT + 5
        total_text_height = 3 * H_FONT + 2 * 5
        initial_y = (H_WINDOW - total_text_height) // 2
        text_width_go = LNUM_FONT * len(game_over_text)
        text_x_go = (L_WINDOW - text_width_go) // 2
        draw_string(game_over_text, text_x_go, initial_y, TEXT_COLOR, BACKGROUND_COLOR)
        text_width_score = LNUM_FONT * len(score_text)
        text_x_score = (L_WINDOW - text_width_score) // 2
        draw_string(score_text, text_x_score, initial_y + line_spacing, TEXT_COLOR, BACKGROUND_COLOR)
        text_width_reset = LNUM_FONT * len(reset_text)
        text_x_reset = (L_WINDOW - text_width_reset) // 2
        draw_string(reset_text, text_x_reset, initial_y + 2 * line_spacing, TEXT_COLOR, BACKGROUND_COLOR)

def draw_available_blocks():
    fill_rect(BLOCK_AREA_X, BLOCKS_DISPLAY_START_Y, L_WINDOW - BLOCK_AREA_X, H_WINDOW - BLOCKS_DISPLAY_START_Y, BACKGROUND_COLOR)
    current_y_pos = BLOCKS_DISPLAY_START_Y
    for i, block_data in enumerate(available_blocks):
        label_y = current_y_pos
        draw_string(f"F{i+1}:", BLOCK_AREA_X, label_y, TEXT_COLOR, BACKGROUND_COLOR)
        block_width = 3 * PREVIEW_CELL_SIZE + 2
        label_width = LNUM_FONT * len(f"F{i+1}:")
        block_x = BLOCK_AREA_X + label_width + SMALL_LABEL_BLOCK_PADDING
        available_space = (L_WINDOW - BLOCK_AREA_X) - (label_width + SMALL_LABEL_BLOCK_PADDING)
        center_offset = max(0, (available_space - block_width) // 2)
        block_x += center_offset
        block_y = label_y + H_FONT + SMALL_LABEL_BLOCK_PADDING
        if block_data is not None:
            draw_block(block_data['shape'], block_x, block_y, block_data['color'], PREVIEW_CELL_SIZE)
        else:
            used_text = f"F{i+1}: USED"
            used_width = LNUM_FONT * len(used_text)
            fill_rect(BLOCK_AREA_X, label_y, used_width, H_FONT, BACKGROUND_COLOR)
            draw_string(used_text, BLOCK_AREA_X, label_y, TEXT_COLOR, BACKGROUND_COLOR)
            fill_rect(block_x, block_y, 3 * PREVIEW_CELL_SIZE + 2, 3 * PREVIEW_CELL_SIZE + 2, BACKGROUND_COLOR)
        current_y_pos += (H_FONT + SMALL_LABEL_BLOCK_PADDING + 3 * PREVIEW_CELL_SIZE + FIXED_GAP_BETWEEN_BLOCKS)

def draw_main_menu():
    global main_menu_selection_index
    fill_rect(0, 0, L_WINDOW, H_WINDOW, BACKGROUND_COLOR)
    title_text = "BLOCK BLAST"
    title_width = LNUM_FONT * len(title_text)
    title_x = (L_WINDOW - title_width) // 2
    title_y = H_WINDOW // 4 - H_FONT // 2
    draw_string(title_text, title_x, title_y, TEXT_COLOR, BACKGROUND_COLOR)
    options = ["Play Mode Normal", "Play with Selected Mode", "Settings", "Exit"]
    line_height = H_FONT + 8
    total_height = len(options) * line_height
    menu_start_y = title_y + H_FONT + 20
    for i, option_text in enumerate(options):
        current_y = menu_start_y + i * line_height
        text_width = LNUM_FONT * len(option_text)
        text_x = (L_WINDOW - text_width) // 2
        if i == main_menu_selection_index:
            fill_rect(text_x - 5, current_y - 2, text_width + 10, H_FONT + 4, MENU_HIGHLIGHT_COLOR)
            draw_string(option_text, text_x, current_y, MENU_TEXT_COLOR, MENU_HIGHLIGHT_COLOR)
        else:
            draw_string(option_text, text_x, current_y, TEXT_COLOR, BACKGROUND_COLOR)

def draw_mode_selection_menu():
    global mode_menu_selection_index
    fill_rect(0, 0, L_WINDOW, H_WINDOW, BACKGROUND_COLOR)
    title_text = "SELECT MODE"
    title_width = LNUM_FONT * len(title_text)
    title_x = (L_WINDOW - title_width) // 2
    title_y = H_WINDOW // 4 - H_FONT // 2
    draw_string(title_text, title_x, title_y, TEXT_COLOR, BACKGROUND_COLOR)
    options = ["Easy Mode", "Hard Mode", "Back"]
    line_height = H_FONT + 8
    total_height = len(options) * line_height
    menu_start_y = title_y + H_FONT + 20
    for i, option_text in enumerate(options):
        current_y = menu_start_y + i * line_height
        text_width = LNUM_FONT * len(option_text)
        text_x = (L_WINDOW - text_width) // 2
        if i == mode_menu_selection_index:
            fill_rect(text_x - 5, current_y - 2, text_width + 10, H_FONT + 4, MENU_HIGHLIGHT_COLOR)
            draw_string(option_text, text_x, current_y, MENU_TEXT_COLOR, MENU_HIGHLIGHT_COLOR)
        else:
            draw_string(option_text, text_x, current_y, TEXT_COLOR, BACKGROUND_COLOR)

def draw_settings_menu():
    global settings_menu_selection_index, is_dark_theme
    fill_rect(0, 0, L_WINDOW, H_WINDOW, BACKGROUND_COLOR)
    title_text = "SETTINGS"
    title_width = LNUM_FONT * len(title_text)
    title_x = (L_WINDOW - title_width) // 2
    title_y = H_WINDOW // 4 - H_FONT // 2
    draw_string(title_text, title_x, title_y, TEXT_COLOR, BACKGROUND_COLOR)
    theme_status = "Dark" if is_dark_theme else "Light"
    options = [f"Theme: {theme_status}", "Back"]
    line_height = H_FONT + 8
    total_height = len(options) * line_height
    menu_start_y = title_y + H_FONT + 20
    for i, option_text in enumerate(options):
        current_y = menu_start_y + i * line_height
        text_width = LNUM_FONT * len(option_text)
        text_x = (L_WINDOW - text_width) // 2
        if i == settings_menu_selection_index:
            fill_rect(text_x - 5, current_y - 2, text_width + 10, H_FONT + 4, MENU_HIGHLIGHT_COLOR)
            draw_string(option_text, text_x, current_y, MENU_TEXT_COLOR, MENU_HIGHLIGHT_COLOR)
        else:
            draw_string(option_text, text_x, current_y, TEXT_COLOR, BACKGROUND_COLOR)

def generate_three_blocks():
    global available_blocks, active_block_shape, active_block_color, selected_block_idx, is_easy_mode
    available_blocks = []
    for _ in range(3):
        if is_easy_mode:
            shape_idx = choice(EASY_SHAPES_INDICES)
            color = generate_random_color()
        else:
            shape_idx = randint(0, len(SHAPES) - 1)
            color = (255, 192, 203)  # Pink color for Hard Mode
        shape = [[0 for _ in range(3)] for _ in range(3)]
        for r_s in range(len(SHAPES[shape_idx])):
            for c_s in range(len(SHAPES[shape_idx][r_s])):
                shape[r_s][c_s] = SHAPES[shape_idx][r_s][c_s]
        available_blocks.append({"shape": shape, "color": color})
    active_block_shape = None
    active_block_color = None
    selected_block_idx = -1
    draw_available_blocks()

def can_place_block(block, row, col):
    if block is None:
        return False
    for i in range(len(block)):
        for j in range(len(block[i])):
            if block[i][j]:
                grid_pos_x = col + j
                grid_pos_y = row + i
                if not (0 <= grid_pos_y < GRID_SIZE and 0 <= grid_pos_x < GRID_SIZE) or \
                   grid[grid_pos_y][grid_pos_x] != BACKGROUND_COLOR:
                    return False
    return True

def place_block(block, row, col):
    global grid, score, is_easy_mode, active_block_shape
    num_cells_placed = 0
    for i in range(len(block)):
        for j in range(len(block[i])):
            if block[i][j]:
                if 0 <= row + i < GRID_SIZE and 0 <= col + j < GRID_SIZE:
                    grid[row + i][col + j] = active_block_color
                    draw_grid_cell(row + i, col + j)
                    num_cells_placed += 1
    score += num_cells_placed
    if not is_easy_mode and active_block_shape is not None:
        num_cells_in_active_block = sum(row.count(1) for row in active_block_shape)
        score += num_cells_in_active_block * 2
    return num_cells_placed

def would_clear_lines(block, target_row, target_col):
    temp_grid = [row[:] for row in grid]
    potential_rows_to_clear = []
    potential_cols_to_clear = []
    for i in range(len(block)):
        for j in range(len(block[i])):
            if block[i][j]:
                r, c = target_row + i, target_col + j
                if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and temp_grid[r][c] == BACKGROUND_COLOR:
                    temp_grid[r][c] = (1, 1, 1)
                else:
                    return [], []
    for r in range(GRID_SIZE):
        row_full = True
        for c in range(GRID_SIZE):
            if temp_grid[r][c] == BACKGROUND_COLOR:
                row_full = False
                break
        if row_full:
            potential_rows_to_clear.append(r)
    for c in range(GRID_SIZE):
        col_full = True
        for r in range(GRID_SIZE):
            if temp_grid[r][c] == BACKGROUND_COLOR:
                col_full = False
                break
        if col_full:
            potential_cols_to_clear.append(c)
    return potential_rows_to_clear, potential_cols_to_clear

def is_grid_empty():
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c] != BACKGROUND_COLOR:
                return False
    return True

def show_notification(message, duration=1.5):
    text_width = LNUM_FONT * len(message)
    text_x = (L_WINDOW - text_width) // 2
    text_y = (H_WINDOW - H_FONT) // 2
    fill_rect(text_x - 10, text_y - 5, text_width + 20, H_FONT + 10, (50, 50, 200))
    draw_string(message, text_x, text_y, (255, 255, 255), (50, 50, 200))
    time.sleep(duration)
    fill_rect(text_x - 10, text_y - 5, text_width + 20, H_FONT + 10, BACKGROUND_COLOR)
    draw_initial_grid()
    for r_grid in range(GRID_SIZE):
        for c_grid in range(GRID_SIZE):
            draw_grid_cell(r_grid, c_grid, grid[r_grid][c_grid])
    draw_score()
    draw_available_blocks()
    if active_block_shape is not None:
        draw_current_block_preview(active_block_shape, cursor_y, cursor_x, get_lightened_color(active_block_color))

def clear_lines():
    global score, combo_chain, grid, is_easy_mode, available_blocks, is_normal_mode
    rows_to_clear = []
    cols_to_clear = []
    for i in range(GRID_SIZE):
        row_full = True
        for j in range(GRID_SIZE):
            if grid[i][j] == BACKGROUND_COLOR:
                row_full = False
                break
        if row_full:
            rows_to_clear.append(i)
    for j in range(GRID_SIZE):
        col_full = True
        for i in range(GRID_SIZE):
            if grid[i][j] == BACKGROUND_COLOR:
                col_full = False
                break
        if col_full:
            cols_to_clear.append(j)
    num_lines_cleared = len(rows_to_clear) + len(cols_to_clear)
    if num_lines_cleared > 0:
        combo_chain += 1
        for r in rows_to_clear:
            for c in range(GRID_SIZE):
                draw_grid_cell(r, c, CLEAR_HIGHLIGHT_COLOR)
        for c in cols_to_clear:
            for r in range(GRID_SIZE):
                draw_grid_cell(r, c, CLEAR_HIGHLIGHT_COLOR)
        time.sleep(0.5)
        for r in rows_to_clear:
            for c in range(GRID_SIZE):
                grid[r][c] = BACKGROUND_COLOR
                draw_grid_cell(r, c)
        for c in cols_to_clear:
            for r in range(GRID_SIZE):
                grid[r][c] = BACKGROUND_COLOR
                draw_grid_cell(r, c)
        base_score_component = 10 * (num_lines_cleared)**2
        block_bonus_component = 0
        if active_block_shape is not None:
            num_cells_in_block = sum(row.count(1) for row in active_block_shape)
            if num_lines_cleared >= 3:
                block_bonus_component = num_cells_in_block * 5
            elif num_lines_cleared == 2:
                block_bonus_component = num_cells_in_block * 3
        clear_grid_bonus_component = 0
        grid_was_empty_after_clear = is_grid_empty()
        if grid_was_empty_after_clear:
            clear_grid_bonus_component = 500
            if is_normal_mode and is_easy_mode:
                is_easy_mode = False
                show_notification("Hard Mode: ACTIVATED!")
                draw_initial_grid()
                for r_grid in range(GRID_SIZE):
                    for c_grid in range(GRID_SIZE):
                        draw_grid_cell(r_grid, c_grid, grid[r_grid][c_grid])
                generate_three_blocks()
        mode_multiplier = 2 if not is_easy_mode else 1
        combo_bonus_factor = 1.0 + 0.2 * (combo_chain - 1) if combo_chain > 1 else 1.0
        total_score_this_turn = ((base_score_component * combo_bonus_factor) + \
                                 block_bonus_component + clear_grid_bonus_component) * mode_multiplier
        score += int(total_score_this_turn)
        draw_score()
    else:
        combo_chain = 0

def can_place_any_block_from_available():
    for block_data in available_blocks:
        if block_data is not None:
            block_shape = block_data['shape']
            for r in range(GRID_SIZE):
                for c in range(GRID_SIZE):
                    if can_place_block(block_shape, r, c):
                        return True
    return False

def clear_block_preview_and_highlights():
    global prev_block_preview_pos_x, prev_block_preview_pos_y, prev_active_block_shape, highlighted_rows, highlighted_cols
    if prev_block_preview_pos_x != -1 and prev_active_block_shape is not None:
        for i in range(len(prev_active_block_shape)):
            for j in range(len(prev_active_block_shape[i])):
                if prev_active_block_shape[i][j]:
                    grid_pos_x = prev_block_preview_pos_x + j
                    grid_pos_y = prev_block_preview_pos_y + i
                    if 0 <= grid_pos_y < GRID_SIZE and 0 <= grid_pos_x < GRID_SIZE:
                        draw_grid_cell(grid_pos_y, grid_pos_x)
    for r in highlighted_rows:
        for c in range(GRID_SIZE):
            draw_grid_cell(r, c)
    for c in highlighted_cols:
        for r in range(GRID_SIZE):
            draw_grid_cell(r, c)
    highlighted_rows = []
    highlighted_cols = []
    prev_block_preview_pos_x = -1
    prev_block_preview_pos_y = -1
    prev_active_block_shape = None

def reset_game_data():
    global grid, score, cursor_x, cursor_y, game_over, prev_cursor_x, prev_cursor_y, highlighted_rows, highlighted_cols, active_block_shape, active_block_color, selected_block_idx, combo_chain, prev_block_preview_pos_x, prev_block_preview_pos_y, prev_active_block_shape
    fill_rect(0, 0, L_WINDOW, H_WINDOW, BACKGROUND_COLOR)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            grid[i][j] = BACKGROUND_COLOR
    score = 0
    cursor_x, cursor_y = 0, 0
    prev_cursor_x, prev_cursor_y = 0, 0
    game_over = False
    highlighted_rows = []
    highlighted_cols = []
    active_block_shape = None
    active_block_color = None
    selected_block_idx = -1
    combo_chain = 0
    prev_block_preview_pos_x = -1
    prev_block_preview_pos_y = -1
    prev_active_block_shape = None

def start_game(mode, is_normal=False):
    global current_game_state, is_easy_mode, is_normal_mode
    is_easy_mode = mode if not is_normal else True
    is_normal_mode = is_normal
    reset_game_data()
    current_game_state = PLAYING
    draw_initial_grid()
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            draw_grid_cell(r, c)
    generate_three_blocks()
    draw_score()
    if not is_easy_mode:
        show_notification("Hard Mode: ON!", 1)

def draw_cursor():
    draw_grid_cell(prev_cursor_y, prev_cursor_x)

def handle_main_menu_input(key):
    global main_menu_selection_index, current_game_state, is_easy_mode, is_normal_mode
    options_count = 4
    if key == KEY_UP:
        main_menu_selection_index = (main_menu_selection_index - 1 + options_count) % options_count
        draw_main_menu()
    elif key == KEY_DOWN:
        main_menu_selection_index = (main_menu_selection_index + 1) % options_count
        draw_main_menu()
    elif key == KEY_EXE or key == KEY_SHIFT:
        if main_menu_selection_index == 0:
            start_game(True, is_normal=True)
        elif main_menu_selection_index == 1:
            current_game_state = MODE_SELECTION_MENU
            draw_mode_selection_menu()
        elif main_menu_selection_index == 2:
            current_game_state = SETTINGS_MENU
            draw_settings_menu()
        elif main_menu_selection_index == 3:
            raise SystemExit

def handle_mode_selection_input(key):
    global mode_menu_selection_index, current_game_state
    options_count = 3
    if key == KEY_UP:
        mode_menu_selection_index = (mode_menu_selection_index - 1 + options_count) % options_count
        draw_mode_selection_menu()
    elif key == KEY_DOWN:
        mode_menu_selection_index = (mode_menu_selection_index + 1) % options_count
        draw_mode_selection_menu()
    elif key == KEY_EXE or key == KEY_SHIFT:
        if mode_menu_selection_index == 0:
            start_game(True)
        elif mode_menu_selection_index == 1:
            start_game(False)
        elif mode_menu_selection_index == 2:
            current_game_state = MAIN_MENU
            draw_main_menu()

def handle_settings_input(key):
    global settings_menu_selection_index, current_game_state, is_dark_theme
    options_count = 2
    if key == KEY_UP:
        settings_menu_selection_index = (settings_menu_selection_index - 1 + options_count) % options_count
        draw_settings_menu()
    elif key == KEY_DOWN:
        settings_menu_selection_index = (settings_menu_selection_index + 1) % options_count
        draw_settings_menu()
    elif key == KEY_EXE or key == KEY_SHIFT:
        if settings_menu_selection_index == 0:
            is_dark_theme = not is_dark_theme
            update_theme_colors()
            draw_settings_menu()
        elif settings_menu_selection_index == 1:
            current_game_state = MAIN_MENU
            draw_main_menu()

def handle_playing_input(key):
    global cursor_x, cursor_y, game_over, prev_cursor_x, prev_cursor_y, score, highlighted_rows, highlighted_cols, active_block_shape, active_block_color, selected_block_idx, current_game_state
    global prev_block_preview_pos_x, prev_block_preview_pos_y, prev_active_block_shape
    if key == KEY_F6:
        current_game_state = PAUSED
        menu_selection_index = 0
        draw_menu_in_game()
        return
    prev_cursor_x, prev_cursor_y = cursor_x, cursor_y
    moved_cursor = False
    if key == KEY_LEFT and cursor_x > 0:
        cursor_x -= 1
        moved_cursor = True
    elif key == KEY_RIGHT and cursor_x < GRID_SIZE - 1:
        cursor_x += 1
        moved_cursor = True
    elif key == KEY_UP and cursor_y > 0:
        cursor_y -= 1
        moved_cursor = True
    elif key == KEY_DOWN and cursor_y < GRID_SIZE - 1:
        cursor_y += 1
        moved_cursor = True
    if key in [KEY_F1, KEY_F2, KEY_F3, KEY_1, KEY_2, KEY_3]:
        chosen_idx = -1
        if key == KEY_F1 or key == KEY_1: chosen_idx = 0
        elif key == KEY_F2 or key == KEY_2: chosen_idx = 1
        elif key == KEY_F3 or key == KEY_3: chosen_idx = 2
        if 0 <= chosen_idx < len(available_blocks) and available_blocks[chosen_idx] is not None:
            clear_block_preview_and_highlights()
            active_block_shape = available_blocks[chosen_idx]['shape']
            active_block_color = available_blocks[chosen_idx]['color']
            selected_block_idx = chosen_idx
            draw_available_blocks()
        moved_cursor = True
    elif (key == KEY_EXE or key == KEY_SHIFT) and active_block_shape is not None:
        if can_place_block(active_block_shape, cursor_y, cursor_x):
            cells_placed = place_block(active_block_shape, cursor_y, cursor_x)
            draw_score()
            clear_lines()
            available_blocks[selected_block_idx] = None
            draw_available_blocks()
            clear_block_preview_and_highlights()
            active_block_shape = None
            active_block_color = None
            selected_block_idx = -1
            cursor_x, cursor_y = 0, 0
            if all(b is None for b in available_blocks):
                generate_three_blocks()
    if moved_cursor or active_block_shape is not None:
        clear_block_preview_and_highlights()
        if active_block_shape is not None:
            current_preview_color = get_lightened_color(active_block_color)
            r_to_h, c_to_h = [], []
            if can_place_block(active_block_shape, cursor_y, cursor_x):
                r_to_h, c_to_h = would_clear_lines(active_block_shape, cursor_y, cursor_x)
                if r_to_h or c_to_h:
                    highlighted_rows = r_to_h
                    highlighted_cols = c_to_h
                    for r in highlighted_rows:
                        for c in range(GRID_SIZE):
                            draw_grid_cell(r, c, POTENTIAL_CLEAR_COLOR)
                    for c in highlighted_cols:
                        for r in range(GRID_SIZE):
                            draw_grid_cell(r, c, POTENTIAL_CLEAR_COLOR)
            draw_current_block_preview(active_block_shape, cursor_y, cursor_x, current_preview_color)
            prev_block_preview_pos_x = cursor_x
            prev_block_preview_pos_y = cursor_y
            prev_active_block_shape = active_block_shape
        else:
            prev_block_preview_pos_x = -1
            prev_block_preview_pos_y = -1
            prev_active_block_shape = None
    if not can_place_any_block_from_available():
        current_game_state = GAME_OVER
        game_over = True
        draw_game_over()
        return

def handle_paused_input(key):
    global menu_selection_index, current_game_state, is_easy_mode
    options = ["Resume", "Replay", "Exit"]
    options_count = len(options)
    if key == KEY_UP:
        menu_selection_index = (menu_selection_index - 1 + options_count) % options_count
        draw_menu_in_game()
    elif key == KEY_DOWN:
        menu_selection_index = (menu_selection_index + 1) % options_count
        draw_menu_in_game()
    elif key == KEY_EXE or key == KEY_SHIFT:
        if menu_selection_index == 0:
            current_game_state = PLAYING
            fill_rect(MENU_X - 10, MENU_Y - 10, MENU_WIDTH + 20, MENU_HEIGHT_MAIN + 20, BACKGROUND_COLOR)
            draw_initial_grid()
            for r in range(GRID_SIZE):
                for c in range(GRID_SIZE):
                    draw_grid_cell(r, c)
            draw_score()
            draw_available_blocks()
            if active_block_shape is not None:
                draw_current_block_preview(active_block_shape, cursor_y, cursor_x, get_lightened_color(active_block_color))
        elif menu_selection_index == 1:
            start_game(is_easy_mode, is_normal=is_normal_mode)
        elif menu_selection_index == 2:
            current_game_state = MAIN_MENU
            draw_main_menu()

def draw_menu_in_game():
    global menu_selection_index
    fill_rect(MENU_X, MENU_Y, MENU_WIDTH, MENU_HEIGHT_MAIN, MENU_BG_COLOR)
    options = ["Resume", "Replay", "Exit"]
    line_height = H_FONT + 5
    for i, option_text in enumerate(options):
        current_y = MENU_Y + 10 + i * line_height
        if i == menu_selection_index:
            fill_rect(MENU_X + 5, current_y - 2, MENU_WIDTH - 10, H_FONT + 4, MENU_TEXT_COLOR)
            draw_string(option_text, MENU_X + 10, current_y, MENU_BG_COLOR, MENU_TEXT_COLOR)
        else:
            draw_string(option_text, MENU_X + 10, current_y, MENU_TEXT_COLOR, MENU_BG_COLOR)

draw_main_menu()

while True:
    e = pollevent()
    if e.type == KEYEV_DOWN:
        if current_game_state == MAIN_MENU:
            handle_main_menu_input(e.key)
        elif current_game_state == MODE_SELECTION_MENU:
            handle_mode_selection_input(e.key)
        elif current_game_state == SETTINGS_MENU:
            handle_settings_input(e.key)
        elif current_game_state == PLAYING:
            handle_playing_input(e.key)
        elif current_game_state == PAUSED:
            handle_paused_input(e.key)
        elif current_game_state == GAME_OVER:
            if e.key == KEY_MENU:
                current_game_state = MAIN_MENU
                draw_main_menu()
