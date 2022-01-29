import pygame
from random import randint

black = (0, 0, 0)


class Enemy(pygame.sprite.Sprite):
    name = 'enemy'

    def __init__(self, screen):
        super().__init__()

        self.default_img_path = 'assets/enemy.png'

        self.default_image = pygame.transform.scale(
            pygame.image.load(self.default_img_path), (30, 40))

        self.image = pygame.transform.rotate(self.default_image, 180)
        self.rect = self.image.get_rect()
        self.rect.x = randint(self.image.get_width(),
                              screen.get_width() - self.image.get_width())
        self.rect.y = -self.image.get_height()

    def enemyMove(self, velocity):
        self.rect.y += velocity
