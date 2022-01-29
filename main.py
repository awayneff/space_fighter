import pygame
from random import randint
import ui
from ui import Text
from player import Player
from weapon import Bullet, Rocket
from enemy import Enemy

# Variables (re)initialization
def init():
    global enCount, incrNum, enBulCount, hp, score, pl, screen, spritesList, bg_pos1, bg_pos2

    # Change incrNum to edit enemies' spawn speed (less - faster, more - slower)
    enCount, incrNum = 0, 100
    enBulCount = 0
    hp = 5
    score = 0
    bg_pos1 = 0
    bg_pos2 = -screenSize[1]

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

    if enCount >= incrNum:
        spritesList.add(Enemy(screen))

        if incrNum > 90:
            incrNum -= 5
        enCount = 0

    if len(enemies) > 0:
        enemy = enemies[randint(0, len(enemies) - 1)]

        if enBulCount >= 80:
            shotSound.play()
            bullet = Bullet((255, 0, 0), 5, 5, enemy.rect.x +
                            enemy.image.get_width() // 2 - 2, enemy.rect.y + 40)
            bullet.name = 'enemyBullet'

            spritesList.add(bullet)
            enBulCount = 0


# Destroy enemy, bullet or player on collision
def kill():
    global spritesList, score, hp, explosion_coords

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
            
            # Kill all enemies on the screen with a missle
            if pygame.sprite.collide_mask(sprite, enemySprite) and sprite.name == 'rocket' and enemySprite.name == 'enemy':
                for spr in sprites:
                    if 0 < spr.rect.y <= screenSize[1] and spr.name != "player" and spr.name != "bullet":
                        explosion_coords.append(spr)
                        delSprites.append(spr)
                delSprites.append(sprite)
                score += len(delSprites) - 1
                explosion_sound.play()

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

# Variables for background movement
bg_vel = 1
rocket_cooldown = 200
rocket_ct = 0
explosion_coords = []
time_elapsed = 0

pygame.init()
pygame.joystick.init()
screen = pygame.display.set_mode(screenSize, pygame.RESIZABLE)
pygame.display.set_caption("Space Fight")
clock = pygame.time.Clock()

bg_img = pygame.transform.scale(pygame.image.load("assets/bg.png"), screenSize)
pause_bg_img = pygame.transform.scale(
    pygame.image.load("assets/pause_bg.png"), screenSize)
hp_img = pygame.transform.scale(pygame.image.load("assets/hp.png"), (25, 25))
explosion_img = pygame.transform.scale(pygame.image.load("assets/explosion.png"), (30, 30))

# Player initialization
pl = Player(screen)
pl.rect.x = (screen.get_width() - pl.image.get_width()) // 2
pl.rect.y = pl.limit
velocity = 4

# Sprites list initialization
spritesList = pygame.sprite.Group()
spritesList.add(pl)

init()

# Main menu on game launch
main_menu = True

# Death state
dead = False

# Speeding state
thrust_on = False

# Gamepad stuff
try: 
    gamepad = True
    print(pygame.joystick.Joystick(0).get_init())
except:
    gamepad = False
    
pressed_shoot = False
pressed_thrust = False

# UI
scoreText = Text(screen, str(score), (25, 25), 25)

# Music initialization
pygame.mixer.init()
bg_music = pygame.mixer.music.load("assets/bg_music.mp3")
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(-1, 0.0)

hpSound = pygame.mixer.Sound('assets/hp.mp3')
shotSound = pygame.mixer.Sound('assets/shot.mp3')
deathSound = pygame.mixer.Sound('assets/death.mp3')
killSound = pygame.mixer.Sound('assets/kill.mp3')
missle_sound = pygame.mixer.Sound("assets/rocket_launch.wav")
explosion_sound = pygame.mixer.Sound("assets/explosion.wav")
thrust_sound = pygame.mixer.Sound("assets/thrust_on.wav")
thrust_ongoing_sound = pygame.mixer.Sound("assets/thrust_ongoing.wav")

# Main loop
while True:
    if main_menu:
        main_menu = ui.main_menu(screen, ui.getData('highscore.txt'), pause_bg_img)
        
    clock.tick(60)
    screen.blit(bg_img, (0, bg_pos1))
    screen.blit(bg_img, (0, bg_pos2))
    
    # Update the rocket cooldown
    rocket_ct += 1
    
    # Explosion blit
    if len(explosion_coords) > 0: 
        for sprite in explosion_coords:
            screen.blit(explosion_img, (sprite.rect.x, sprite.rect.y))
        
        time_elapsed += 1
        
        if time_elapsed > 50:
            time_elapsed = 0
            explosion_coords = []
        
    if thrust_on:
        (x, y) = screenSize
        velocity = x * y // 50000
        pl.image = pl.image_thrust
        if bg_vel < 0.4 * velocity:
            bg_vel += velocity * 0.005
        if 0.4 * velocity < bg_vel <= velocity:
            bg_vel += velocity * 0.03
    else:
        (x, y) = screenSize
        thrust_sound.stop()
        velocity = x * y // 150000
        pl.image = pl.image_slow
        if bg_vel > velocity:
            bg_vel -= velocity * 0.01
        if velocity > bg_vel >= velocity * 0.375:
            bg_vel -= velocity * 0.3

    # Move the background images to imitate movement
    bg_pos1 += bg_vel
    bg_pos2 += bg_vel

    if bg_pos1 > screenSize[1]:
        bg_pos1 = -screenSize[1]
    if bg_pos2 > screenSize[1]:
        bg_pos2 = -screenSize[1]

    spritesList.update()

    key = pygame.key.get_pressed()

    # Game logic

    # Player movement
    if not gamepad:
        if key[pygame.K_w]:
            pl.moveY(-velocity)
        if key[pygame.K_s]:
            pl.moveY(velocity)
        if key[pygame.K_a]:
            pl.moveX(-velocity)
        if key[pygame.K_d]:
            pl.moveX(velocity)

    # Gamepad controls
    if gamepad:
        # Movement
        if pygame.joystick.Joystick(0).get_axis(1) < -0.1:
            pl.moveY(-velocity)
        if pygame.joystick.Joystick(0).get_axis(1) > 0.1:
            pl.moveY(velocity)
        if pygame.joystick.Joystick(0).get_axis(0) < -0.1:
            pl.moveX(-velocity)
        if pygame.joystick.Joystick(0).get_axis(0) > 0.1:
            pl.moveX(velocity)

        if pygame.joystick.Joystick(0).get_button(1) == 1 and hp >= 0 and not pressed_shoot:
            pressed_shoot = True
            spritesList.add(Bullet((0, 0, 255), 5, 5, pl.rect.x +
                            pl.image.get_width() // 2, pl.rect.y))
            shotSound.play()

        if pygame.joystick.Joystick(0).get_button(9) == 1:
            pygame.mixer.music.pause()
            ui.pauseScreen(screen, pause_bg_img)
            pygame.mixer.music.unpause()

        if pygame.joystick.Joystick(0).get_button(6) == 1 and pygame.joystick.Joystick(0).get_button(7) == 1 and not pressed_thrust:
            pressed_thrust = True
            thrust_on = True
            if bg_vel < velocity // 2:
                thrust_sound.play()
            thrust_ongoing_sound.play(-1)

        if pygame.joystick.Joystick(0).get_button(1) == 0:
            pressed_shoot = False

        # Boost off
        if pygame.joystick.Joystick(0).get_button(6) == 0 or pygame.joystick.Joystick(0).get_button(7) == 0:
            thrust_on = False
            pressed_thrust = False
            thrust_ongoing_sound.stop()

    for event in pygame.event.get():
        # Game quit
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.VIDEORESIZE:
            screenSize = pygame.display.get_surface().get_size()
            pause_bg_img = pygame.transform.scale(pause_bg_img, screenSize)
            bg_img = pygame.transform.scale(
                bg_img, (screenSize[0], screenSize[1] + 50))

            pl.rect.x, pl.rect.y = (
                (screen.get_width() - pl.image.get_width()) // 2, screen.get_height() - 200)

            bg_pos1 = 0
            bg_pos2 = -screenSize[1]
        if not gamepad:
            if event.type == pygame.KEYDOWN:
                # Shooting
                if event.key == pygame.K_SPACE and hp >= 0:
                    spritesList.add(Bullet((0, 0, 255), 5, 5, pl.rect.x +
                                    pl.image.get_width() // 2, pl.rect.y))
                    shotSound.play()
                
                # Rocket launch
                if event.key == pygame.K_RETURN and hp >= 0:
                    if rocket_ct >= rocket_cooldown:
                        spritesList.add(Rocket(pl.rect.x + pl.image.get_width() // 2, pl.rect.y))
                        spritesList.add(Rocket(pl.rect.x + pl.image.get_width() // 4, pl.rect.y))
                        rocket_ct = 0
                        missle_sound.play()
                        
                # Boost on
                if event.key == pygame.K_LSHIFT:
                    thrust_on = True
                    if bg_vel < velocity // 2:
                        thrust_sound.play()
                    thrust_ongoing_sound.play(-1)

                # UI logic
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.pause()
                    ui.pauseScreen(screen, pause_bg_img)
                    pygame.mixer.music.unpause()

            if event.type == pygame.KEYUP:
                # Boost off
                if event.key == pygame.K_LSHIFT:
                    thrust_on = False
                    thrust_ongoing_sound.stop()

    for sprite in spritesList:
        # Bullets movement
        if sprite.name == 'bullet':
            sprite.bulletMove(1.5 * velocity)
        if sprite.name == "rocket":
            sprite.rocket_move(1.5 * velocity)
        if sprite.name == 'enemyBullet':
            sprite.bulletMove(-velocity // 2)

        # Enemies movement
        if sprite.name == 'enemy':
            sprite.enemyMove(randint(velocity // 5, velocity // 3))

    checker()
    kill()
    enemyGenerator()

    # Player death
    if hp <= 0:
        pygame.mixer.music.pause()
        pygame.mixer.music.rewind()
        thrust_ongoing_sound.stop()
        hpSound.stop()
        killSound.stop()
        shotSound.stop()
        deathSound.play()

        pl.image = pl.image_slow
        ui.saveData('highscore.txt', score, ui.getData('highscore.txt'))
        dead = ui.endScreen(screen, score, ui.getData(
            'highscore.txt'), pause_bg_img)

        if not dead:
            init()
            pygame.mixer.music.unpause()
            velocity = 4
            bg_vel = 1
            dead = True

    # UI logic
    scoreText.showText(str(score))

    for i in range(0, hp):
        screen.blit(hp_img, (screen.get_width() - 50 - i * 25, 25))

    # Pygame stuff
    spritesList.draw(screen)
    pygame.display.update()
