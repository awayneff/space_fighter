import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()

        self.screen = screen

        self.image = pygame.image.load('sprite.png')
        self.rect = self.image.get_rect()
        
        pygame.draw.rect(screen, 'black', self.rect, 1)
    
    def update(self):
        self.screen.blit(self.image, self.rect)
        
    def moveY(self, pixels):
        self.rect.y += pixels

        if self.rect.y >= self.screen.get_height():
            self.rect.y = self.screen.get_height()

        if self.rect.y <= 200:
            self.rect.y = 200
            
        print(self.rect.x, self.rect.y)
