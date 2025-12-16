import pygame
import random

# --- 初期設定 ---
ROWS, COLS = 20, 10
CELL = 30
MARGIN = 20

WIDTH = COLS * CELL + MARGIN * 2
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


# 回転関数
def rotate_cw(cells):
    # ClockWise(時計回り)
    return [(-dy, dx) for dx, dy in cells]


# 固定する関数
def lock_to_board(mino_x, mino_y, cells, board):
    for dx, dy in cells:
        x = mino_x + dx
        y = mino_y + dy
        board[y][x] = 1  # board[y][x] = 1 はそこにブロックがあるという意味


# ミノをリセットする関数。新規のミノの形成
def spawn_mino():
    kind = random.choice(list(SHAPES.keys()))
    cells = SHAPES[kind]
    x = COLS // 2  # ミノの初期座標
    y = 0
    return x, y, cells, kind


# 行が埋まっているかの判定
# 行消し＝＞配列の削除＋上に空行を追加
def clear_lines(board, ROWS, COLS):
    new_board = []
    cleared = 0

    for r in range(ROWS):
        if 0 not in board[r]:
            cleared += 1  # 消えた行を数える
        else:
            new_board.append(board[r])
    # 消えた行の数だけ、上に空行を足す
    for _ in range(cleared):
        new_board.insert(0, [0] * COLS)
    return new_board, cleared


# 回転＋ウォールキック関数
def try_rotate(mino_x, mino_y, cells, board, ROWS, COLS):
    rotated = rotate_cw(cells)
    for dx, dy in [(0, 0), (-1, 0), (1, 0)]:
        if can_move(mino_x + dx, mino_y + dy, rotated, board, ROWS, COLS):
            return mino_x + dx, mino_y + dy, rotated
    # どれもダメなら回転失敗（元のまま）
    return mino_x, mino_y, cells


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

# 盤面データ
board = [[0] * COLS for _ in range(ROWS)]
# 最初のミノを生成
mino_x, mino_y, mino_cells, mino_kind = spawn_mino()
running = True
while running:
    # --- ① イベント処理（入力） ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if can_move(mino_x - 1, mino_y, mino_cells, board, ROWS, COLS):
                    mino_x -= 1
            elif event.key == pygame.K_RIGHT:
                if can_move(mino_x + 1, mino_y, mino_cells, board, ROWS, COLS):
                    mino_x += 1
            elif event.key == pygame.K_UP:
                if mino_kind != "O":
                    mino_x, mino_y, mino_cells = try_rotate(
                        mino_x, mino_y, mino_cells, board, ROWS, COLS
                    )

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
            lock_to_board(mino_x, mino_y, mino_cells, board)  # 固定
            board, _ = clear_lines(board, ROWS, COLS)  # 行消し
            mino_x, mino_y, mino_cells, mino_kind = spawn_mino()  # 新しいミノを作る
            if not can_move(mino_x, mino_y, mino_cells, board, ROWS, COLS):
                running = False
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
