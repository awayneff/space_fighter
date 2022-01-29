import pygame


class Player(pygame.sprite.Sprite):
    name = 'player'
    
    def __init__(self, screen):
        super().__init__()
        self.imagePath = 'assets/player.png'
        self.image_thrust_path = 'assets/player_speeding.png'
        
        self.screen = screen
        self.limit = 200

        self.image_thrust = pygame.transform.scale(pygame.image.load(self.image_thrust_path), (40, 55))
        self.image_slow = pygame.transform.scale(pygame.image.load(self.imagePath), (40, 50))
        
        self.image = self.image_slow
        self.rect = self.image.get_rect()

        

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
