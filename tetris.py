import pygame

# --- 初期設定 ---
ROWS, COLS = 20, 10
CELL = 30
MARGIN = 20

WIDTH, HEIGHT = 480, 640
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

# 盤面データ
board = [[0] * COLS for _ in range(ROWS)]

running = True
while running:
    # --- イベント処理 ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- 描画 ---
    screen.fill((0, 0, 0))

    # 盤面のマス目を描く
    for r in range(ROWS):
        for c in range(COLS):
            x = MARGIN + c * CELL
            y = MARGIN + r * CELL
            rect = pygame.Rect(x, y, CELL, CELL)
            pygame.draw.rect(screen, (40, 40, 40), rect, 1)

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
