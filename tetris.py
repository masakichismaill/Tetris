import pygame
import random

# ------------------
# 設定
# ------------------
ROWS, COLS = 20, 10
CELL = 30
MARGIN = 20

SIDE = 200
WIDTH = COLS * CELL + MARGIN * 2 + SIDE
HEIGHT = ROWS * CELL + MARGIN * 2
FPS = 60

SHAPES = {
    "I": [(0, 0), (0, 1), (0, 2), (0, 3)],
    "O": [(0, 0), (1, 0), (0, 1), (1, 1)],
    "T": [(-1, 0), (0, 0), (1, 0), (0, 1)],
    "S": [(0, 0), (1, 0), (-1, 1), (0, 1)],
    "Z": [(-1, 0), (0, 0), (0, 1), (1, 1)],
    "J": [(-1, 0), (0, 0), (1, 0), (1, 1)],
    "L": [(-1, 0), (0, 0), (1, 0), (-1, 1)],
}
COLORS = {
    "I": (0, 200, 200),
    "O": (200, 200, 0),
    "T": (180, 0, 180),
    "S": (0, 200, 0),
    "Z": (200, 0, 0),
    "J": (0, 0, 200),
    "L": (255, 140, 0),
}

# 落下（ソフトドロップ）
normal_interval = 500
soft_interval = 50
fall_interval = normal_interval
fall_timer = 0


# ------------------
# 関数
# ------------------
def can_move(mino_x, mino_y, cells, board):
    for dx, dy in cells:
        nx = mino_x + dx
        ny = mino_y + dy
        if not (0 <= nx < COLS and 0 <= ny < ROWS):
            return False
        if board[ny][nx] != 0:
            return False
    return True


def rotate_cw(cells):
    return [(-dy, dx) for dx, dy in cells]


def lock_to_board(mino_x, mino_y, cells, board, mino_kind):
    for dx, dy in cells:
        x = mino_x + dx
        y = mino_y + dy
        board[y][x] = mino_kind


def spawn_mino():
    kind = random.choice(list(SHAPES.keys()))
    cells = SHAPES[kind][:]  # 念のためコピー
    x = COLS // 2
    y = 0
    return x, y, cells, kind


def clear_lines(board):
    new_board = []
    cleared = 0
    for r in range(ROWS):
        if 0 not in board[r]:
            cleared += 1
        else:
            new_board.append(board[r])
    for _ in range(cleared):
        new_board.insert(0, [0] * COLS)
    return new_board, cleared


def try_rotate(mino_x, mino_y, cells, board):
    rotated = rotate_cw(cells)
    for dx, dy in [(0, 0), (-1, 0), (1, 0)]:
        if can_move(mino_x + dx, mino_y + dy, rotated, board):
            return mino_x + dx, mino_y + dy, rotated
    return mino_x, mino_y, cells


# ゴーストのY座標を計算する関数
def get_ghost_y(mino_x, mino_y, cells, board):
    gy = mino_y
    while can_move(mino_x, gy + 1, cells, board):
        gy += 1
    return gy


def add_score(score, cleared):
    if cleared == 1:
        return score + 100
    if cleared == 2:
        return score + 300
    if cleared == 3:
        return score + 500
    if cleared == 4:
        return score + 800
    return score


# ------------------
# 初期化
# ------------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)

board = [[0] * COLS for _ in range(ROWS)]
score = 0

# NEXTを先に作って、現在ミノに採用
next_x, next_y, next_cells, next_kind = spawn_mino()
mino_x, mino_y, mino_cells, mino_kind = next_x, next_y, next_cells, next_kind
next_x, next_y, next_cells, next_kind = spawn_mino()

