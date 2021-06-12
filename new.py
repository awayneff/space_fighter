import pygame

pygame.init()

black = (0, 0, 0)
screenSize = (700, 600)
screen = pygame.display.set_mode(screenSize)

clock = pygame.time.Clock()

while True:
    clock.tick(60)
    screen.fill(black)
    
    
    pygame.display.flip()
    