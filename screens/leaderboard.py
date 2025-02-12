import pygame
from constants import cellSize
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

        self.texts = []
        self.textsRects = []

        self.oldLetters = ["š", "Š", "ž", "Ž", "č", "Č", "ć", "Ć", "đ", "Đ"]
        self.newLetters = ["s", "S", "z", "Z", "c", "C", "c", "C", "dz", "DZ"]

        for i in range(10):
            self.texts.append(self.font.render(f"{i + 1}.Anon: 0", False, "#FFFFFF"))

        for i, text in enumerate(self.texts):
            self.textsRects.append(text.get_rect())
            self.textsRects[i].left = self.left
            self.textsRects[i].y += cellSize * 2 * (i + 2)

    def draw(self, surface):

        self.update()
        surface.blit(self.backButton, self.backButtonRect)
        for i in range(len(self.textsRects)):
            surface.blit(self.texts[i], self.textsRects[i])

    def update(self):
        mousePos = pygame.mouse.get_pos()
        mousePressed = pygame.mouse.get_pressed()
        scores = getLeaderboard()

        for i in range(len(scores)):
            name = scores[i][1]
            for j in range(len(self.oldLetters)):
                name = name.replace(self.oldLetters[j], self.newLetters[j])

            self.texts[i] = self.font.render(f"{i + 1} {name}:{scores[i][2]}", False, "#FFFFFF")

            if i == 10:
                break

        if self.backButtonRect.topleft <= mousePos <= self.backButtonRect.bottomright and mousePressed[0]:
            if getPreviousState() == 3:
                changeState(3)
            else:
                changeState(1)
