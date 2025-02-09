import pygame
from constants import cellSize
from functions import *


class mainScreen:
    def __init__(self, screen):
        self.screen = screen
        self.state = 1

        self.mainFont = pygame.font.Font('graphics/font.ttf', int(cellSize * 1.5))
        self.miniFont = pygame.font.Font('graphics/font.ttf', int(cellSize * 0.8) - (cellSize // 10))

        self.mainText = self.mainFont.render('Main Screen', False, "#FFFFFF")
        self.mainTextRect = self.mainText.get_rect()

        self.startText = self.miniFont.render("Start game", False, "#FFFFFF")
        self.startTextRect = self.startText.get_rect()
        self.leaderboardText = self.miniFont.render("Leaderboard", False, "#FFFFFF")
        self.leaderboardTextRect = self.leaderboardText.get_rect(x=200)

        # set the center of the rectangular object.

        self.mainTextRect.center = (screen.get_width() // 2, screen.get_height() // 2 - (screen.get_height() // 6))

        self.startTextRect.center = (self.mainTextRect.centerx, self.mainTextRect.centery + cellSize * 3)
        self.leaderboardTextRect.center = ( self.mainTextRect.centerx, screen.get_height() // 2 - (screen.get_height() // 10) + cellSize * 4)

        self.startBackgroundRect = (pygame.Rect
                                    (self.startTextRect.centerx - (self.startTextRect.width // 2) - (
                                                self.startTextRect.width // 10),
                                     self.startTextRect.centery - self.startTextRect.height,
                                     self.startTextRect.width + (self.startTextRect.width // 5),
                                     self.startTextRect.height * 2))

        self.leaderboardBackgroundRect = (pygame.Rect
                                          (self.leaderboardTextRect.centerx - (self.leaderboardTextRect.width // 2) - (
                                                  self.leaderboardTextRect.width // 10),
                                           self.leaderboardTextRect.centery - self.leaderboardTextRect.height,
                                           self.leaderboardTextRect.width + (self.leaderboardTextRect.width // 5),
                                           self.leaderboardTextRect.height * 2))

    def draw(self, surface):
        pygame.draw.rect(surface, "#555555", self.startBackgroundRect)
        pygame.draw.rect(surface, "#005500", self.leaderboardBackgroundRect)
        surface.blit(self.mainText, self.mainTextRect)
        surface.blit(self.startText, self.startTextRect)
        surface.blit(self.leaderboardText, self.leaderboardTextRect)
        self.pressButtons()

    def pressButtons(self):
        mousePos = pygame.mouse.get_pos()
        mouseButton = pygame.mouse.get_pressed()

        if self.startBackgroundRect.topleft[0] <= mousePos[0] <= self.startBackgroundRect.bottomright[0] \
                and self.startBackgroundRect.topleft[1] <= mousePos[1] <= self.startBackgroundRect.bottomright[1] \
                and mouseButton[0]:
            changeState(4)

        if self.leaderboardBackgroundRect.topleft[0] <= mousePos[0] <= self.leaderboardBackgroundRect.bottomright[0] \
                and self.leaderboardBackgroundRect.topleft[1] <= mousePos[1] <= \
                self.leaderboardBackgroundRect.bottomright[1] \
                and mouseButton[0]:
            changeState(5)
