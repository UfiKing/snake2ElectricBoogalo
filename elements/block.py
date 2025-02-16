import pygame
from pygame import Vector2
from constants import cellSize
class Block:
    def __init__(self, x, y):
        self.position = Vector2(x,y)
        self.image = pygame.image.load("graphics/box/normal/box.png")
        self.image = pygame.transform.scale(self.image, (cellSize, cellSize))
        self.imageRect = self.image.get_rect()
        self.imageRect.x = x * cellSize
        self.imageRect.y = y * cellSize

    def draw(self, screen):
        """pygame.draw.rect(screen, (255,255,255),
                         pygame.Rect(self.position.x * cellSize,
                                     self.position.y * cellSize,
                                     cellSize, cellSize))"""
        screen.blit(self.image, self.imageRect)


