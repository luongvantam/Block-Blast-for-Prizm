from kandinsky import fill_rect, draw_string
from gint import *
from random import randint

L_FENETRE = 320
H_FENETRE = 224

H_POLICE = 10
LNUM_POLICE = 8

GRID_SIZE = 8
CELL_SIZE = 28
GRID_X = 0
GRID_Y = 0
BLOCK_AREA_X = GRID_X + GRID_SIZE * CELL_SIZE + 5
BLOCK_AREA_Y = (H_FENETRE - 3 * CELL_SIZE) // 2
H_SOL = H_POLICE + 4

COULEUR_FOND = (40, 40, 40)
COULEUR_BORD = (255, 255, 255)
COULEUR_SOL = (180, 232, 232)
COULEUR_CLEAR_HIGHLIGHT = (200, 255, 200)
COULEUR_CLEAR_PREVIEW = (255, 255, 100)
COULEUR_POTENTIAL_CLEAR = (100, 200, 255)

SHAPES = [
    [[1,1,1],
     [1,1,1],
     [1,1,1]],

     [[1,1,1],
     [1,1,1],
     [0,0,0]],
     [[1,1,0],
     [1,1,0],
     [1,1,0]],

     [[1,1,0],
     [1,1,0],
     [0,0,0]],

     [[1,1,0],
     [0,0,0],
     [0,0,0]],
    [[1,0,0],
     [1,0,0],
     [0,0,0]],

     [[1,0,0],
     [1,0,0],
     [1,0,0]],
     [[1,1,1],
     [0,0,0],
     [0,0,0]],

    [[1,0,0],
     [0,0,0],
     [0,0,0]],

     [[1,0,0],
     [1,0,0],
     [1,1,0]],
     [[1,1,0],
     [1,0,0],
     [1,0,0]],
     [[1,1,1],
     [1,0,0],
     [0,0,0]],
     [[1,1,1],
     [0,0,1],
     [0,0,0]],

     [[1,1,0],
     [0,1,1],
     [0,0,0]],
     [[0,1,1],
     [1,1,0],
     [0,0,0]],
     [[1,0,0],
     [1,1,0],
     [0,1,0]],
     [[0,1,0],
     [1,1,0],
     [1,0,0]],

     [[1,0,0],
     [1,1,0],
     [1,0,0]],
     [[0,1,0],
     [1,1,1],
     [0,0,0]],
     [[0,1,0],
     [1,1,0],
     [0,1,0]],
     [[1,1,1],
     [0,1,0],
     [0,0,0]],
]

