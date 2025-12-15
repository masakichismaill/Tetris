from tkinter.tix import ROW
import pygame

# --- 初期設定 ---
ROWS, COLS = 20, 10
CELL = 30
MARGIN = 20

WIDTH = COLS * CELL + MARGIN * 2
HEIGHT = ROWS * CELL + MARGIN * 2
FPS = 60

# ミノの設定
mino_x = COLS // 2
mino_y = 0
mino_cells = [(0, 0), (0, 1), (0, 2), (0, 3)]  # 縦のIミノ

# 落下の設定
fall_interval = 500  # 500msごとに落下
fall_timer = 0  # 溜まった時間


# ------------------
# 　関数群
# ------------------
# 衝突判定関数
def can_move(mino_x, mino_y, cells, board, ROWS, COLS):
    for dx, dy in cells:
        # nx,ny:次の位置(next x/y)
        nx = mino_x + dx
        ny = mino_y + dy
        # 盤面の外に出るならNG
        if not (0 <= nx < COLS and 0 <= ny < ROWS):
            return False
        # 盤面にブロックがあるならNG（今回はまだ全部0なので将来用）
        if board[ny][nx] != 0:
            return False
    return True


# 固定する関数
def lock_to_board(mino_x, mino_y, cells, board):
    for dx, dy in cells:
        x = mino_x + dx
        y = mino_y + dy
        board[y][x] = 1  # board[y][x] = 1 はそこにブロックがあるという意味


# ミノをリセットする関数
def spawn_mino():
    x = COLS // 2
    y = 0
    cells = [(0, 0), (0, 1), (0, 2), (0, 3)]
    return x, y, cells


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

# 盤面データ
board = [[0] * COLS for _ in range(ROWS)]

running = True
while running:
    # --- ① イベント処理（入力） ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if mino_x > 0:
                    mino_x -= 1
            elif event.key == pygame.K_RIGHT:
                if mino_x < COLS - 1:
                    mino_x += 1

    # --- ② 時間更新（dt） ---
    dt = clock.tick(FPS)  # 前フレームからの経過ms
    fall_timer += dt

    # --- ③ 落下判定（毎フレーム） ---
    if fall_timer >= fall_interval:
        # １マス下に行けるか？
        if can_move(mino_x, mino_y + 1, mino_cells, board, ROWS, COLS):
            mino_y += 1
        else:
            # 着地：盤面に固定
            lock_to_board(mino_x, mino_y, mino_cells, board)
            # 新しいミノを作る
            mino_x, mino_y, mino_cells = spawn_mino()
        # 行けないなら止める（今回は固定まではしない）
        fall_timer = 0

    # --- ④ 描画 ---
    screen.fill((0, 0, 0))

    # グリッド（枠線）
    for r in range(ROWS):
        for c in range(COLS):
            x = MARGIN + c * CELL
            y = MARGIN + r * CELL
            rect = pygame.Rect(x, y, CELL, CELL)
            # 固定ブロックがあれば塗る
            if board[r][c] == 1:
                pygame.draw.rect(screen, (200, 200, 200), rect)
            pygame.draw.rect(screen, (40, 40, 40), rect, 1)

    # ミノ
    for dx, dy in mino_cells:
        x = MARGIN + (mino_x + dx) * CELL
        y = MARGIN + (mino_y + dy) * CELL
        rect = pygame.Rect(x, y, CELL, CELL)
        pygame.draw.rect(screen, (0, 200, 200), rect)

    pygame.display.flip()

pygame.quit()
