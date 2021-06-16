import pygame
from random import randint

black = (0, 0, 0)


class Enemy(pygame.sprite.Sprite):
    name = 'enemy'

    def __init__(self, screen, color, width, height):
        super().__init__()

        self.imagePath = 'sprites/enemy.png'
        self.image = pygame.image.load(self.imagePath)
        
        self.rect = self.image.get_rect()
        self.rect.x = randint(self.image.get_width(),
                              screen.get_width() - self.image.get_width())
        self.rect.y = -self.image.get_height()

    def enemyMove(self, velocity):
        self.rect.y += velocity
