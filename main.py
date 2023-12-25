import pygame
import time
import random

pygame.init()

pygame.display.set_caption("BOMB DASH")
screen = pygame.display.set_mode((1920, 1000), pygame.FULLSCREEN)

runGame = True
runMenu = True
runScore = False
mainRun = True
goToMenu = False

xSpeed = float(0)
ySpeed = float(0)
playerX = 100
playerY = 100
launchSpeed = 6
diminutionSpeed = 0.1
xScreen = 600
yScreen = 600
spawnRate = 250

up = False
down = False
Right = False
Left = False

shadowFrameDelay = 10
bombs = []
explodingBombs = []

newTime = float(0)
lastTime = float(0)

colors = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

i = 0
positions = []
defPositions = []
for edz in range(0, shadowFrameDelay):
    positions.append([0, 0])
    defPositions.append([0, 0])


def getBestScore():
    file = open("bestscore.score", "r+")
    return int(file.read())


def setBestScore(score):
    file = open("bestscore.score", "w+")
    file.write(str(score))


def text_to_screen(screens, text, x, y, size=50, font_type='Ubuntu-R.ttf', color=colors):
    text = str(text)
    font = pygame.font.Font(font_type, size)
    text = font.render(text, True, color)
    screens.blit(text, (x, y))


def drawPlayer(x, y, positions, i):
    pygame.draw.rect(screen, (100, 0, 100),
                     pygame.Rect(positions[i - shadowFrameDelay][0], positions[i - shadowFrameDelay][1], 50, 50), 5)
    pygame.draw.rect(screen, (255, 0, 255), pygame.Rect(x, y, 50, 50), 1)


def drawBombs():
    for bomb in bombs:
        if bomb[2] != 0:
            text_to_screen(screen, int(bomb[2] / 10), bomb[0] - 15, bomb[1] - 15, 30, color=(255, bomb[2], bomb[2]))

    for bomb in explodingBombs:
        if bomb[2] < 600:
            pygame.draw.rect(screen, colors,
                             pygame.Rect((bomb[0] - (bomb[2] / 2)), (bomb[1] - (bomb[2] / 2)), bomb[2], bomb[2]), 1)
            for azi in range(1, 20):
                pygame.draw.rect(screen, (
                    int(colors[0] - (azi * (colors[0] / 20))),
                    int(colors[1] - (azi * (colors[1] / 20))),
                    int(colors[2] - (azi * (colors[2] / 20)))),
                                 pygame.Rect((bomb[0] - (bomb[2] / 2)) + azi, (bomb[1] - (bomb[2] / 2)) + azi,
                                             bomb[2] - azi * 2, bomb[2] - azi * 2), 1)


score = 0

