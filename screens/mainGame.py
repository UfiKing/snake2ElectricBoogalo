import pygame
from constants import cellSize, cellNumber
from elements import fruit
from elements.snake import Snake
from elements.fruit import Fruit
from gameLogic import *


class mainGame:
    def killApples(self):
        self.fruit = []
        self.badFruit = []
        for i in range(getNumberOfApples()):
            self.fruit.append(Fruit(self.snake))
            if getBadApples():
                self.badFruit.append(Fruit(self.snake, True))
                self.badFruit[i].randomize(self.snake.body)
        for i in range(getNumberOfApples() - 1):
            self.fruit[i + 1].randomize(self.snake.body)

    def __init__(self):
        self.snake = Snake()

        self.killApples()
        setDead()
        self.timer = 0
        self.index = 0
        self.score = 0

        self.font = pygame.font.Font("graphics/font.ttf", int(cellSize * 1.5))

        self.scoreText = self.font.render(str(self.score), False, "#FFFFFF")
        self.scoreRect = self.scoreText.get_rect()

        self.scoreRect.topleft = (10, 10)

        self.text0 = self.font.render("0", False, "#FFFFFF")
        self.text1 = self.font.render("1", False, "#FFFFFF")
        self.text2 = self.font.render("2", False, "#FFFFFF")
        self.text3 = self.font.render("3", False, "#FFFFFF")

        self.text0Rect = self.text0.get_rect()
        self.text1Rect = self.text1.get_rect()
        self.text2Rect = self.text2.get_rect()
        self.text3Rect = self.text3.get_rect()

        self.text3Rect.center = cellNumber // 2 * cellSize, cellNumber // 2 * cellSize
        self.text2Rect.center = cellNumber // 2 * cellSize, cellNumber // 2 * cellSize
        self.text1Rect.center = cellNumber // 2 * cellSize, cellNumber // 2 * cellSize

        self.badFruit = [Fruit(self.snake, True)]
        self.badFruit[0].randomize(self.snake.body)

    def update(self,screen):
        if getLivingState():
            self.killApples()
            setAlive()
        if self.index == 19:
            if not getGameState():
                self.snake.move()
                self.collide()
                self.checkFail()

        else:
            self.index += 1


    def draw(self, screen):
        badApples = getBadApples()

        for apple in self.fruit:
            apple.drawFruit(screen)
        self.snake.draw(screen)
        if 0 < self.index <= 6:
            screen.blit(self.text3, self.text3Rect)
        elif 6 < self.index <= 12:
            screen.blit(self.text2, self.text2Rect)
        elif 12 < self.index <= 18:
            screen.blit(self.text1, self.text1Rect)
        screen.blit(self.scoreText, self.scoreRect)
        if badApples:
            for badFruit in self.badFruit:
                badFruit.drawFruit(screen)

        if getGameState():
            self.pauseScreen(screen)

    def collide(self):

        for i, apple in enumerate(self.fruit):
            if apple.pos == self.snake.body[0]:
                apple.randomize(self.snake.body)
                self.snake.addBlock()
                self.score += 1
                self.scoreText = self.font.render(str(self.score), False, "#FFFFFF")
                self.scoreRect = self.scoreText.get_rect()
                self.scoreRect.topleft = (10, 10)
                if getBadApples():
                    self.badFruit[i].randomize(self.snake.body)

        for badApple in self.badFruit:
            if badApple.pos == self.snake.body[0] and getBadApples():
                self.gameOver()


    def checkFail(self):
        pacifist = getPacifist()
        if not 0 <= self.snake.body[0].x < cellNumber or not 0 <= self.snake.body[0].y < cellNumber:
            head = self.snake.body[0]
            if pacifist:
                if head.x > cellNumber + 1:
                    head.x = -1
                elif head.x < 0:
                    head.x = cellNumber + 1
                elif head.y > cellNumber + 1:
                    head.y = -1
                elif head.y < 0:
                    head.y = cellNumber +1
            else:
                self.gameOver()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0] and not pacifist:
                self.gameOver()

    def gameOver(self):
        changeState(3)

        addToDB(getUsername(), self.score)

        changeId(getTopId())
        self.snake.setDefaults()
        setDead()

        self.index = 0
        self.score = 0

        self.scoreText = self.font.render(str(self.score), False, "#FFFFFF")
        self.scoreRect = self.scoreText.get_rect()
        self.scoreRect.topleft = (10, 10)

    def pauseScreen(self, surface):
        font = pygame.font.Font("graphics/font.ttf", int(cellSize * 0.8))

        rect = pygame.Rect(0, 0, cellSize * 10, 10 * cellSize)
        rect.centerx = cellNumber // 2 * cellSize
        rect.centery = cellNumber // 2 * cellSize

        outerRect = pygame.Rect(0, 0, int(cellSize * 10.5), int(cellSize * 10.5))
        outerRect.centerx = cellNumber // 2 * cellSize
        outerRect.centery = cellNumber // 2 * cellSize

        pygame.draw.rect(surface, "#000000", outerRect)
        pygame.draw.rect(surface, "#F0AC92", rect)

        text = font.render("Pause game", False, "#FFFFFF")
        textRect = text.get_rect()
        textRect.centerx = rect.centerx
        textRect.centery = (cellNumber // 2 - 4) * cellSize




        quitText = font.render("Quit", False, "#FFFFFF")
        quitTextRect = quitText.get_rect()
        quitTextRect.centerx = rect.centerx
        quitTextRect.centery = (cellNumber // 2 - 1) * cellSize
        pygame.draw.rect(surface, "#000000", quitTextRect)

        quitTextBackground = quitTextRect.copy()
        quitTextBackground.x -= cellSize // 2
        quitTextBackground.y -= cellSize // 2
        quitTextBackground.width += cellSize
        quitTextBackground.height += cellSize
        pygame.draw.rect(surface, "#000000", quitTextBackground)


        resumeText = font.render("Resume", False, "#FFFFFF")
        resumeTextRect = resumeText.get_rect()
        resumeTextRect.centerx = rect.centerx
        resumeTextRect.centery = (cellNumber // 2 + 2) * cellSize

        resumeTextBackground = resumeTextRect.copy()
        resumeTextBackground.x -= cellSize // 2
        resumeTextBackground.y -= cellSize // 2
        resumeTextBackground.width += cellSize
        resumeTextBackground.height += cellSize
        pygame.draw.rect(surface, "#000000", resumeTextBackground)

        surface.blit(text, textRect)
        surface.blit(quitText, quitTextRect)
        surface.blit(resumeText, resumeTextRect)

        mousePos = pygame.mouse.get_pos()
        mouseButtons = pygame.mouse.get_pressed()
        if quitTextBackground.collidepoint(mousePos):
            if mouseButtons[0]:
                self.gameOver()
        if resumeTextBackground.collidepoint(mousePos):
            if mouseButtons[0]:
                switchGameState()
