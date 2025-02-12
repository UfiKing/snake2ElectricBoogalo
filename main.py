import sys
import pygame
from constants import cellSize, cellNumber
from pygame import Vector2
from screens.mainScreen import mainScreen
from screens.mainGame import mainGame
from screens.gameOver import gameOverScreen
from screens.nameScreen import nameScreen
from screens.leaderboard import leaderboardScreen
from gameLogic import *

class main:

    def __init__(self, screen):
        self.mainGame = mainGame()
        self.mainScreen = mainScreen(screen)
        self.gameOverScreen = gameOverScreen()
        self.nameScreen = nameScreen()
        self.leaderboardScreen = leaderboardScreen(screen)

    def events(self, event, screen):
        state = getState()
        if event.type == SCREEN_UPDATE and state == 2:
            self.mainGame.update(screen)
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_w or event.key == pygame.K_UP) and self.mainGame.snake.currentDirection.y != 1:
                self.mainGame.snake.direction = Vector2(0, -1)
            elif (
                    event.key == pygame.K_s or event.key == pygame.K_DOWN) and self.mainGame.snake.currentDirection.y != -1:
                self.mainGame.snake.direction = Vector2(0, 1)
            elif (
                    event.key == pygame.K_d or event.key == pygame.K_RIGHT) and self.mainGame.snake.currentDirection.x != -1:
                self.mainGame.snake.direction = Vector2(1, 0)
            elif (
                    event.key == pygame.K_a or event.key == pygame.K_LEFT) and self.mainGame.snake.currentDirection.x != 1:
                self.mainGame.snake.direction = Vector2(-1, 0)
            elif event.key == pygame.K_ESCAPE and state == 2:
                switchGameState()

        if event.type == pygame.TEXTINPUT and self.nameScreen.pressed and len(self.nameScreen.name) != 12:
            self.nameScreen.name.append(event.text)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE and len(
                self.nameScreen.name) > 0 and self.nameScreen.pressed:
            self.nameScreen.name.pop()
        if event.type == pygame.MOUSEBUTTONUP:
            setMouseButtonUp(True)
        else:
            setMouseButtonUp(False)


    def drawAndUpdate(self, screen):
        state = getState()
        if state == 1:
            self.mainScreen.draw(screen)
        elif state == 2:
            self.mainGame.draw(screen)
        elif state == 3:
            self.gameOverScreen.draw(screen)
        elif state == 4:
            self.nameScreen.update(screen)
        elif state == 5:
            self.leaderboardScreen.draw(screen)


pygame.init()

screen = pygame.display.set_mode( (cellSize * cellNumber, cellSize * cellNumber) )
clock = pygame.time.Clock()


game = main(screen)
SCREEN_UPDATE = pygame.USEREVENT  # tle nardimo svoj event
pygame.time.set_timer(SCREEN_UPDATE, 150)  # in executamo tale event vsakih 150ms



def drawGrid(screen):
    for i in range(cellNumber):
        for j in range(cellNumber):
            if i % 2 == 0:
                if j % 2 == 0:
                    pygame.draw.rect(screen, "#AFD746", pygame.Rect(i * cellSize, j * cellSize, cellSize, cellSize))
                    pygame.draw.rect(screen, "#b9dc5c", pygame.Rect((i + 1) * cellSize, j * cellSize, cellSize, cellSize))
                else:
                    pygame.draw.rect(screen, "#AFD746", pygame.Rect((i+1) * cellSize, j * cellSize, cellSize, cellSize))
                    pygame.draw.rect(screen, "#b9dc5c",
                                     pygame.Rect(i * cellSize, j * cellSize, cellSize, cellSize))

while True:
    #screen.fill("#AFD746")
    drawGrid(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        game.events(event, screen)

    game.drawAndUpdate(screen)

    pygame.display.update()
    clock.tick(60)