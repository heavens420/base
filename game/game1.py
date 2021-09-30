import pygame

pygame.init()

screen = pygame.display.set_mode((500, 600))
clock = pygame.time.Clock()

FPS = 60
running = True

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255))
    pygame.display.update()
