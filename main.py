import sys
import pygame
from snake import Snake
from fruit import Fruit
from pygame import Vector2
from constants import cellSize, cellNumber



pygame.init()

screen = pygame.display.set_mode( (cellSize * cellNumber, cellSize * cellNumber) )
clock = pygame.time.Clock()


SCREEN_UPDATE = pygame.USEREVENT#tle nardimo svoj event
pygame.time.set_timer(SCREEN_UPDATE, 150)#in executamo tale event vsakih 150ms

class mainGame:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def update(self):
        self.snake.move()
        self.collide()
        self.checkFail()

    def draw(self, screen):
        self.fruit.drawFruit(screen)
        self.snake.draw(screen)

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
        changeState(1)
        self.snake.setDefaults()
        self.fruit.randomize()

class mainScreen:
    def __init__(self, screen):
        self.screen = screen
        self.state = 1

        self.mainFont = pygame.font.Font('freesansbold.ttf', cellSize *2)
        self.miniFont = pygame.font.Font('freesansbold.ttf', cellSize - (cellSize //10) )

        self.mainText = self.mainFont.render('Main Screen', True, "#FFFFFF")
        self.mainTextRect = self.mainText.get_rect()

        self.startText = self.miniFont.render("Start game", True, "#FFFFFF")
        self.startTextRect = self.startText.get_rect()
        self.leaderboardText = self.miniFont.render("Leaderboard", True,"#FFFFFF")
        self.leaderboardTextRect = self.leaderboardText.get_rect(x=200)

        # set the center of the rectangular object.

        self.mainTextRect.center = (screen.get_width()//2, screen.get_height() // 2 - (screen.get_height() // 4))

        self.startTextRect.midleft = (self.mainTextRect.x , screen.get_height() // 2)
        self.leaderboardTextRect.midright = (self.mainTextRect.width + self.mainTextRect.x , screen.get_height() // 2)

        self.startBackgroundRect = (pygame.Rect
                                (self.startTextRect.centerx - (self.startTextRect.width // 2) - (self.startTextRect.width // 10),
                                self.startTextRect.centery - self.startTextRect.height,
                                self.startTextRect.width + (self.startTextRect.width // 5),
                                self.startTextRect.height * 2))

        self.leaderboardBackgroundRect = (pygame.Rect
                                    (self.leaderboardTextRect.centerx - (self.leaderboardTextRect.width // 2) - (
                                                self.leaderboardTextRect.width // 10),
                                     self.leaderboardTextRect.centery - self.leaderboardTextRect.height,
                                     self.leaderboardTextRect.width + (self.leaderboardTextRect.width // 5),
                                     self.leaderboardTextRect.height * 2))

    def draw(self, surface):
        pygame.draw.rect(surface, "#555555", self.startBackgroundRect)
        pygame.draw.rect(surface, "#005500", self.leaderboardBackgroundRect)
        surface.blit(self.mainText, self.mainTextRect)
        surface.blit(self.startText, self.startTextRect)
        surface.blit(self.leaderboardText, self.leaderboardTextRect)
        self.pressButtons()

    def pressButtons(self):
        mousePos = pygame.mouse.get_pos()
        mouseButton = pygame.mouse.get_pressed()

        if self.startBackgroundRect.topleft[0] <= mousePos[0] <= self.startBackgroundRect.bottomright[0]\
                and self.startBackgroundRect.topleft[1] <= mousePos[1] <= self.startBackgroundRect.bottomright[1]\
                and mouseButton[0]:
            changeState(2)

def changeState(newState):
    logic.state = newState

class logic:
    state = 1
    def __init__(self):
        self.mainGame = mainGame()
        self.mainScreen = mainScreen(screen)


    def events(self, event):
        if event.type == SCREEN_UPDATE and logic.state == 2:
            self.mainGame.update()
        if event.type == pygame.KEYDOWN:
            print(f"current direction {self.mainGame.snake.direction}, currentDirection = {self.mainGame.snake.currentDirection}")
            if event.key == pygame.K_w or event.key == pygame.K_UP and self.mainGame.snake.currentDirection.y != 1:
                self.mainGame.snake.direction = Vector2(0, -1)
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN and self.mainGame.snake.currentDirection.y != -1:
                self.mainGame.snake.direction = Vector2(0, 1)
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT and self.mainGame.snake.currentDirection.x != -1:
                self.mainGame.snake.direction = Vector2(1, 0)
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT and self.mainGame.snake.currentDirection.x != 1:
                self.mainGame.snake.direction = Vector2(-1, 0)

    def drawAndUpdate(self, screen):
        if logic.state == 1:
            self.mainScreen.draw(screen)
        elif logic.state == 2:
            self.mainGame.draw(screen)


game = logic()


while True:
    screen.fill("#AFD746")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        game.events(event)

    game.drawAndUpdate(screen)



    pygame.display.update()
    clock.tick(60)

