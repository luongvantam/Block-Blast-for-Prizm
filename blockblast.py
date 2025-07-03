from kandinsky import fill_rect, draw_string
from gint import *
from random import randint, choice

L_FENETRE = 320
H_FENETRE = 224

H_POLICE = 10
LNUM_POLICE = 8

GRID_SIZE = 8
CELL_SIZE = 28
PREVIEW_CELL_SIZE = 14

GRID_X = 0
GRID_Y = 0
BLOCK_AREA_X = GRID_X + GRID_SIZE * CELL_SIZE + 5

SMALL_LABEL_BLOCK_PADDING = 2
FIXED_GAP_BETWEEN_BLOCKS = 5

SCORE_DISPLAY_Y = 2

BLOCKS_DISPLAY_START_Y = SCORE_DISPLAY_Y + H_POLICE + 20

MENU_WIDTH = 100
MENU_HEIGHT = 60
MENU_X = (L_FENETRE - MENU_WIDTH) // 2
MENU_Y = (H_FENETRE - MENU_HEIGHT) // 2
MENU_BG_COLOR = (60, 60, 60)
MENU_TEXT_COLOR = (255, 255, 255)

COULEUR_FOND = (40, 40, 40)
COULEUR_BORD = (255, 255, 255)
COULEUR_SOL = (180, 232, 232)
COULEUR_CLEAR_HIGHLIGHT = (200, 255, 200)
COULEUR_CLEAR_PREVIEW = (255, 255, 100)
COULEUR_POTENTIAL_CLEAR = (100, 200, 255)

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
]

