from warnings import catch_warnings

import pygame
from constants import cellSize, cellNumber
from gameLogic import *


class leaderboardScreen:
    def __init__(self, screen):
        self.font = pygame.font.Font('graphics/font.ttf', cellSize)
        self.fontBig = pygame.font.Font('graphics/font.ttf', int(cellSize * 1.5))

        self.backButton = pygame.image.load("graphics/backArrowLeft32.png")
        self.backButton = pygame.transform.scale(self.backButton, (cellSize * 3, cellSize * 3))
        self.backButtonRect = self.backButton.get_rect()
        self.backButtonRect.centerx = 2 * cellSize
        self.backButtonRect.centery = cellSize * 2

        self.leaderBoardText = self.fontBig.render("Leaderboard", False, "#FFFFFF")
        self.leaderBoardTextRect = self.leaderBoardText.get_rect()
        self.leaderBoardTextRect.centerx = screen.get_width() // 2
        self.leaderBoardTextRect.centery = cellSize * 2

        self.left = cellSize
        self.right = screen.get_width() - screen.get_width() // 4

        self.apple = pygame.image.load("graphics/jabolko16.png")
        self.apple = pygame.transform.scale(self.apple, (cellSize * 2, cellSize * 2))
        self.appleRect = self.apple.get_rect()
        self.appleRect.right = cellSize * cellNumber - cellSize * 3

        self.appleBad = pygame.image.load("graphics/jabolko16.bad.png")
        self.appleBad = pygame.transform.scale(self.appleBad, (cellSize * 2, cellSize * 2))

        self.boxYes = pygame.image.load("graphics/box/small/boxSmallYes.png")
        self.boxYes = pygame.transform.scale(self.boxYes, (cellSize * 2, cellSize * 2))
        self.boxRect = self.boxYes.get_rect()
        self.boxRect.right = cellSize * cellNumber
        self.boxRect.y = cellSize * 2

        self.boxNo = pygame.image.load("graphics/box/small/boxSmallNo.png")
        self.boxNo = pygame.transform.scale(self.boxNo, (cellSize * 2, cellSize * 2))

        self.texts = []
        self.textsRects = []

        self.oldLetters = ["š", "Š", "ž", "Ž", "č", "Č", "ć", "Ć", "đ", "Đ"]
        self.newLetters = ["s", "S", "z", "Z", "c", "C", "c", "C", "dz", "DZ"]

        self.leaderboardStats = 0

        self.currentLeaderboard = 1

        for i in range(10):
            self.texts.append(self.font.render(f"{i + 1}.Anon: 0", False, "#FFFFFF"))

        for i, text in enumerate(self.texts):
            self.textsRects.append(text.get_rect())
            self.textsRects[i].left = self.left
            self.textsRects[i].y += cellSize * 2 * (i + 2)

        self.scores = 0

        self.apple1 = pygame.image.load("graphics/jabolko16_1.png")
        self.apple1 = pygame.transform.scale(self.apple1, (cellSize * 2, cellSize * 2))
        self.apple1Rect = self.apple1.get_rect()
        self.apple1Rect.centery = self.backButtonRect.centery
        self.apple1Rect.left = self.backButtonRect.right + cellSize * 3
        self.apple1Bad = pygame.image.load("graphics/jabolko16_1.bad.png")
        self.apple1Bad = pygame.transform.scale(self.apple1Bad, (cellSize * 2, cellSize * 2))

        self.apple3 = pygame.image.load("graphics/jabolko16_3.png")
        self.apple3 = pygame.transform.scale(self.apple3, (cellSize * 2, cellSize * 2))
        self.apple3Rect = self.apple3.get_rect()
        self.apple3Rect.centery = self.backButtonRect.centery
        self.apple3Rect.left = self.apple1Rect.right + cellSize * 3
        self.apple3Bad = pygame.image.load("graphics/jabolko16_3.bad.png")
        self.apple3Bad = pygame.transform.scale(self.apple3Bad, (cellSize * 2, cellSize * 2))

        self.apple5 = pygame.image.load("graphics/jabolko16_5.png")
        self.apple5 = pygame.transform.scale(self.apple5, (cellSize * 2, cellSize * 2))
        self.apple5Rect = self.apple5.get_rect()
        self.apple5Rect.centery = self.backButtonRect.centery
        self.apple5Rect.left = self.apple3Rect.right + cellSize * 3
        self.apple5Bad = pygame.image.load("graphics/jabolko16_5.bad.png")
        self.apple5Bad = pygame.transform.scale(self.apple5Bad, (cellSize * 2, cellSize * 2))

    def draw(self, surface):
        if self.currentLeaderboard == 1:
            surface.blit(self.apple1Bad, self.apple1Rect)
        else:
            surface.blit(self.apple1, self.apple1Rect)

        if self.currentLeaderboard == 3:
            surface.blit(self.apple3Bad, self.apple3Rect)
        else:
            surface.blit(self.apple3, self.apple3Rect)

        if self.currentLeaderboard == 5:
            surface.blit(self.apple5Bad, self.apple5Rect)
        else:
            surface.blit(self.apple5, self.apple5Rect)
        self.update()
        surface.blit(self.backButton, self.backButtonRect)
        for i in range(len(self.textsRects)):
            surface.blit(self.texts[i], self.textsRects[i])
            try:
                if self.scores[i][4]:
                    surface.blit(self.boxYes, self.boxRect)
                else:
                    surface.blit(self.boxNo, self.boxRect)
                if not self.scores[i][5]:
                    surface.blit(self.apple, self.appleRect)
                else:
                    surface.blit(self.appleBad, self.appleRect)
            except IndexError:
                pass

            self.boxRect.y += cellSize * 2
            self.appleRect.y += cellSize * 2
        self.boxRect.y = cellSize * 2 * 2
        self.appleRect.y = cellSize * 2 * 2

    def update(self):
        mousePos = pygame.mouse.get_pos()
        mousePressed = pygame.mouse.get_pressed()
        for i in range(10):
            self.texts[i] = self.font.render(f"{i + 1}.Anon: 0", False, "#FFFFFF")

        match self.currentLeaderboard:
            case 1: self.scores = getLeaderboard(1)
            case 3: self.scores = getLeaderboard(3)
            case 5:
                self.scores = getLeaderboard(5)

        for i in range(len(self.scores)):
            name = self.scores[i][1]
            for j in range(len(self.oldLetters)):
                name = name.replace(self.oldLetters[j], self.newLetters[j])

            self.texts[i] = self.font.render(f"{i + 1} {name}:{self.scores[i][2]}", False, "#FFFFFF")

            if i == 10:
                break

        if self.backButtonRect.collidepoint(mousePos) and getMouseButtonUp():
            if getPreviousState() == 3:
                changeState(3)
            else:
                changeState(1)
        if self.apple1Rect.collidepoint(mousePos) and getMouseButtonUp():
            self.currentLeaderboard = 1
        if self.apple3Rect.collidepoint(mousePos) and getMouseButtonUp():
            self.currentLeaderboard = 3
        if self.apple5Rect.collidepoint(mousePos) and getMouseButtonUp():
            self.currentLeaderboard = 5