grid = [[COULEUR_FOND for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
score = 0
current_block = [[0 for _ in range(3)] for _ in range(3)]
next_block = [[0 for _ in range(3)] for _ in range(3)]
current_block_color = (0,0,0)
next_block_color = (0,0,0)

cursor_x, cursor_y = 0, 0
prev_cursor_x, prev_cursor_y = 0, 0
game_over = False
current_shape_idx = 0
next_shape_idx = 0
current_score_display = -1

highlighted_rows = []
highlighted_cols = []

def generate_random_color():
    r = randint(80, 255)
    g = randint(80, 255)
    b = randint(80, 255)
    return (r, g, b)

def get_lightened_color(rgb_tuple, amount=50):
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
            draw_grid_cell(i, j, COULEUR_FOND)

def draw_current_block_preview(block, row, col, color):
    for i in range(3):
        for j in range(3):
            if block[i][j]:
                grid_pos_x = col + j
                grid_pos_y = row + i
                if 0 <= grid_pos_y < GRID_SIZE and 0 <= grid_pos_x < GRID_SIZE:
                    draw_prect(GRID_X + grid_pos_x * CELL_SIZE + 1, GRID_Y + grid_pos_y * CELL_SIZE + 1,
                               CELL_SIZE - 2, CELL_SIZE - 2, color)

def draw_block_area_background():
    fill_rect(BLOCK_AREA_X, BLOCK_AREA_Y - H_POLICE - 5 - 1, 3 * CELL_SIZE + 50, 3 * CELL_SIZE + H_POLICE + 5 + 1, COULEUR_FOND)

def draw_block(block, x, y, color):
    for i in range(3):
        for j in range(3):
            if block[i][j]:
                draw_prect(x + j * CELL_SIZE + 1, y + i * CELL_SIZE + 1,
                           CELL_SIZE - 2, CELL_SIZE - 2, color)

def draw_score():
    global current_score_display
    if score != current_score_display:
        score_str = str(score)
        text_width = LNUM_POLICE * len(score_str)
        
        x_score = BLOCK_AREA_X
        y_score = 10
        
        fill_rect(x_score, y_score, L_FENETRE - x_score, H_POLICE, COULEUR_FOND)
        
        draw_string(score_str, x_score, y_score, COULEUR_BORD, COULEUR_FOND)
        
        current_score_display = score

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

def generate_initial_blocks():
    global current_shape_idx, current_block, next_shape_idx, next_block, current_block_color, next_block_color
    
    current_shape_idx = randint(0, len(SHAPES) - 1)
    for i in range(3):
        for j in range(3):
            if i < len(SHAPES[current_shape_idx]) and j < len(SHAPES[current_shape_idx][i]):
                current_block[i][j] = SHAPES[current_shape_idx][i][j]
            else:
                current_block[i][j] = 0
    current_block_color = generate_random_color()

    next_shape_idx = randint(0, len(SHAPES) - 1)
    for i in range(3):
        for j in range(3):
            if i < len(SHAPES[next_shape_idx]) and j < len(SHAPES[next_shape_idx][i]):
                next_block[i][j] = SHAPES[next_shape_idx][i][j]
            else:
                next_block[i][j] = 0
    next_block_color = generate_random_color()
    
    draw_block_area_background()
    draw_string("NEXT:", BLOCK_AREA_X, BLOCK_AREA_Y - H_POLICE - 5, COULEUR_BORD, COULEUR_FOND)
    draw_block(next_block, BLOCK_AREA_X, BLOCK_AREA_Y, next_block_color)

def advance_block():
    global current_block, next_block, current_shape_idx, next_shape_idx, current_block_color, next_block_color
    
    current_block = [row[:] for row in next_block]
    current_shape_idx = next_shape_idx
    current_block_color = next_block_color

    next_shape_idx = randint(0, len(SHAPES) - 1)
    for i in range(3):
        for j in range(3):
            if i < len(SHAPES[next_shape_idx]) and j < len(SHAPES[next_shape_idx][i]):
                next_block[i][j] = SHAPES[next_shape_idx][i][j]
            else:
                next_block[i][j] = 0
    next_block_color = generate_random_color()
    
    draw_block_area_background()
    draw_string("NEXT:", BLOCK_AREA_X, BLOCK_AREA_Y - H_POLICE - 5, COULEUR_BORD, COULEUR_FOND)
    draw_block(next_block, BLOCK_AREA_X, BLOCK_AREA_Y, next_block_color)

def can_place_block(block, row, col):
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
    for i in range(3):
        for j in range(3):
            if block[i][j]:
                if 0 <= row + i < GRID_SIZE and 0 <= col + j < GRID_SIZE:
                    grid[row + i][col + j] = current_block_color
                    draw_grid_cell(row + i, col + j)

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

def can_place_any_block(block_to_check):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if can_place_block(block_to_check, i, j):
                return True
    return False

def reset_game():
    global grid, score, cursor_x, cursor_y, game_over, prev_cursor_x, prev_cursor_y, highlighted_rows, highlighted_cols
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

    draw_initial_grid()
    generate_initial_blocks()

    current_preview_color = get_lightened_color(current_block_color)
    r_to_h, c_to_h = [], []
    if can_place_block(current_block, cursor_y, cursor_x):
        r_to_h, c_to_h = would_clear_lines(current_block, cursor_y, cursor_x)
        if r_to_h or c_to_h:
            current_preview_color = COULEUR_CLEAR_PREVIEW
            highlighted_rows = r_to_h
            highlighted_cols = c_to_h
            for r in highlighted_rows:
                for c in range(GRID_SIZE):
                    draw_grid_cell(r, c, COULEUR_POTENTIAL_CLEAR)
            for c in highlighted_cols:
                for r in range(GRID_SIZE):
                    draw_grid_cell(r, c, COULEUR_POTENTIAL_CLEAR)

    draw_current_block_preview(current_block, cursor_y, cursor_x, current_preview_color)
    draw_score()


def action(key):
    global cursor_x, cursor_y, game_over, prev_cursor_x, prev_cursor_y, score, highlighted_rows, highlighted_cols
    if game_over and key == KEY_MENU:
        reset_game()
        return
    if game_over:
        draw_game_over()
        return

    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            draw_grid_cell(r, c)

    highlighted_rows = []
    highlighted_cols = []

    prev_cursor_x, prev_cursor_y = cursor_x, cursor_y

    moved = False
    if key == KEY_LEFT and cursor_x > 0:
        cursor_x -= 1
        moved = True
    elif key == KEY_RIGHT and cursor_x < GRID_SIZE - 1:
        cursor_x += 1
        moved = True
    elif key == KEY_UP and cursor_y > 0:
        cursor_y -= 1
        moved = True
    elif key == KEY_DOWN and cursor_y < GRID_SIZE - 1:
        cursor_y += 1
        moved = True
    elif key == KEY_EXE or key == KEY_SHIFT:
        if can_place_block(current_block, cursor_y, cursor_x):
            place_block(current_block, cursor_y, cursor_x)
            score += 2
            draw_score()
            clear_lines()
            advance_block()
            
            cursor_x, cursor_y = 0, 0

            if not can_place_any_block(current_block):
                game_over = True
                draw_game_over()
                return
        else:
            pass

    current_preview_color = get_lightened_color(current_block_color)
    r_to_h, c_to_h = [], []

    if can_place_block(current_block, cursor_y, cursor_x):
        r_to_h, c_to_h = would_clear_lines(current_block, cursor_y, cursor_x)
        if r_to_h or c_to_h:
            current_preview_color = COULEUR_CLEAR_PREVIEW
            highlighted_rows = r_to_h
            highlighted_cols = c_to_h
            for r in highlighted_rows:
                for c in range(GRID_SIZE):
                    draw_grid_cell(r, c, COULEUR_POTENTIAL_CLEAR)
            for c in highlighted_cols:
                for r in range(GRID_SIZE):
                    draw_grid_cell(r, c, COULEUR_POTENTIAL_CLEAR)

    draw_current_block_preview(current_block, cursor_y, cursor_x, current_preview_color)

fill_rect(0, 0, L_FENETRE, H_FENETRE, COULEUR_FOND)
draw_initial_grid()
generate_initial_blocks()

current_preview_color = get_lightened_color(current_block_color)
r_to_h, c_to_h = [], []
if can_place_block(current_block, cursor_y, cursor_x):
    r_to_h, c_to_h = would_clear_lines(current_block, cursor_y, cursor_x)
    if r_to_h or c_to_h:
        current_preview_color = COULEUR_CLEAR_PREVIEW
        highlighted_rows = r_to_h
        highlighted_cols = c_to_h
        for r in highlighted_rows:
            for c in range(GRID_SIZE):
                draw_grid_cell(r, c, COULEUR_POTENTIAL_CLEAR)
        for c in highlighted_cols:
            for r in range(GRID_SIZE):
                draw_grid_cell(r, c, COULEUR_POTENTIAL_CLEAR)

draw_current_block_preview(current_block, cursor_y, cursor_x, current_preview_color)
draw_score()

while True:
    e = pollevent()
    if e.type == KEYEV_DOWN and e.key in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, KEY_EXE, KEY_MENU, KEY_SHIFT]:
        action(e.key)
    elif e.type == KEYEV_DOWN and e.key == KEY_EXIT:
        raise SystemExit
