import pygame
from pygame import Vector2
from screens.mainScreen import mainScreen
from screens.mainGame import mainGame
from screens.gameOver import gameOverScreen
from screens.nameScreen import nameScreen
from screens.leaderboard import leaderboardScreen
from functions import *

pygame.init()

SCREEN_UPDATE = pygame.USEREVENT  # tle nardimo svoj event
pygame.time.set_timer(SCREEN_UPDATE, 150)  # in executamo tale event vsakih 150ms


class logic:
    # these are the possible game states
    # 1 -> mainMenu
    # 2 -> game
    # 3 -> gameOver
    # 4 -> nameEntryScreen
    # 5 -> leaderBoard

    def __init__(self, screen):
        self.mainGame = mainGame()
        self.mainScreen = mainScreen(screen)
        self.gameOverScreen = gameOverScreen()
        self.nameScreen = nameScreen()
        self.leaderboardScreen = leaderboardScreen(screen)

    def events(self, event):
        state = getState()
        if event.type == SCREEN_UPDATE and state == 2:
            self.mainGame.update()
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

        if event.type == pygame.TEXTINPUT and self.nameScreen.pressed:
            self.nameScreen.name.append(event.text)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE and len(
                self.nameScreen.name) > 0 and self.nameScreen.pressed:
            self.nameScreen.name.pop()

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
