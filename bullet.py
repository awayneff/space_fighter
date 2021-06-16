import pygame

black = (0, 0, 0)


class Bullet(pygame.sprite.Sprite):
    name = 'bullet'

    def __init__(self, color, width, height, x, y):
        super().__init__()

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Bullet initialization
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(black)
        self.image.set_colorkey(black)

        pygame.draw.rect(self.image, color, [0, 0, self.width, self.height])

        self.rect = self.image.get_rect()

        # Bullet movement
        self.rect.x = self.x
        self.rect.y = self.y

    def bulletMove(self, velocity):
        self.rect.y -= velocity
