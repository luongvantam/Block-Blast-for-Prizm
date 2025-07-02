from kandinsky import fill_rect, draw_string
from gint import *
from random import randint

L_FENETRE = 396 
H_FENETRE = 224 

LNUMH_POLICE = {"small": (8, 10), "medium": (12, 17), "large": (18, 23)}
POLICE = "small"
H_POLICE = LNUMH_POLICE[POLICE][1]
LNUM_POLICE = LNUMH_POLICE[POLICE][0]

GRID_SIZE = 8
CELL_SIZE = 28
GRID_X = 0
GRID_Y = 0
BLOCK_AREA_X = GRID_X + GRID_SIZE * CELL_SIZE + 5
BLOCK_AREA_Y = (H_FENETRE - 3 * CELL_SIZE) // 2
H_SOL = H_POLICE + 4
H_FOND = H_FENETRE - H_SOL

COULEUR_BORD = (128, 128, 128)
COULEUR_FOND = (138, 43, 226)
COULEUR_SOL = (180, 232, 232)
COULEUR_BLOCK = (255, 255, 255)
COULEUR_PREVIEW = (150, 255, 150)

SHAPES = [
    [[1, 1, 1], [0, 0, 0], [0, 0, 0]],
    [[1, 1], [1, 1]],
    [[1, 0, 0], [1, 1, 1], [0, 0, 0]],
    [[0, 0, 1], [1, 1, 1], [0, 0, 0]],
    [[0, 1, 0], [1, 1, 1], [0, 0, 0]],
    [[0, 1, 1], [1, 1, 0], [0, 0, 0]],
    [[1, 1, 0], [0, 1, 1], [0, 0, 0]]
]

grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
score = 0
current_block = [[0 for _ in range(3)] for _ in range(3)]
cursor_x, cursor_y = 0, 0
prev_cursor_x, prev_cursor_y = 0, 0
game_over = False
current_shape_idx = 0
current_score_display = -1

def draw_prect(x, y, w, h, c):
    fill_rect(x, y, w, h, c)

def draw_grid_cell(row, col):
    color = COULEUR_BLOCK if grid[row][col] == 1 else COULEUR_FOND
    draw_prect(GRID_X + col * CELL_SIZE + 1, GRID_Y + row * CELL_SIZE + 1, 
               CELL_SIZE - 2, CELL_SIZE - 2, color)

def draw_initial_grid():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            draw_prect(GRID_X + j * CELL_SIZE, GRID_Y + i * CELL_SIZE, 
                      CELL_SIZE, CELL_SIZE, COULEUR_BORD)
            draw_grid_cell(i, j)

def draw_preview_block(block, row, col, color):
    for i in range(3):
        for j in range(3):
            if block[i][j]:
                grid_pos_x = col + j
                grid_pos_y = row + i
                if 0 <= grid_pos_y < GRID_SIZE and 0 <= grid_pos_x < GRID_SIZE and grid[grid_pos_y][grid_pos_x] == 0:
                    draw_prect(GRID_X + grid_pos_x * CELL_SIZE + 1, GRID_Y + grid_pos_y * CELL_SIZE + 1, 
                               CELL_SIZE - 2, CELL_SIZE - 2, color)

def clear_preview_block(block, row, col):
    for i in range(3):
        for j in range(3):
            if block[i][j]:
                grid_pos_x = col + j
                grid_pos_y = row + i
                if 0 <= grid_pos_y < GRID_SIZE and 0 <= grid_pos_x < GRID_SIZE:
                    draw_grid_cell(grid_pos_y, grid_pos_x)

def draw_block_area_background():
    fill_rect(BLOCK_AREA_X, BLOCK_AREA_Y, 3 * CELL_SIZE, 3 * CELL_SIZE, COULEUR_FOND)

def draw_block(block, x, y):
    for i in range(3):
        for j in range(3):
            if block[i][j]:
                draw_prect(x + j * CELL_SIZE + 1, y + i * CELL_SIZE + 1, 
                          CELL_SIZE - 2, CELL_SIZE - 2, COULEUR_BLOCK)

def draw_score():
    global current_score_display
    if score != current_score_display:
        score_str = "Score: " + str(score)
        l_score = LNUM_POLICE * len(score_str) 
        x_score = BLOCK_AREA_X
        y_score = 10
        draw_prect(x_score, y_score, l_score, H_POLICE, COULEUR_SOL)
        draw_string(score_str, x_score, y_score, COULEUR_BORD, COULEUR_SOL)
        current_score_display = score

