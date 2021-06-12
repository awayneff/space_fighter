import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, color, width, height, velocity):
        super().__init__()
        
        self.image = pygame.Surface([width, height])
        self.image.fill('white')
        self.image.set_colorkey('white')
        
        self.velocity = velocity
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        
        rect = pygame.get_rect()
        
    def moveUp(self, pixels):
        
        
        
