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
            if getMode() == 2:
                self.badFruit.append(Fruit(self.snake, True))
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

    def update(self):
        if getLivingState():
            self.killApples()
            setAlive()
        if self.index == 19:
            self.snake.move()
            self.collide()
            self.checkFail()
        else:
            self.index += 1


    def draw(self, screen):
        mode = getMode()

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
        if mode == 2:
            for badFruit in self.badFruit:
                badFruit.drawFruit(screen)


    def collide(self):
        mode = getMode()
        for i, apple in enumerate(self.fruit):
            if apple.pos == self.snake.body[0]:
                apple.randomize(self.snake.body)
                self.snake.addBlock()
                self.score += 1
                self.scoreText = self.font.render(str(self.score), False, "#FFFFFF")
                self.scoreRect = self.scoreText.get_rect()
                self.scoreRect.topleft = (10, 10)
                if getMode() == 2:
                    self.badFruit[i].randomize(self.snake.body)

        for badApple in self.badFruit:
            if badApple.pos == self.snake.body[0] and mode == 2:
                self.gameOver()


    def checkFail(self):
        if not 0 <= self.snake.body[0].x < cellNumber or not 0 <= self.snake.body[0].y < cellNumber:
            self.gameOver()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
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