def draw_game_over():
    if game_over:
        fill_rect(0, 0, L_FENETRE, H_FENETRE, COULEUR_FOND) 
        draw_string("Game Over! [MENU] to reset", GRID_X + 20, GRID_Y + GRID_SIZE * CELL_SIZE // 2, 
                   COULEUR_BORD, COULEUR_FOND)

def generate_block():
    global current_shape_idx, current_block
    draw_block_area_background()
    current_shape_idx = randint(0, len(SHAPES) - 1)
    for i in range(3):
        for j in range(3):
            current_block[i][j] = SHAPES[current_shape_idx][i][j]
    draw_block(current_block, BLOCK_AREA_X, BLOCK_AREA_Y)

def can_place_block(block, row, col):
    for i in range(3):
        for j in range(3):
            if block[i][j]:
                grid_pos_x = col + j
                grid_pos_y = row + i
                if (grid_pos_y >= GRID_SIZE or grid_pos_x >= GRID_SIZE or 
                    grid_pos_y < 0 or grid_pos_x < 0 or grid[grid_pos_y][grid_pos_x]):
                    return False
    return True

def place_block(block, row, col):
    global grid
    for i in range(3):
        for j in range(3):
            if block[i][j]:
                grid[row + i][col + j] = 1
                draw_grid_cell(row + i, col + j)

def clear_lines():
    global score
    rows_cleared = 0
    cols_cleared = 0
    
    for i in range(GRID_SIZE):
        row_full = True
        for j in range(GRID_SIZE):
            if grid[i][j] == 0:
                row_full = False
                break
        if row_full:
            for j in range(GRID_SIZE):
                grid[i][j] = 0
                draw_grid_cell(i, j)
            rows_cleared += 1
    
    for j in range(GRID_SIZE):
        col_full = True
        for i in range(GRID_SIZE):
            if grid[i][j] == 0:
                col_full = False
                break
        if col_full:
            for i in range(GRID_SIZE):
                grid[i][j] = 0
                draw_grid_cell(i, j)
            cols_cleared += 1
    
    if rows_cleared > 0 or cols_cleared > 0:
        score += 10 * (rows_cleared + cols_cleared)
        draw_score()

def can_place_any_block():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if can_place_block(current_block, i, j):
                return True
    return False

def reset_game():
    global grid, score, cursor_x, cursor_y, game_over, prev_cursor_x, prev_cursor_y
    fill_rect(0, 0, L_FENETRE, H_FENETRE, COULEUR_FOND)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            grid[i][j] = 0
    score = 0
    cursor_x, cursor_y = 0, 0
    prev_cursor_x, prev_cursor_y = 0, 0
    game_over = False
    draw_initial_grid()
    generate_block()
    draw_score()
    draw_preview_block(current_block, cursor_y, cursor_x, COULEUR_PREVIEW)

def action(key):
    global cursor_x, cursor_y, game_over, prev_cursor_x, prev_cursor_y
    if game_over and key == KEY_MENU:
        reset_game()
        return
    if game_over:
        return
    
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
            clear_preview_block(current_block, cursor_y, cursor_x)
            place_block(current_block, cursor_y, cursor_x)
            clear_lines()
            generate_block()
            if not can_place_any_block():
                game_over = True
            draw_game_over()
            draw_preview_block(current_block, cursor_y, cursor_x, COULEUR_PREVIEW)
        
    if moved:
        clear_preview_block(current_block, prev_cursor_y, prev_cursor_x)
        draw_preview_block(current_block, cursor_y, cursor_x, COULEUR_PREVIEW)

fill_rect(0, 0, L_FENETRE, H_FENETRE, COULEUR_FOND)
draw_initial_grid()
generate_block()
draw_score()
draw_preview_block(current_block, cursor_y, cursor_x, COULEUR_PREVIEW)

while True:
    e = pollevent()
    if e.type == KEYEV_DOWN and e.key in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, KEY_EXE, KEY_MENU, KEY_SHIFT]:
        action(e.key)
    elif e.type == KEYEV_DOWN and e.key == KEY_EXIT:
        raise SystemExit
