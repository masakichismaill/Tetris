import pygame

# --- 初期設定 ---
WIDTH, HEIGHT = 480, 640
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

running = True

while running:
    # --- イベント処理（閉じるボタンなど） ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- 描画 ---
    screen.fill((0, 0, 0))
    pygame.display.flip()

    clock.tick(FPS)
pygame.quit()
