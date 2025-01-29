import pygame
import sys


pygame.init()

WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()


def getUserName():
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            MANAGER.proccess(event)

        MANAGER.update(UI_REFRESH_RATE)
        screen.fill("white")



        pygame.display.update()
        clock.tick
getUserName()