import pygame, random
from pygame import Vector2
from constants import *

class Fruit:

    def __init__(self):
        self.x = 14
        self.y = 9
        self.pos = Vector2(self.x, self.y)
        self.jabolko = pygame.image.load("graphics/jabolko16.png").convert_alpha()
        self.jabolko = pygame.transform.scale(self.jabolko, (cellSize, cellSize))

    def drawFruit(self, screen):
        fruitRect = pygame.Rect(self.pos.x * cellSize, self.pos.y * cellSize, cellSize, cellSize)
        screen.blit(self.jabolko, fruitRect)
        #pygame.draw.rect(screen, (126,166,114), fruitRect)

    def randomize(self, snakeBody):
        self.x = random.randint(0, cellNumber - 1)
        self.y = random.randint(0, cellNumber - 1)
        self.pos = Vector2(self.x, self.y)
        for snake in snakeBody:
            if snake == self.pos:
                self.randomize(snakeBody)

    def setDefaults(self):
        self.x = 14
        self.y = 9
        self.pos = Vector2(self.x, self.y)