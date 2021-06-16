import pygame
import ui
from ui import Text
from player import Player
from bullet import Bullet
from enemy import Enemy


# Variables initialization
def init():
    global enCount, incrNum, enBulCount, hp, score, pl, screen, spritesList

    enCount, incrNum = 0, 150
    enBulCount = 0
    # Setup  hp
    hp = 5

    score = 0

    pl.rect.x, pl.rect.y = (
        (screen.get_width() - pl.image.get_width()) // 2, screen.get_height() - 200)

    for sprite in spritesList:
        if sprite.name != 'player':
            spritesList.remove(sprite)


# Delete bullet or enemy if it exceededs the limit
def checker():
    global spritesList, screen, hp

    sprites = spritesList.sprites()
    delSprites = []

    for sprite in sprites:
        if sprite.rect.y <= 0 and sprite.name == 'bullet':
            delSprites.append(sprite)

        if sprite.rect.y >= screen.get_height() and sprite.name == 'enemyBullet':
            delSprites.append(sprite)

    for sprite in sprites:
        if sprite.rect.y >= screen.get_height() + sprite.image.get_height()\
                and sprite.name == 'enemy':
            delSprites.append(sprite)
            hpSound.play()
            hp -= 1

    spritesList.remove(delSprites)


# Enemies generation with decreasing interval and enemy bullet shooting
def enemyGenerator():
    global enCount, enBulCount, incrNum, spritesList

    enemies = []
    enCount += 1
    enBulCount += 1

    for sprite in spritesList.sprites():
        if sprite.name == 'enemy':
            enemies.append(sprite)

    if enCount == incrNum:
        spritesList.add(Enemy(screen, white, 30, 30))

        if incrNum > 35:
            incrNum -= 5
        enCount = 0

    for enemy in enemies:
        if enBulCount >= 80:
            shotSound.play()
            bullet = Bullet(white, 5, 5, enemy.rect.x +
                            enemy.image.get_width() // 2, enemy.rect.y + 40)
            bullet.name = 'enemyBullet'

            spritesList.add(bullet)
            enBulCount = 0


# Destroy enemy, bullet or player on collision
def kill():
    global spritesList, score, hp

    sprites = spritesList.sprites()
    delSprites = []

    for sprite in sprites:
        for enemySprite in sprites:
            # Enemy kill
            if pygame.sprite.collide_mask(sprite, enemySprite) and sprite.name == 'bullet' and enemySprite.name == 'enemy':
                delSprites.append(enemySprite)
                delSprites.append(sprite)
                score += 1
                killSound.play()

            # Destroy enemy bullet by player's
            if pygame.sprite.collide_mask(sprite, enemySprite) and sprite.name == 'bullet' and enemySprite.name == 'enemyBullet':
                delSprites.append(enemySprite)
                delSprites.append(sprite)

            # Player damage/ kill by collision with the enemy
            if pygame.sprite.collide_mask(sprite, enemySprite) and sprite.name == 'player' and enemySprite.name == 'enemy':
                delSprites.append(enemySprite)
                hpSound.play()
                hp -= 1

            # Player damage/ kill by bullet
            if pygame.sprite.collide_mask(sprite, enemySprite) and sprite.name == 'player' and enemySprite.name == 'enemyBullet':
                delSprites.append(enemySprite)
                hpSound.play()
                hp -= 1

    spritesList.remove(delSprites)


# Pygame stuff
black = (0, 0, 0)
white = (255, 255, 255)
screenSize = (700, 600)

pygame.init()
screen = pygame.display.set_mode(screenSize)
clock = pygame.time.Clock()

# Player initialization
pl = Player(screen)
pl.rect.x = (screen.get_width() - pl.image.get_width()) // 2
pl.rect.y = pl.limit
velocity = 4

# Sprites list initialization
spritesList = pygame.sprite.Group()
spritesList.add(pl)

init()

# DEBUGGING
ls = []

# Death state
state = False

# UI
scoreText = Text(screen, str(score), (30, 30), 25)
scoreUI = Text(screen, 'score', (30, 50), 50)

hpText = Text(screen, str(hp), (screen.get_width() - 30, 30), 25)
hpUI = Text(screen, 'hp', (screen.get_width() - 30, 50), 50)

# Music initialization
hpSound = pygame.mixer.Sound('sounds/hp.mp3')
shotSound = pygame.mixer.Sound('sounds/shot.mp3')
deathSound = pygame.mixer.Sound('sounds/death.mp3')
killSound = pygame.mixer.Sound('sounds/kill.mp3')

# Main loop
while True:
    clock.tick(60)
    screen.fill(black)

    key = pygame.key.get_pressed()

    spritesList.update()

    # Game logic

    # Player movement
    if key[pygame.K_w]:
        pl.moveY(-velocity)
    if key[pygame.K_s]:
        pl.moveY(velocity)
    if key[pygame.K_a]:
        pl.moveX(-velocity)
    if key[pygame.K_d]:
        pl.moveX(velocity)

    for event in pygame.event.get():
        # Game quit
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            # Shooting
            if event.key == pygame.K_SPACE and hp >= 0:
                spritesList.add(Bullet(white, 5, 5, pl.rect.x +
                                pl.image.get_width() // 2, pl.rect.y))
                shotSound.play()

            # Boost on
            if event.key == pygame.K_LSHIFT:
                velocity = 10
            # UI logic
            if event.key == pygame.K_ESCAPE:
                ui.pauseScreen(screen)

        if event.type == pygame.KEYUP:
            # Boost off
            if event.key == pygame.K_LSHIFT:
                velocity = 4

    for sprite in spritesList:
        # Bullets movement
        if sprite.name == 'bullet':
            sprite.bulletMove(5)
        if sprite.name == 'enemyBullet':
            sprite.bulletMove(-5)

        # Enemies movement
        if sprite.name == 'enemy':
            sprite.enemyMove(3)

    checker()
    kill()
    enemyGenerator()

    # Player death
    if hp <= 0:
        hpSound.stop()
        killSound.stop()
        shotSound.stop()
        deathSound.play()

        ui.saveData('highscore.txt', score, ui.getData('highscore.txt'))
        state = ui.endScreen(screen, score, ui.getData('highscore.txt'))

        if not state:
            init()
            state = True

    # UI logic
    scoreText.showText('score')
    scoreUI.showText(str(score))
    hpText.showText('hp')
    hpUI.showText(str(hp))

    # DEBUGGING
    #ls = spritesList.sprites()
    # print('\n\n\n\n')
    # for sprite in ls:
    #   print(sprite.name, sprite.rect.x, sprite.rect.y)
    # DEBUGGING

    # Pygame stuff
    spritesList.draw(screen)
    pygame.display.flip()
