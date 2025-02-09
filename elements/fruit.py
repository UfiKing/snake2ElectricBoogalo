import pygame, random
from pygame import Vector2
from constants import *

class Fruit:

    def __init__(self, snake, bad=False):
        #self.x = cellNumber // 2 + 3
        #self.y = cellNumber // 2
        #self.pos = Vector2(self.x, self.y)
        self.setDefaults(snake)
        self.jabolko = pygame.image.load("graphics/jabolko16.png").convert_alpha()
        self.jabolko = pygame.transform.scale(self.jabolko, (cellSize, cellSize))

        if bad:
            self.jabolko = pygame.image.load("graphics/jabloko16.bad.png").convert_alpha()
            self.jabolko = pygame.transform.scale(self.jabolko, (cellSize, cellSize))

    def drawFruit(self, screen):
        fruitRect = pygame.Rect(self.pos.x * cellSize, self.pos.y * cellSize, cellSize, cellSize)
        screen.blit(self.jabolko, fruitRect)

    def randomize(self, snakeBody):
        self.x = random.randint(0, cellNumber - 1)
        self.y = random.randint(0, cellNumber - 1)
        self.pos = Vector2(self.x, self.y)
        for snake in snakeBody:
            if snake == self.pos:
                self.randomize(snakeBody)

    def setDefaults(self, snake):
        self.x = cellNumber // 2 + 3
        self.y = cellNumber // 2
        self.pos = Vector2(self.x, self.y)
        for body in snake.body:
            if body == self.pos:
                self.setDefaults(body)
