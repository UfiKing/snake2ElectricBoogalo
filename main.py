import sys
import pygame
from constants import cellSize, cellNumber
from logic import logic


pygame.init()

screen = pygame.display.set_mode( (cellSize * cellNumber, cellSize * cellNumber) )
clock = pygame.time.Clock()


game = logic(screen)

def drawGrid(screen):
    for i in range(cellNumber):
        for j in range(cellNumber):
            if i % 2 == 0:
                if j % 2 == 0:
                    pygame.draw.rect(screen, "#AFD746", pygame.Rect(i * cellSize, j * cellSize, cellSize, cellSize))
                    pygame.draw.rect(screen, "#b9dc5c", pygame.Rect((i + 1) * cellSize, j * cellSize, cellSize, cellSize))
                else:
                    pygame.draw.rect(screen, "#AFD746", pygame.Rect((i+1) * cellSize, j * cellSize, cellSize, cellSize))
                    pygame.draw.rect(screen, "#b9dc5c",
                                     pygame.Rect(i * cellSize, j * cellSize, cellSize, cellSize))

while True:
    #screen.fill("#AFD746")
    drawGrid(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        game.events(event)

    game.drawAndUpdate(screen)

    pygame.display.update()
    clock.tick(60)