while mainRun:
    positions = defPositions
    i = 0
    spawnRate = 250
    bombs.clear()
    explodingBombs.clear()
    score = 0
    playerX = 100
    playerY = 100
    xSpeed = 0
    ySpeed = 0
    runGame = True
    runMenu = True
    runScore = False
    goToMenu = False
    while runMenu:
        screen.fill((0, 0, 0))
        # inputs

        for event in pygame.event.get():
            if event == pygame.QUIT:
                runMenu = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    xSpeed = launchSpeed
                if event.key == pygame.K_q:
                    xSpeed = -launchSpeed
                if event.key == pygame.K_z:
                    ySpeed = -launchSpeed
                if event.key == pygame.K_s:
                    ySpeed = launchSpeed

        if xSpeed < 0:
            xSpeed += diminutionSpeed
        if xSpeed > 0:
            xSpeed -= diminutionSpeed
        if -diminutionSpeed < xSpeed < diminutionSpeed:
            xSpeed = 0

        if ySpeed < 0:
            ySpeed += diminutionSpeed
        if ySpeed > 0:
            ySpeed -= diminutionSpeed
        if -diminutionSpeed < ySpeed < diminutionSpeed:
            ySpeed = 0

        # update positions

        lastx = playerX
        lasty = playerY

        playerX += float(xSpeed)
        playerY += float(ySpeed)

        newTime = time.time_ns() / 10000000

        # hitboxe checking
        if (1920 / 3) < playerX + 50 < (1920 / 3) * 2 and (1080 / 3) < playerY + 50 < (1080 / 3) * 2:
            runMenu = False

        if (1920 / 3) < playerX + 50 < (1920 / 3) * 2 and (1080 / 2) < playerY < (1080 / 3) * 2:
            runMenu = False

        if (1920 / 3) < playerX < (1920 / 3) * 2 and (1080 / 2) < playerY + 50 < (1080 / 3) * 2:
            runMenu = False

        if (1920 / 3) < playerX < (1920 / 3) * 2 and (1080 / 2) < playerY < (1080 / 3) * 2:
            runMenu = False

        if 1730 < playerX + 50 < 1920 and 0 < playerY < 50:
            mainRun = False
            runMenu = False
            runGame = False
            pygame.QUIT
            pass

        if 1730 < playerX < 1920 and 0 < playerY + 50 < 50:
            mainRun = False
            runMenu = False
            runGame = False
            pygame.QUIT
            pass

        if 1730 < playerX + 50 < 1920 and 0 < playerY + 50 < 50:
            mainRun = False
            runMenu = False
            runGame = False
            pygame.QUIT
            pass

        if 1730 < playerX + 50 < 1920 and 0 < playerY < 50:
            mainRun = False
            runMenu = False
            runGame = False
            pygame.QUIT
            pass

        if playerX > 1650 and playerY > 980:
            runGame = False
            runScore = True
            goToMenu = True
        if playerX + 50 > 1650 and playerY > 980:
            runGame = False
            runMenu = False
            runScore = True
            goToMenu = True
        if playerX > 1650 and playerY + 50 > 980:
            runGame = False
            runMenu = False
            runScore = True
            goToMenu = True
        if playerX + 50 > 1650 and playerY + 50 > 980:
            runGame = False
            runMenu = False
            runScore = True
            goToMenu = True

        # CHECKING MY CORNERS

        if playerY < 0:
            playerY = 0
        if playerX < 0:
            playerX = 0
        if playerY > 1080 - 50:
            playerY = 1080 - 50
        if playerX > 1920 - 50:
            playerXd = 1920 - 50

        # drawing to screen

        positions.append([playerX, playerY])
        drawPlayer(playerX, playerY, positions, i)
        text_to_screen(screen, "> Jouer !", (1920 / 2) - 400, (1080 / 2) - 100, size=200)
        text_to_screen(screen, "Quitter", 1730, 20, size=50)
        text_to_screen(screen, "Historique", 1650, 980, size=50)
        text_to_screen(screen, "Scrupikal", 10, 1040, size=25)
        pygame.display.flip()

    while runScore:
        screen.fill((0, 0, 0))
        # inputs

        for event in pygame.event.get():
            if event == pygame.QUIT:
                runScore = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    xSpeed = launchSpeed
                if event.key == pygame.K_q:
                    xSpeed = -launchSpeed
                if event.key == pygame.K_z:
                    ySpeed = -launchSpeed
                if event.key == pygame.K_s:
                    ySpeed = launchSpeed

        if xSpeed < 0:
            xSpeed += diminutionSpeed
        if xSpeed > 0:
            xSpeed -= diminutionSpeed
        if -diminutionSpeed < xSpeed < diminutionSpeed:
            xSpeed = 0

        if ySpeed < 0:
            ySpeed += diminutionSpeed
        if ySpeed > 0:
            ySpeed -= diminutionSpeed
        if -diminutionSpeed < ySpeed < diminutionSpeed:
            ySpeed = 0

        # update positions

        lastx = playerX
        lasty = playerY

        playerX += float(xSpeed)
        playerY += float(ySpeed)

        newTime = time.time_ns() / 10000000

        # hitboxe checking

        if 1730 < playerX + 50 < 1920 and 0 < playerY < 50:
            runGame = False
            runScore = False
            pass

        if 1730 < playerX < 1920 and 0 < playerY + 50 < 50:
            runGame = False
            runScore = False
            pass

        if 1730 < playerX + 50 < 1920 and 0 < playerY + 50 < 50:
            runGame = False
            runScore = False
            pass

        if 1730 < playerX + 50 < 1920 and 0 < playerY < 50:
            runGame = False
            runScore = False
            pass

        # CHECKING MY CORNERS

        if playerY < 0:
            playerY = 0
        if playerX < 0:
            playerX = 0
        if playerY > 1080 - 50:
            playerY = 1080 - 50
        if playerX > 1920 - 50:
            playerXd = 1920 - 50

        # drawing to screen

        positions.append([playerX, playerY])
        drawPlayer(playerX, playerY, positions, i)
        text_to_screen(screen, "Quitter", 1730, 20, size=50)
        file = open("score.score", "r+")
        i = 0
        lines = file.read().split("\n")
        text_to_screen(screen, "Best score : " + str(getBestScore()), 50, 20, size=40)
        for line in lines:
            text_to_screen(screen, line, 50, 50 + (i * 35), size=30)
            i += 1
        file.close()

        pygame.display.flip()

    startTime = time.time_ns() / 100000000

    while runGame:
        screen.fill((0, 0, 0))

        # inputs

        for event in pygame.event.get():
            if event == pygame.QUIT:
                runGame = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    xSpeed = launchSpeed
                if event.key == pygame.K_q:
                    xSpeed = -launchSpeed
                if event.key == pygame.K_z:
                    ySpeed = -launchSpeed
                if event.key == pygame.K_s:
                    ySpeed = launchSpeed

        if xSpeed < 0:
            xSpeed += diminutionSpeed
        if xSpeed > 0:
            xSpeed -= diminutionSpeed
        if -diminutionSpeed < xSpeed < diminutionSpeed:
            xSpeed = 0

        if ySpeed < 0:
            ySpeed += diminutionSpeed
        if ySpeed > 0:
            ySpeed -= diminutionSpeed
        if -diminutionSpeed < ySpeed < diminutionSpeed:
            ySpeed = 0

        # update positions

        lastx = playerX
        lasty = playerY

        playerX += float(xSpeed)
        playerY += float(ySpeed)

        newTime = time.time_ns() / 10000000

        # update bombs
        for bomb in bombs:
            if bomb[2] > 0:
                bomb[2] -= 1
            elif bomb[2] <= 0 and not bomb[3]:
                explodingBombs.append([bomb[0], bomb[1], 0])
                bomb[3] = True
        for bomb in explodingBombs:
            if bomb[2] < 600:
                bomb[2] += 1

        # randomly spawning bombs

        if random.randint(0, int(spawnRate)) == 1:
            bombs.append([random.randint(0, 1920), random.randint(0, 1080), 200, False])

        spawnRate -= 0.005

        # hitboxe checking

        for bomb in explodingBombs:
            if (bomb[0] - (bomb[2] / 2)) < playerX + 50 < (bomb[0] - (bomb[2] / 2)) + bomb[2] and (
                    bomb[1] - (bomb[2] / 2)) < playerY < (bomb[1] - (bomb[2] / 2)) + bomb[2] and bomb[2] < 600:
                runGame = False

            if (bomb[0] - (bomb[2] / 2)) < playerX < (bomb[0] - (bomb[2] / 2)) + bomb[2] and (
                    bomb[1] - (bomb[2] / 2)) < playerY + 50 < (bomb[1] - (bomb[2] / 2)) + bomb[2] and bomb[2] < 600:
                runGame = False

            if (bomb[0] - (bomb[2] / 2)) < playerX + 50 < (bomb[0] - (bomb[2] / 2)) + bomb[2] and (
                    bomb[1] - (bomb[2] / 2)) < playerY < (bomb[1] - (bomb[2] / 2)) + bomb[2] and bomb[2] < 600:
                runGame = False

            if (bomb[0] - (bomb[2] / 2)) < playerX < (bomb[0] - (bomb[2] / 2)) + bomb[2] and (
                    bomb[1] - (bomb[2] / 2)) < playerY < (bomb[1] - (bomb[2] / 2)) + bomb[2] and bomb[2] < 600:
                runGame = False

            # CHECKING MY CORNERS

            if playerY < 0:
                playerY = 0
            if playerX < 0:
                playerX = 0
            if playerY > 1080 - 50:
                playerY = 1080 - 50
            if playerX > 1920 - 50:
                playerX = 1920 - 50

        # drawing to screen

        positions.append([playerX, playerY])
        drawPlayer(playerX, playerY, positions, i)
        drawBombs()
        text_to_screen(screen, str(int(time.time_ns() / 100000000 - startTime)), 30, 30)
        pygame.display.flip()

        lastTime = float(time.time_ns() / 10000000)

    if mainRun and not goToMenu:
        score = int(time.time_ns() / 100000000 - startTime)
        file = open("score.score", "a+")
        file.write(f"Date : {time.ctime(),}, Score : {score}\n")
        file.close()

        if getBestScore() < score :
            setBestScore(score)

        screen.fill((0, 0, 0))
        text_to_screen(screen, "Bien joué !!", 1920 / 2 - 150, 1080 / 2 - 30)
        text_to_screen(screen, "Score : " + str(score),
                       1920 / 2 - 150,
                       1080 / 2 + 30,
                       size=25)
        text_to_screen(screen, "Best score : " + str(getBestScore()),
                       1920 / 2 - 150,
                       1080 / 2 + 55,
                       size=25)

        pygame.display.flip()

        time.sleep(2)