grid = [[COULEUR_FOND for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
score = 0
cursor_x, cursor_y = 0, 0
prev_cursor_x, prev_cursor_y = 0, 0
game_over = False
menu_open = False
menu_selection_index = 0

available_blocks = []
active_block_shape = None
active_block_color = None
selected_block_idx = -1

highlighted_rows = []
highlighted_cols = []

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
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            draw_prect(GRID_X + j * CELL_SIZE, GRID_Y + i * CELL_SIZE,
                       CELL_SIZE, CELL_SIZE, COULEUR_BORD)

def draw_current_block_preview(block, row, col, color):
    if block is None:
        return
    for i in range(3):
        for j in range(3):
            if block[i][j]:
                grid_pos_x = col + j
                grid_pos_y = row + i
                if 0 <= grid_pos_y < GRID_SIZE and 0 <= grid_pos_x < GRID_SIZE:
                    draw_prect(GRID_X + grid_pos_x * CELL_SIZE + 1, GRID_Y + grid_pos_y * CELL_SIZE + 1,
                               CELL_SIZE - 2, CELL_SIZE - 2, color)

def draw_block(block, x, y, color, cell_size_override=None):
    size = CELL_SIZE if cell_size_override is None else cell_size_override
    for i in range(3):
        for j in range(3):
            if block[i][j]:
                draw_prect(x + j * size + 1, y + i * size + 1,
                           size - 2, size - 2, color)

def draw_score():
    score_str_val = str(score)
    full_score_text = "score: " + score_str_val

    fill_rect(BLOCK_AREA_X, SCORE_DISPLAY_Y, L_FENETRE - BLOCK_AREA_X, H_POLICE + 10, COULEUR_FOND)

    draw_string(full_score_text, BLOCK_AREA_X, SCORE_DISPLAY_Y, COULEUR_BORD, COULEUR_FOND)

def draw_game_over():
    global score
    if game_over:
        fill_rect(0, 0, L_FENETRE, H_FENETRE, COULEUR_FOND)

        game_over_text = "Game Over!"
        reset_text = "[MENU] to reset"
        score_text = "Score: " + str(score)

        line_spacing = H_POLICE + 5

        total_text_height = 3 * H_POLICE + 2 * 5

        initial_y = (H_FENETRE - total_text_height) // 2

        text_width_go = LNUM_POLICE * len(game_over_text)
        text_x_go = (L_FENETRE - text_width_go) // 2
        draw_string(game_over_text, text_x_go, initial_y, COULEUR_BORD, COULEUR_FOND)

        text_width_score = LNUM_POLICE * len(score_text)
        text_x_score = (L_FENETRE - text_width_score) // 2
        draw_string(score_text, text_x_score, initial_y + line_spacing, COULEUR_BORD, COULEUR_FOND)

        text_width_reset = LNUM_POLICE * len(reset_text)
        text_x_reset = (L_FENETRE - text_width_reset) // 2
        draw_string(reset_text, text_x_reset, initial_y + 2 * line_spacing, COULEUR_BORD, COULEUR_FOND)

def draw_available_blocks():
    fill_rect(BLOCK_AREA_X, BLOCKS_DISPLAY_START_Y, L_FENETRE - BLOCK_AREA_X, H_FENETRE - BLOCKS_DISPLAY_START_Y, COULEUR_FOND)

    current_y_pos = BLOCKS_DISPLAY_START_Y

    for i, block_data in enumerate(available_blocks):
        label_y = current_y_pos

        draw_string(f"F{i+1}:", BLOCK_AREA_X, label_y, COULEUR_BORD, COULEUR_FOND)

        block_width = 3 * PREVIEW_CELL_SIZE + 2
        label_width = LNUM_POLICE * len(f"F{i+1}:")
        block_x = BLOCK_AREA_X + label_width + SMALL_LABEL_BLOCK_PADDING
        available_space = (L_FENETRE - BLOCK_AREA_X) - (label_width + SMALL_LABEL_BLOCK_PADDING)
        center_offset = max(0, (available_space - block_width) // 2)
        block_x += center_offset

        block_y = label_y + H_POLICE + SMALL_LABEL_BLOCK_PADDING
        if block_data is not None:
            draw_block(block_data['shape'], block_x, block_y, block_data['color'], PREVIEW_CELL_SIZE)
        else:
            used_text = f"F{i+1}: USED"
            used_width = LNUM_POLICE * len(used_text)
            fill_rect(BLOCK_AREA_X, label_y, used_width, H_POLICE, COULEUR_FOND)
            draw_string(used_text, BLOCK_AREA_X, label_y, COULEUR_BORD, COULEUR_FOND)
            fill_rect(block_x, block_y, 3 * PREVIEW_CELL_SIZE + 2, 3 * PREVIEW_CELL_SIZE + 2, COULEUR_FOND)

        current_y_pos += (H_POLICE + SMALL_LABEL_BLOCK_PADDING + 3 * PREVIEW_CELL_SIZE + FIXED_GAP_BETWEEN_BLOCKS)

def draw_menu():
    global menu_selection_index
    if menu_open:
        fill_rect(MENU_X, MENU_Y, MENU_WIDTH, MENU_HEIGHT, MENU_BG_COLOR)

        options = ["Replay", "Resume", "Exit"]
        line_height = H_POLICE + 5

        for i, option_text in enumerate(options):
            current_y = MENU_Y + 10 + i * line_height

            if i == menu_selection_index:
                fill_rect(MENU_X + 5, current_y - 2, MENU_WIDTH - 10, H_POLICE + 4, MENU_TEXT_COLOR)
                draw_string(option_text, MENU_X + 10, current_y, MENU_BG_COLOR, MENU_TEXT_COLOR)
            else:
                draw_string(option_text, MENU_X + 10, current_y, MENU_TEXT_COLOR, MENU_BG_COLOR)

def generate_three_blocks():
    global available_blocks, active_block_shape, active_block_color, selected_block_idx
    available_blocks = []
    for _ in range(3):
        shape_idx = randint(0, len(SHAPES) - 1)
        shape = [[0 for _ in range(3)] for _ in range(3)]
        for r in range(3):
            for c in range(3):
                if r < len(SHAPES[shape_idx]) and c < len(SHAPES[shape_idx][r]):
                    shape[r][c] = SHAPES[shape_idx][r][c]
                else:
                    shape[r][c] = 0
        color = generate_random_color()
        available_blocks.append({"shape": shape, "color": color})

    active_block_shape = None
    active_block_color = None
    selected_block_idx = -1
    draw_available_blocks()

def can_place_block(block, row, col):
    if block is None:
        return False
    for i in range(3):
        for j in range(3):
            if block[i][j]:
                grid_pos_x = col + j
                grid_pos_y = row + i
                if not (0 <= grid_pos_y < GRID_SIZE and 0 <= grid_pos_x < GRID_SIZE) or \
                   grid[grid_pos_y][grid_pos_x] != COULEUR_FOND:
                    return False
    return True

def place_block(block, row, col):
    global grid
    num_cells_placed = 0
    for i in range(3):
        for j in range(3):
            if block[i][j]:
                if 0 <= row + i < GRID_SIZE and 0 <= col + j < GRID_SIZE:
                    grid[row + i][col + j] = active_block_color
                    draw_grid_cell(row + i, col + j)
                    num_cells_placed += 1
    return num_cells_placed

def would_clear_lines(block, target_row, target_col):
    temp_grid = [row[:] for row in grid]
    potential_rows_to_clear = []
    potential_cols_to_clear = []

    for i in range(3):
        for j in range(3):
            if block[i][j]:
                r, c = target_row + i, target_col + j
                if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and temp_grid[r][c] == COULEUR_FOND:
                    temp_grid[r][c] = (1, 1, 1)
                else:
                    return [], []

    for r in range(GRID_SIZE):
        row_full = True
        for c in range(GRID_SIZE):
            if temp_grid[r][c] == COULEUR_FOND:
                row_full = False
                break
        if row_full:
            potential_rows_to_clear.append(r)

    for c in range(GRID_SIZE):
        col_full = True
        for r in range(GRID_SIZE):
            if temp_grid[r][c] == COULEUR_FOND:
                col_full = False
                break
        if col_full:
            potential_cols_to_clear.append(c)

    return potential_rows_to_clear, potential_cols_to_clear

def clear_lines():
    global score
    rows_to_clear = []
    cols_to_clear = []

    for i in range(GRID_SIZE):
        row_full = True
        for j in range(GRID_SIZE):
            if grid[i][j] == COULEUR_FOND:
                row_full = False
                break
        if row_full:
            rows_to_clear.append(i)

    for j in range(GRID_SIZE):
        col_full = True
        for i in range(GRID_SIZE):
            if grid[i][j] == COULEUR_FOND:
                col_full = False
                break
        if col_full:
            cols_to_clear.append(j)

    if rows_to_clear or cols_to_clear:
        for r in rows_to_clear:
            for c in range(GRID_SIZE):
                draw_grid_cell(r, c, COULEUR_CLEAR_HIGHLIGHT)
        for c in cols_to_clear:
            for r in range(GRID_SIZE):
                draw_grid_cell(r, c, COULEUR_CLEAR_HIGHLIGHT)

        for _ in range(20000):
            pass

        for r in rows_to_clear:
            for c in range(GRID_SIZE):
                grid[r][c] = COULEUR_FOND
                draw_grid_cell(r, c)
        for c in cols_to_clear:
            for r in range(GRID_SIZE):
                grid[r][c] = COULEUR_FOND
                draw_grid_cell(r, c)

        score += 10 * (len(rows_to_clear) + len(cols_to_clear))
        draw_score()

def can_place_any_block_from_available():
    for block_data in available_blocks:
        if block_data is not None:
            block_shape = block_data['shape']
            for r in range(GRID_SIZE):
                for c in range(GRID_SIZE):
                    if can_place_block(block_shape, r, c):
                        return True
    return False

def reset_game():
    global grid, score, cursor_x, cursor_y, game_over, prev_cursor_x, prev_cursor_y, highlighted_rows, highlighted_cols, active_block_shape, active_block_color, selected_block_idx, menu_open, menu_selection_index

    fill_rect(0, 0, L_FENETRE, H_FENETRE, COULEUR_FOND)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            grid[i][j] = COULEUR_FOND
    score = 0
    cursor_x, cursor_y = 0, 0
    prev_cursor_x, prev_cursor_y = 0, 0
    game_over = False
    highlighted_rows = []
    highlighted_cols = []
    active_block_shape = None
    active_block_color = None
    selected_block_idx = -1
    menu_open = False
    menu_selection_index = 0

    draw_initial_grid()
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            draw_grid_cell(r, c)
    generate_three_blocks()
    draw_score()

def action(key):
    global cursor_x, cursor_y, game_over, prev_cursor_x, prev_cursor_y, score, highlighted_rows, highlighted_cols, active_block_shape, active_block_color, selected_block_idx, menu_open, menu_selection_index

    if game_over and key == KEY_MENU:
        reset_game()
        return
    if game_over:
        draw_game_over()
        return

    if key == KEY_F6:
        menu_open = not menu_open
        if menu_open:
            draw_menu()
        else:
            fill_rect(MENU_X, MENU_Y, MENU_WIDTH, MENU_HEIGHT, COULEUR_FOND)
            draw_initial_grid()
            for r in range(GRID_SIZE):
                for c in range(GRID_SIZE):
                    draw_grid_cell(r, c)
            draw_score()
            draw_available_blocks()
        return

    if menu_open:
        if key == KEY_UP:
            menu_selection_index = (menu_selection_index - 1 + 3) % 3
            draw_menu()
        elif key == KEY_DOWN:
            menu_selection_index = (menu_selection_index + 1) % 3
            draw_menu()
        elif key == KEY_EXE or key == KEY_SHIFT:
            if menu_selection_index == 0:
                reset_game()
            elif menu_selection_index == 1:
                menu_open = False
                fill_rect(MENU_X, MENU_Y, MENU_WIDTH, MENU_HEIGHT, COULEUR_FOND)
                draw_initial_grid()
                for r in range(GRID_SIZE):
                    for c in range(GRID_SIZE):
                        draw_grid_cell(r, c)
                draw_score()
                draw_available_blocks()
            elif menu_selection_index == 2:
                raise SystemExit
        return

    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            draw_grid_cell(r, c)

    highlighted_rows = []
    highlighted_cols = []

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

    if key in [KEY_F1, KEY_F2, KEY_F3]:
        chosen_idx = -1
        if key == KEY_F1: chosen_idx = 0
        elif key == KEY_F2: chosen_idx = 1
        elif key == KEY_F3: chosen_idx = 2

        if 0 <= chosen_idx < len(available_blocks) and available_blocks[chosen_idx] is not None:
            active_block_shape = available_blocks[chosen_idx]['shape']
            active_block_color = available_blocks[chosen_idx]['color']
            selected_block_idx = chosen_idx
            draw_available_blocks()
        moved_cursor = True

    elif (key == KEY_EXE or key == KEY_SHIFT) and active_block_shape is not None:
        if can_place_block(active_block_shape, cursor_y, cursor_x):
            cells_placed = place_block(active_block_shape, cursor_y, cursor_x)
            score += cells_placed
            draw_score()
            clear_lines()

            available_blocks[selected_block_idx] = None
            draw_available_blocks()

            active_block_shape = None
            active_block_color = None
            selected_block_idx = -1
            cursor_x, cursor_y = 0, 0

            if all(b is None for b in available_blocks):
                generate_three_blocks()

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
                        draw_grid_cell(r, c, COULEUR_POTENTIAL_CLEAR)
                for c in highlighted_cols:
                    for r in range(GRID_SIZE):
                        draw_grid_cell(r, c, COULEUR_POTENTIAL_CLEAR)

        draw_current_block_preview(active_block_shape, cursor_y, cursor_x, current_preview_color)

    if not can_place_any_block_from_available():
        game_over = True
        draw_game_over()
        return

fill_rect(0, 0, L_FENETRE, H_FENETRE, COULEUR_FOND)
draw_initial_grid()
for r in range(GRID_SIZE):
    for c in range(GRID_SIZE):
        draw_grid_cell(r, c)
generate_three_blocks()
draw_score()

while True:
    e = pollevent()
    if e.type == KEYEV_DOWN and e.key in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, KEY_EXE, KEY_MENU, KEY_SHIFT, KEY_F1, KEY_F2, KEY_F3, KEY_F6]:
        action(e.key)
