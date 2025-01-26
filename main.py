import sys
import pygame
import random
from pygame.math import Vector2

class Snake:
    def getImage(self, x, y, scale):
        slika = pygame.Surface((16, 16)).convert_alpha()
        slika.blit(self.snakeSpriteSheet, (0, 0), (x, y, 16, 16))
        slika = pygame.transform.scale(slika, (cellSize, cellSize))
        slika.set_colorkey((255, 255, 0))
        return slika

    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(1, 0)
        self.newBlock = False
        self.currentDirection = self.direction


        self.snakeSpriteSheet = pygame.image.load("Graphics/snake.png").convert_alpha()

        self.head_up = self.getImage(16, 0, cellSize)
        self.head_down = self.getImage(48, 0, cellSize)
        self.head_right = self.getImage(0, 0, cellSize)
        self.head_left = self.getImage(32, 0, cellSize)

        self.tail_up = self.getImage(48, 32, cellSize)
        self.tail_down = self.getImage(16, 32, cellSize)
        self.tail_right = self.getImage(32, 32, cellSize)
        self.tail_left = self.getImage(0, 32, cellSize)

        self.body_vertical = self.getImage(0, 48, cellSize)
        self.body_horizontal = self.getImage(16, 48, cellSize)

        self.body_tr = self.getImage(0, 16, cellSize)
        self.body_tl = self.getImage(16, 16, cellSize)
        self.body_br = self.getImage(48, 16, cellSize)
        self.body_bl = self.getImage(32, 16, cellSize)

        self.head = self.head_right

    def draw(self):
        self.updateHead()
        self.updateTail()
        for i, block in enumerate(self.body):
            x_pos = int(block.x * cellSize)
            y_pos = int(block.y * cellSize)
            blockRect = pygame.Rect(x_pos, y_pos, cellSize, cellSize)


            if i == 0:
                screen.blit(self.head, blockRect)
            elif i == len(self.body) - 1:
                screen.blit(self.tail, blockRect)
            else:
                previousBlock = self.body[i + 1] - block
                nextBlock = self.body[i - 1] - block

                if previousBlock.x == nextBlock.x:
                    screen.blit(self.body_vertical, blockRect)
                elif previousBlock.y == nextBlock.y:
                    screen.blit(self.body_horizontal, blockRect)
                else:
                    if previousBlock.x == -1 and nextBlock.y == -1 or previousBlock.y == -1 and nextBlock.x == -1:
                        screen.blit(self.body_tl, blockRect)

                    elif previousBlock.x == -1 and nextBlock.y == 1 or previousBlock.y == 1 and nextBlock.x == -1:
                        screen.blit(self.body_bl, blockRect)
                    elif previousBlock.x == 1 and nextBlock.y == -1 or previousBlock.y == -1 and nextBlock.x == 1:
                        screen.blit(self.body_tr, blockRect)

                    elif previousBlock.x == 1 and nextBlock.y == 1 or previousBlock.y == 1 and nextBlock.x == 1:
                        screen.blit(self.body_br, blockRect)

    def updateHead(self):
        if self.currentDirection == Vector2(-1, 0): self.head = self.head_left
        elif self.currentDirection == Vector2(1, 0): self.head = self.head_right
        elif self.currentDirection == Vector2(-0, 1): self.head = self.head_down
        elif self.currentDirection == Vector2(0, -1): self.head = self.head_up

    def updateTail(self):
        relacija = self.body[ len(self.body) - 1] - self.body[len(self.body) - 2]
        if relacija == Vector2(1, 0) : self.tail = self.tail_right
        elif relacija == Vector2(-1, 0): self.tail = self.tail_left
        elif relacija == Vector2(0, 1): self.tail = self.tail_down
        elif relacija == Vector2(0, -1): self.tail = self.tail_up


    def move(self):
        self.currentDirection = self.direction
        if self.newBlock:
            bodyCopy = self.body[:]  # tole nardi novo kopijo telese, z zdanjim delom
            self.newBlock = False
        else:
            bodyCopy = self.body[:-1] #tole nardi novo kopijo telese, brez zdanjega dela
        bodyCopy.insert(0, bodyCopy[0] + self.direction)
        self.body = bodyCopy[:]

    def addBlock(self):
        self.newBlock = True



class Fruit:
    def __init__(self):
        self.x = random.randint(0, cellNumber - 1 )
        self.y = random.randint(0, cellNumber - 1)
        self.pos = Vector2(self.x, self.y)

    def drawFruit(self):
        fruitRect = pygame.Rect(self.pos.x * cellSize, self.pos.y * cellSize, cellSize, cellSize)
        screen.blit(jabolko, fruitRect)
        #pygame.draw.rect(screen, (126,166,114), fruitRect)

    def randomize(self):
        self.x = random.randint(0, cellNumber - 1)
        self.y = random.randint(0, cellNumber - 1)
        self.pos = Vector2(self.x, self.y)

class main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def update(self):
        self.snake.move()
        self.collide()
        self.checkFail()

    def draw(self):
        self.fruit.drawFruit()
        self.snake.draw()

    def collide(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.addBlock()

    def checkFail(self):
        if not 0 <= self.snake.body[0].x < cellNumber or not 0 <= self.snake.body[0].y < cellNumber:
            self.gameOver()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.gameOver()


    def gameOver(self):
        pygame.quit()
        sys.exit()

cellSize = 64
cellNumber = 20

pygame.init()

screen = pygame.display.set_mode( (cellSize * cellNumber, cellSize * cellNumber) )
clock = pygame.time.Clock()
jabolko = pygame.image.load("graphics/jabolko16.png").convert_alpha()
jabolko = pygame.transform.scale(jabolko, (cellSize, cellSize))

SCREEN_UPDATE = pygame.USEREVENT#tle nardimo svoj event
pygame.time.set_timer(SCREEN_UPDATE, 150)#in executamo tale event vsakih 150ms

mainGame = main()





while True:
    screen.fill("#AFD746")



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            mainGame.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and mainGame.snake.currentDirection.y != 1:
                mainGame.snake.direction = Vector2(0, -1)

            if event.key == pygame.K_s and mainGame.snake.currentDirection.y != -1:
                mainGame.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_d and mainGame.snake.currentDirection.x != -1:
                mainGame.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_a and mainGame.snake.currentDirection.x != 1:
                mainGame.snake.direction = Vector2(-1, 0)

            if event.key == pygame.K_UP and mainGame.snake.currentDirection.y != 1:
                mainGame.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and mainGame.snake.currentDirection.y != -1:
                mainGame.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_RIGHT and mainGame.snake.currentDirection.x != -1:
                mainGame.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_LEFT and mainGame.snake.currentDirection.x != 1:
                mainGame.snake.direction = Vector2(-1, 0)

    mainGame.draw()
    pygame.display.update()
    clock.tick(60)
