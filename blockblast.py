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
COULEUR_CURSOR = (0, 255, 0)

SHAPES = [
    [[1, 1, 0], [0, 1, 0], [0, 0, 0]],
    [[1, 1, 1], [0, 0, 0], [0, 0, 0]],
    [[1, 0, 0], [1, 0, 0], [1, 0, 0]],
    [[1, 1, 0], [1, 1, 0], [0, 0, 0]],
    [[1, 0, 0], [1, 1, 0], [0, 0, 0]],
    [[0, 1, 0], [1, 1, 0], [0, 0, 0]],
    [[0, 0, 1], [1, 1, 0], [0, 0, 0]],
    [[1, 1, 1], [0, 1, 0], [0, 0, 0]],
    [[1, 1, 1], [1, 0, 0], [0, 0, 0]],
    [[1, 0, 0], [1, 1, 1], [0, 0, 0]],
    [[0, 0, 1], [1, 1, 1], [0, 0, 0]],
    [[0, 1, 0], [0, 1, 0], [1, 1, 0]],
    [[1, 1, 0], [1, 0, 0], [1, 0, 0]],
    [[0, 1, 1], [1, 1, 0], [0, 0, 0]],
    [[1, 1, 0], [0, 1, 1], [0, 0, 0]],
    [[0, 1, 0], [1, 1, 1], [0, 0, 0]],
    [[1, 0, 1], [0, 1, 0], [0, 0, 0]],
    [[1, 1, 0], [0, 1, 0], [0, 1, 0]],
    [[0, 1, 0], [1, 1, 0], [0, 1, 0]],
    [[1, 1, 1], [1, 1, 0], [0, 0, 0]],
    [[1, 0, 0], [1, 1, 1], [0, 0, 1]]
]

grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
score = 0
current_block = [[0 for _ in range(3)] for _ in range(3)]
cursor_x, cursor_y = 0, 0
game_over = False
current_shape_idx = 0


def draw_prect(x, y, w, h, c):
    """Vẽ rectangle bằng fill_rect."""
    fill_rect(x, y, w, h, c)

def draw_grid():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            draw_prect(GRID_X + j * CELL_SIZE, GRID_Y + i * CELL_SIZE, 
                      CELL_SIZE, CELL_SIZE, COULEUR_BORD)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            color = COULEUR_BLOCK if grid[i][j] == 1 else COULEUR_FOND
            draw_prect(GRID_X + j * CELL_SIZE + 1, GRID_Y + i * CELL_SIZE + 1, 
                      CELL_SIZE - 2, CELL_SIZE - 2, color)
    if not game_over:
        draw_prect(GRID_X + cursor_x * CELL_SIZE + 1, GRID_Y + cursor_y * CELL_SIZE + 1, 
                  CELL_SIZE - 2, CELL_SIZE - 2, COULEUR_CURSOR)

def draw_block(block, x, y):
    for i in range(3):
        for j in range(3):
            if block[i][j]:
                draw_prect(x + j * CELL_SIZE + 1, y + i * CELL_SIZE + 1, 
                          CELL_SIZE - 2, CELL_SIZE - 2, COULEUR_BLOCK)

def draw_score():
    score_str = "Score: " + str(score)
    l_score = LNUM_POLICE * len(str(score)) + 7 * LNUM_POLICE
    x_score = BLOCK_AREA_X
    y_score = 10
    draw_prect(x_score, y_score, l_score, H_POLICE, COULEUR_SOL)
    draw_string(score_str, x_score, y_score, COULEUR_BORD, COULEUR_SOL)

def draw_game_over():
    if game_over:
        draw_string("Game Over! [MENU] to reset", GRID_X + 20, GRID_Y + GRID_SIZE * CELL_SIZE // 2, 
                   COULEUR_BORD, COULEUR_FOND)

def generate_block():
    global current_shape_idx, current_block
    current_shape_idx = randint(0, 3)
    for i in range(3):
        for j in range(3):
            current_block[i][j] = SHAPES[current_shape_idx][i][j]

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

def clear_lines():
    global score
    rows_cleared = 0
    cols_cleared = 0
    rows_to_clear = [0] * GRID_SIZE
    cols_to_clear = [0] * GRID_SIZE
    
    for i in range(GRID_SIZE):
        row_full = all(grid[i][j] for j in range(GRID_SIZE))
        col_full = all(grid[j][i] for j in range(GRID_SIZE))
        if row_full:
            rows_to_clear[i] = 1
        if col_full:
            cols_to_clear[i] = 1
    
    for i in range(GRID_SIZE):
        if rows_to_clear[i]:
            for j in range(GRID_SIZE):
                grid[i][j] = 0
            rows_cleared += 1
        if cols_to_clear[i]:
            for j in range(GRID_SIZE):
                grid[j][i] = 0
            cols_cleared += 1
    
    score += 10 * (rows_cleared + cols_cleared)

def can_place_any_block():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if can_place_block(current_block, i, j):
                return True
    return False

def reset_game():
    global grid, score, cursor_x, cursor_y, game_over
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            grid[i][j] = 0
    score = 0
    cursor_x, cursor_y = 0, 0
    game_over = False
    generate_block()

def draw_jeu():
    fill_rect(0, 0, L_FENETRE, H_FENETRE, COULEUR_FOND)
    draw_grid()
    draw_block(current_block, BLOCK_AREA_X, BLOCK_AREA_Y)
    draw_score()
    draw_game_over()

def action(key):
    global cursor_x, cursor_y, game_over
    if game_over and key == KEY_MENU:
        reset_game()
        return
    if game_over:
        return
    
    if key == KEY_LEFT and cursor_x > 0: cursor_x -= 1
    elif key == KEY_RIGHT and cursor_x < GRID_SIZE - 1: cursor_x += 1
    elif key == KEY_UP and cursor_y > 0: cursor_y -= 1
    elif key == KEY_DOWN and cursor_y < GRID_SIZE - 1: cursor_y += 1
    elif key == KEY_EXE or key == KEY_SHIFT and can_place_block(current_block, cursor_y, cursor_x):
        place_block(current_block, cursor_y, cursor_x)
        clear_lines()
        generate_block()
        if not can_place_any_block():
            game_over = True

generate_block()
draw_jeu()

while True:
    e = pollevent()
    if e.type == KEYEV_DOWN and e.key in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, KEY_EXE, KEY_MENU, KEY_SHIFT]:
        action(e.key)
        draw_jeu()
    elif e.type == KEYEV_DOWN and e.key == KEY_EXIT:
        raise SystemExit
