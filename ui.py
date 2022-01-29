import pygame

white = (255, 255, 255)
black = (0, 0, 0)


clock = pygame.time.Clock()
pygame.joystick.init()

# Gamepad stuff
try: 
    gamepad = True
    print(pygame.joystick.Joystick(0).get_init())
except:
    gamepad = False
    
class Text():
    def __init__(self, screen, caption, coords, fontSize):
        self.coords = coords
        self.screen = screen

        self.font = pygame.font.Font(None, fontSize)
        self.text = self.font.render(caption, 1, white)

        self.width = self.text.get_width()
        self.height = self.text.get_height()

    # Show the text
    def showText(self, caption):
        self.text = self.font.render(caption, 1, white)
        self.screen.blit(self.text, self.coords)


def main_menu(screen, highScore, bg_img):
    main_menu = True

    title = Text(screen, 'Space Fighter', (0, 0), 35)
    title.coords = ((screen.get_width() - title.width) //
                    2, screen.get_height() // 2 - 100)

    highScoreText = Text(screen, 'high score ' + str(highScore), (0, 0), 25)
    highScoreText.coords = ((screen.get_width() - highScoreText.width) //
                            2, screen.get_height() // 2 - 65)

    restart = Text(screen, 'start', (0, 0), 30)
    restart.coords = ((screen.get_width() - restart.width) //
                      2, screen.get_height() // 2 + 100)

    exit = Text(screen, 'ESC to exit', (0, 0), 15)
    exit.coords = ((screen.get_width() - exit.width) //
                   2, screen.get_height() - 50)
    
    while main_menu: 
        screen.blit(bg_img, (0, 0))

        title.showText('Space Fighter')
        highScoreText.showText('high score ' + str(highScore))
        restart.showText('start')
        exit.showText('ESC to exit')

        if gamepad:
            if pygame.joystick.Joystick(0).get_button(2) == 1:
                pygame.quit()
            if pygame.joystick.Joystick(0).get_button(1) == 1:
                main_menu = False
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # Button clicks
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

            # Mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart.coords[0] <= pygame.mouse.get_pos()[0] <= restart.coords[0] + restart.width\
                        and restart.coords[1] <= pygame.mouse.get_pos()[1] <= restart.coords[1] + restart.height:
                    main_menu = False

        pygame.display.update()
        clock.tick(60)

    return main_menu


def endScreen(screen, score, highScore, bg_img):
    dead = True

    title = Text(screen, 'you\'re dead!', (0, 0), 35)
    title.coords = ((screen.get_width() - title.width) //
                    2, screen.get_height() // 2 - 100)

    scoreText = Text(screen, 'score ' + str(score), (0, 0), 25)
    scoreText.coords = ((screen.get_width() - scoreText.width) //
                        2, screen.get_height() // 2 - 35)

    highScoreText = Text(screen, 'high score ' + str(highScore), (0, 0), 25)
    highScoreText.coords = ((screen.get_width() - highScoreText.width) //
                            2, screen.get_height() // 2 - 65)

    restart = Text(screen, 'restart', (0, 0), 30)
    restart.coords = ((screen.get_width() - restart.width) //
                      2, screen.get_height() // 2 + 100)

    exit = Text(screen, 'ESC to exit', (0, 0), 15)
    exit.coords = ((screen.get_width() - exit.width) //
                   2, screen.get_height() - 50)

    while dead:
        screen.blit(bg_img, (0, 0))

        title.showText('you\'re dead!')
        scoreText.showText('score ' + str(score))
        highScoreText.showText('high score ' + str(highScore))
        restart.showText('restart')
        exit.showText('ESC to exit')

        if gamepad:
            if pygame.joystick.Joystick(0).get_button(2) == 1:
                pygame.quit()
            if pygame.joystick.Joystick(0).get_button(1) == 1:
                dead = False
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # Button clicks
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

            # Mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart.coords[0] <= pygame.mouse.get_pos()[0] <= restart.coords[0] + restart.width\
                        and restart.coords[1] <= pygame.mouse.get_pos()[1] <= restart.coords[1] + restart.height:
                    dead = False

        pygame.display.update()
        clock.tick(60)

    return dead


def pauseScreen(screen, bg_img):
    paused = True
    pressed_unpause = False

    title = Text(screen, 'paused', (0, 0), 35)
    title.coords = ((screen.get_width() - title.width) //
                    2, screen.get_height() // 2 - 100)

    caption = Text(screen, 'ESC to continue', (0, 0), 15)
    caption.coords = ((screen.get_width() - caption.width) //
                      2, screen.get_height() - 50)

    while paused:
        screen.blit(bg_img, (0, 0))

        title.showText('paused')
        caption.showText('ESC to continue')

        if gamepad:
            if pygame.joystick.Joystick(0).get_button(1) == 1 or pygame.joystick.Joystick(0).get_button(9) == 1 and not pressed_unpause:
                pressed_unpause = True
                paused = False
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # Button clicks
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False

        pygame.display.update()
        clock.tick(60)


# Save high score to the file
def saveData(fileName, score, highScore):
    # print(highScore)
    highScore = int(highScore)
    if score >= highScore:
        highScore = score

    with open(fileName, 'w') as f:
        f.write(str(highScore))


# Get the high score from the file
def getData(fileName):
    with open(fileName, 'r') as f:
        data = f.read()

    return data
