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
fall_interval = 500  # ms
fall_timer = 0

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
        mino_y += 1
        fall_timer = 0

    # --- ④ 描画 ---
    screen.fill((0, 0, 0))

    # グリッド（枠線）
    for r in range(ROWS):
        for c in range(COLS):
            x = MARGIN + c * CELL
            y = MARGIN + r * CELL
            rect = pygame.Rect(x, y, CELL, CELL)
            pygame.draw.rect(screen, (40, 40, 40), rect, 1)

    # ミノ
    for dx, dy in mino_cells:
        x = MARGIN + (mino_x + dx) * CELL
        y = MARGIN + (mino_y + dy) * CELL
        rect = pygame.Rect(x, y, CELL, CELL)
        pygame.draw.rect(screen, (0, 200, 200), rect)

    pygame.display.flip()

pygame.quit()
