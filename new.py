import pygame
from player import Player

pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
screenSize = (700, 600)
screen = pygame.display.set_mode(screenSize)

clock = pygame.time.Clock()

pl = Player(screen)
pl.rect.x = screen.get_width() // 2

while True:
    clock.tick(60)
    screen.fill(white)
    
    key = pygame.key.get_pressed()
    
    if key[pygame.K_w]:
        pl.moveY(5)
    if key[pygame.K_s]:
        pl.moveY(-5)
    
    pl.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
    
    pl.draw(screen)
    pygame.display.flip()
    