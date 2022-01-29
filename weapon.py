import pygame

black = (0, 0, 0)
rocket_img = "assets/rocket.png"

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
        
class Rocket(pygame.sprite.Sprite):
    name = "rocket"
    
    def __init__(self, x, y) -> None:
        super().__init__()
        self.image = pygame.image.load(rocket_img)
        self.image = pygame.transform.rotate(self.image, 90)
        self.image = pygame.transform.scale(self.image, (10, 10))
        
        self.rect = self.image.get_rect()
        
        # Bullet movement
        self.rect.x = x
        self.rect.y = y
    
    def rocket_move(self, velocity):
        self.rect.y -= velocity