import pygame
from constants import cellSize, cellNumber
from functions import *


class gameOverScreen:
    def __init__(self):
        self.mainFont = pygame.font.Font('graphics/font.ttf', int(cellSize * 1.5))
        self.miniFont = pygame.font.Font('graphics/font.ttf', int(cellSize * 0.5))
        self.midiFont = pygame.font.Font('graphics/font.ttf', cellSize - (cellSize // 10))

        self.mainText = self.mainFont.render('Game over', False, "#FFFFFF")
        self.mainTextRect = self.mainText.get_rect()

        self.menuText = self.miniFont.render("Back to Main Menu", False, "#FFFFFF")
        self.menuTextRect = self.menuText.get_rect()

        self.leaderBoardText = self.miniFont.render("To Leaderboard", False, "#FFFFFF")
        self.leaderBoardTextRect = self.leaderBoardText.get_rect()

        self.retryText = self.miniFont.render("Retry", False, "#FFFFFF")
        self.retryTextRect = self.retryText.get_rect()

        self.mainTextRect.center = (cellNumber // 2 * cellSize, cellNumber // 3 * cellSize - cellSize * 2)

        self.menuTextRect.center = (self.mainTextRect.centerx, self.mainTextRect.y + cellSize * 4)

        self.leaderBoardTextRect.center = (self.menuTextRect.centerx, self.menuTextRect.y + cellSize * 3)

        self.retryTextRect.center = (self.leaderBoardTextRect.centerx, self.leaderBoardTextRect.y + cellSize * 3)

        self.menuBackgroundRect = pygame.Rect(self.menuTextRect.x - cellSize * 0.4,
                                              self.menuTextRect.y - cellSize * 0.4,
                                              self.menuTextRect.width + cellSize * 0.8,
                                              self.menuTextRect.height + cellSize * 0.8)

        self.leaderBoardBackgroundRect = pygame.Rect(self.leaderBoardTextRect.x - cellSize * 0.4,
                                                     self.leaderBoardTextRect.y - cellSize * 0.4,
                                                     self.leaderBoardTextRect.width + cellSize * 0.8,
                                                     self.leaderBoardTextRect.height + cellSize * 0.8)

        self.retryBackgroundRect = pygame.Rect(self.retryTextRect.x - cellSize * 0.4,
                                               self.retryTextRect.y - cellSize * 0.4,
                                               self.retryTextRect.width + cellSize * 0.8,
                                               self.retryTextRect.height + cellSize * 0.8)

    def draw(self, surface):
        surface.blit(self.mainText, self.mainTextRect)
        pygame.draw.rect(surface, "#555555", self.menuBackgroundRect)
        pygame.draw.rect(surface, "#555555", self.leaderBoardBackgroundRect)
        pygame.draw.rect(surface, "#555555", self.retryBackgroundRect)

        surface.blit(self.menuText, self.menuTextRect)
        surface.blit(self.leaderBoardText, self.leaderBoardTextRect)
        surface.blit(self.retryText, self.retryTextRect)

        self.pressButtons()

    def pressButtons(self):
        mousePos = pygame.mouse.get_pos()
        mouseButton = pygame.mouse.get_pressed()
        if self.retryBackgroundRect.topleft[0] <= mousePos[0] <= self.retryBackgroundRect.bottomright[0] and \
                self.retryBackgroundRect.topleft[1] <= mousePos[1] <= self.retryBackgroundRect.bottomright[1] and \
                mouseButton[0]:
            changeState(2)

        elif self.menuBackgroundRect.topleft[0] <= mousePos[0] <= self.menuBackgroundRect.bottomright[0] and \
                self.menuBackgroundRect.topleft[1] <= mousePos[1] <= self.menuBackgroundRect.bottomright[1] and \
                mouseButton[0]:
            changeState(1)

        elif self.leaderBoardBackgroundRect.topleft[0] <= mousePos[0] <= self.leaderBoardTextRect.bottomright[0] \
                and self.leaderBoardBackgroundRect.topleft[1] <= mousePos[1] <= self.leaderBoardTextRect.bottomright[1] and mouseButton[0]:
            changeState(5)
