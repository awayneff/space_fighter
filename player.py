import pygame


class Player(pygame.sprite.Sprite):
    name = 'player'
    
    def __init__(self, screen):
        super().__init__()
        self.imagePath = 'sprites/sprite.png'
        
        self.screen = screen
        self.limit = 200

        self.image = pygame.image.load(self.imagePath)
        self.rect = self.image.get_rect()

        pygame.draw.rect(screen, 'black', self.rect, 1)

    def update(self):
        self.screen.blit(self.image, self.rect)

    def moveY(self, pixels):
        self.rect.y += pixels

        if self.rect.y >= self.screen.get_height() - self.image.get_height():
            self.rect.y = self.screen.get_height() - self.image.get_height()

        if self.rect.y <= self.limit:
            self.rect.y = self.limit

    def moveX(self, pixels):
        self.rect.x += pixels

        if self.rect.x > self.screen.get_width() + self.image.get_width():
            self.rect.x = -self.image.get_width()

        if self.rect.x < -self.image.get_width():
            self.rect.x = self.screen.get_width() + self.image.get_width()