running = True
while running:
    # ------------------
    # ① 入力
    # ------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if can_move(mino_x - 1, mino_y, mino_cells, board):
                    mino_x -= 1

            elif event.key == pygame.K_RIGHT:
                if can_move(mino_x + 1, mino_y, mino_cells, board):
                    mino_x += 1

            elif event.key == pygame.K_UP:
                if mino_kind != "O":
                    mino_x, mino_y, mino_cells = try_rotate(
                        mino_x, mino_y, mino_cells, board
                    )

            elif event.key == pygame.K_DOWN:
                fall_interval = soft_interval

            elif event.key == pygame.K_SPACE:
                # ハードドロップ：行けるだけ下へ
                while can_move(mino_x, mino_y + 1, mino_cells, board):
                    mino_y += 1

                # 固定 → 行消し → スコア → 次ミノ
                lock_to_board(mino_x, mino_y, mino_cells, board, mino_kind)
                board, cleared = clear_lines(board)
                score = add_score(score, cleared)

                mino_x, mino_y, mino_cells, mino_kind = (
                    next_x,
                    next_y,
                    next_cells,
                    next_kind,
                )
                next_x, next_y, next_cells, next_kind = spawn_mino()

                if not can_move(mino_x, mino_y, mino_cells, board):
                    running = False

                fall_timer = 0  # 落下タイマーをリセット

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                fall_interval = normal_interval

    # ------------------
    # ② 時間（dt）
    # ------------------
    dt = clock.tick(FPS)
    fall_timer += dt

    # ------------------
    # ③ 自動落下
    # ------------------
    if fall_timer >= fall_interval:
        if can_move(mino_x, mino_y + 1, mino_cells, board):
            mino_y += 1
        else:
            # 固定 → 行消し → スコア → 次ミノ
            lock_to_board(mino_x, mino_y, mino_cells, board, mino_kind)
            board, cleared = clear_lines(board)
            score = add_score(score, cleared)

            mino_x, mino_y, mino_cells, mino_kind = (
                next_x,
                next_y,
                next_cells,
                next_kind,
            )
            next_x, next_y, next_cells, next_kind = spawn_mino()

            if not can_move(mino_x, mino_y, mino_cells, board):
                running = False

        fall_timer = 0

    # ------------------
    # ④ 描画
    # ------------------
    screen.fill((0, 0, 0))

    # 盤面（固定ブロック + 枠線）
    for r in range(ROWS):
        for c in range(COLS):
            x = MARGIN + c * CELL
            y = MARGIN + r * CELL
            rect = pygame.Rect(x, y, CELL, CELL)
            if board[r][c] != 0:
                pygame.draw.rect(screen, COLORS[board[r][c]], rect)
            pygame.draw.rect(screen, (40, 40, 40), rect, 1)
    ghost_y = get_ghost_y(mino_x, mino_y, mino_cells, board)
    for dx, dy in mino_cells:
        x = MARGIN + (mino_x + dx) * CELL
        y = MARGIN + (ghost_y + dy) * CELL
        rect = pygame.Rect(x, y, CELL, CELL)
        pygame.draw.rect(screen, COLORS[mino_kind], rect, 2)

    # 落下中ミノ
    for dx, dy in mino_cells:
        x = MARGIN + (mino_x + dx) * CELL
        y = MARGIN + (mino_y + dy) * CELL
        rect = pygame.Rect(x, y, CELL, CELL)
        pygame.draw.rect(screen, COLORS[mino_kind], rect)

    # 右パネル（SCORE / NEXT）
    panel_x = MARGIN + COLS * CELL + 40
    panel_y = MARGIN

    score_surf = font.render(f"SCORE: {score}", True, (255, 255, 255))
    screen.blit(score_surf, (panel_x, panel_y))

    next_surf = font.render("NEXT", True, (255, 255, 255))
    screen.blit(next_surf, (panel_x, panel_y + 40))

    preview_x = panel_x
    preview_y = panel_y + 80
    for dx, dy in next_cells:
        px = preview_x + (dx + 2) * CELL
        py = preview_y + (dy + 1) * CELL
        rect = pygame.Rect(px, py, CELL, CELL)
        pygame.draw.rect(screen, COLORS[next_kind], rect)
        pygame.draw.rect(screen, (40, 40, 40), rect, 1)

    pygame.display.flip()

pygame.quit()
