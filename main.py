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
        self.timer = 0
        self.index = 0
        self.score = 0

        self.font = pygame.font.Font("font.ttf", int(cellSize * 1.5))

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

        self.text3Rect.center = screen.get_width() / 2, 9.5 * cellSize
        self.text2Rect.center = screen.get_width() / 2, 9.5 * cellSize
        self.text1Rect.center = screen.get_width() / 2, 9.5 * cellSize

    def update(self):

        if self.index == 19:
            self.snake.move()
            self.collide()
            self.checkFail()
        else:
            self.index +=1



    def draw(self, screen):
        self.fruit.drawFruit(screen)
        self.snake.draw(screen)
        if 0 < self.index <= 6:
            screen.blit(self.text3, self.text3Rect)
        elif 6 < self.index <= 12:
            screen.blit(self.text2, self.text2Rect)
        elif 12 < self.index <= 18:
            screen.blit(self.text1, self.text1Rect)
        screen.blit(self.scoreText, self.scoreRect)

    def collide(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize(self.snake.body)
            self.snake.addBlock()
            self.score += 1
            self.scoreText = self.font.render(str(self.score), False, "#FFFFFF")
            self.scoreRect = self.scoreText.get_rect()
            self.scoreRect.topleft = (10, 10)

    def checkFail(self):
        if not 0 <= self.snake.body[0].x < cellNumber or not 0 <= self.snake.body[0].y < cellNumber:
            self.gameOver()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.gameOver()


    def gameOver(self):
        changeState(3)
        self.snake.setDefaults()
        self.fruit.setDefaults()
        self.index = 0
        self.score = 0

        self.scoreText = self.font.render(str(self.score), False, "#FFFFFF")
        self.scoreRect = self.scoreText.get_rect()
        self.scoreRect.topleft = (10, 10)

class mainScreen:
    def __init__(self, screen):
        self.screen = screen
        self.state = 1

        self.mainFont = pygame.font.Font('font.ttf', int(cellSize * 1.5) )
        self.miniFont = pygame.font.Font('font.ttf', int(cellSize * 0.8) - (cellSize //10) )

        self.mainText = self.mainFont.render('Main Screen', False, "#FFFFFF")
        self.mainTextRect = self.mainText.get_rect()

        self.startText = self.miniFont.render("Start game", False, "#FFFFFF")
        self.startTextRect = self.startText.get_rect()
        self.leaderboardText = self.miniFont.render("Leaderboard", False,"#FFFFFF")
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

class gameOverScreen:
    def __init__(self):
        self.mainFont = pygame.font.Font('font.ttf', int(cellSize * 1.5))
        self.miniFont = pygame.font.Font('font.ttf', int(cellSize * 0.5))
        self.midiFont = pygame.font.Font('font.ttf', cellSize - (cellSize // 10))

        self.mainText = self.mainFont.render('Game over', False, "#FFFFFF")
        self.mainTextRect = self.mainText.get_rect()

        self.menuText = self.miniFont.render("Back to Main Menu", False, "#FFFFFF")
        self.menuTextRect = self.menuText.get_rect()


        self.leaderBoardText = self.miniFont.render("To Leaderboard", False,"#FFFFFF")
        self.leaderBoardTextRect = self.leaderBoardText.get_rect()

        self.retryText = self.miniFont.render("Retry", False, "#FFFFFF")
        self.retryTextRect = self.retryText.get_rect()

        self.mainTextRect.center = (screen.get_width()//2, screen.get_height() // 2 - (screen.get_height() // 6))

        self.menuTextRect.center = (self.mainTextRect.centerx, self.mainTextRect.y + (self.mainTextRect.height * 2))

        self.leaderBoardTextRect.center = (self.menuTextRect.centerx, self.menuTextRect.y + int(self.mainTextRect.height * 1.5))

        self.retryTextRect.center = (self.leaderBoardTextRect.centerx, self.leaderBoardTextRect.y + int(self.mainTextRect.height * 1.5))


        self.menuBackgroundRect = pygame.Rect(int(self.menuTextRect.x * 0.935), int(self.menuTextRect.y * 0.97) , self.menuTextRect.width + self.menuTextRect.width * 0.1,
                                              self.menuTextRect.height * 2)

        self.leaderBoardBackgroundRect = pygame.Rect(int(self.leaderBoardTextRect.x * 0.94),
                                                     int(self.leaderBoardTextRect.y * 0.97),
                                                     self.leaderBoardTextRect.width + self.leaderBoardTextRect.width * 0.1,
                                                    self.leaderBoardTextRect.height * 2)

        self.retryBackgroundRect = pygame.Rect(int(self.retryTextRect.x * 0.94),
                                                     int(self.retryTextRect.y * 0.97),
                                                     self.retryTextRect.width + self.retryTextRect.width * 0.40,
                                                     self.retryTextRect.height * 2.5)

    def draw(self, surface):
        surface.blit(self.mainText, self.mainTextRect)
        pygame.draw.rect(surface, "#555555", self.menuBackgroundRect)
        pygame.draw.rect(surface, "#555555", self.leaderBoardBackgroundRect)
        pygame.draw.rect(surface, "#555555", self.retryBackgroundRect)

        surface.blit(self.menuText, self.menuTextRect)
        surface.blit(self.leaderBoardText, self.leaderBoardTextRect)
        surface.blit(self.retryText, self.retryTextRect)

        self.pressButtons()

    def pressButtons(self):
        mousePos = pygame.mouse.get_pos()
        mouseButton = pygame.mouse.get_pressed()
        if self.retryBackgroundRect.topleft[0] <= mousePos[0] <= self.retryBackgroundRect.bottomright[0] and self.retryBackgroundRect.topleft[1] <= mousePos[1] <= self.retryBackgroundRect.bottomright[1] and mouseButton[0]:
            changeState(2)
        elif self.menuBackgroundRect.topleft[0] <= mousePos[0] <= self.menuBackgroundRect.bottomright[0] and \
                self.menuBackgroundRect.topleft[1] <= mousePos[1] <= self.menuBackgroundRect.bottomright[1] and mouseButton[0]:
            changeState(1)

class nameScreen:
    def __init__(self):
        self.font = pygame.font.Font('font.ttf', cellSize * 2)

        #self.A = self.font.render("A", False, "#FFFFFF")
        self.A = self.font.render("A", False, "#FFFFFF")
        self.B = self.font.render("B", False, "#FFFFFF")
        self.C = self.font.render("C", False, "#FFFFFF")
        self.Č = self.font.render("Č", False, "#FFFFFF")
        self.D = self.font.render("D", False, "#FFFFFF")
        self.E = self.font.render("E", False, "#FFFFFF")
        self.F = self.font.render("F", False, "#FFFFFF")
        self.G = self.font.render("G", False, "#FFFFFF")
        self.H = self.font.render("H", False, "#FFFFFF")
        self.I = self.font.render("I", False, "#FFFFFF")
        self.J = self.font.render("J", False, "#FFFFFF")
        self.K = self.font.render("K", False, "#FFFFFF")
        self.L = self.font.render("L", False, "#FFFFFF")
        self.M = self.font.render("M", False, "#FFFFFF")
        self.N = self.font.render("N", False, "#FFFFFF")
        self.O = self.font.render("O", False, "#FFFFFF")
        self.P = self.font.render("P", False, "#FFFFFF")
        self.Q = self.font.render("Q", False, "#FFFFFF")
        self.R = self.font.render("R", False, "#FFFFFF")
        self.S = self.font.render("S", False, "#FFFFFF")
        self.Š = self.font.render("Š", False, "#FFFFFF")
        self.T = self.font.render("T", False, "#FFFFFF")
        self.U = self.font.render("U", False, "#FFFFFF")
        self.V = self.font.render("V", False, "#FFFFFF")
        self.Z = self.font.render("Z", False, "#FFFFFF")
        self.Ž = self.font.render("Ž", False, "#FFFFFF")

        self.middle = (screen.get_height() //2 //cellSize ) - 1

        self.ARect = pygame.Rect(cellSize, cellSize * self.middle, cellSize * 2, cellSize * 2)

        self.BRect = pygame.Rect(cellSize * 4, cellSize * self.middle, cellSize * 2, cellSize * 2)
        self.CRect = pygame.Rect(cellSize * 7, cellSize * self.middle, cellSize * 2, cellSize * 2)
        self.ČRect = pygame.Rect(cellSize * 10, cellSize * self.middle, cellSize * 2, cellSize * 2)
        self.DRect = pygame.Rect(cellSize * 13, cellSize * self.middle, cellSize * 2, cellSize * 2)
        self.ERect = pygame.Rect(cellSize * 16, cellSize * self.middle, cellSize * 2,
                                 cellSize * 2)
        self.FRect = pygame.Rect(cellSize * 19, cellSize * self.middle, cellSize * 2,
                                 cellSize * 2)

        self.GRect = pygame.Rect(cellSize, cellSize * self.middle + cellSize * 3  , cellSize * 2,
                                 cellSize * 2)
        self.HRect = pygame.Rect(cellSize * 4, cellSize * self.middle + cellSize * 3, cellSize * 2,
                                 cellSize * 2)
        self.IRect = pygame.Rect(cellSize * 7, cellSize * self.middle + cellSize * 3, cellSize * 2,
                                 cellSize * 2)
        self.JRect = pygame.Rect(cellSize * 10, cellSize * self.middle + cellSize * 3, cellSize * 2,
                                 cellSize * 2)
        self.KRect = pygame.Rect(cellSize * 13, cellSize * self.middle + cellSize * 3, cellSize * 2,
                                 cellSize * 2)
        self.LRect = pygame.Rect(cellSize * 16, cellSize * self.middle + cellSize * 3, cellSize * 2,
                                 cellSize * 2)
        self.MRect = pygame.Rect(cellSize * 19, cellSize * self.middle + cellSize * 3, cellSize * 2,
                                 cellSize * 2)

        self.NRect = pygame.Rect(cellSize, cellSize * self.middle + cellSize * 6,
                                 cellSize * 2,
                                 cellSize * 2)
        self.ORect = pygame.Rect(cellSize * 4, cellSize * self.middle + cellSize * 6,
                                 cellSize * 2,
                                 cellSize * 2)
        self.PRect = pygame.Rect(cellSize * 7, cellSize * self.middle + cellSize * 6,
                                 cellSize * 2,
                                 cellSize * 2)
        self.RRect = pygame.Rect(cellSize * 10, cellSize * self.middle + cellSize * 6,
                                 cellSize * 2,
                                 cellSize * 2)
        self.SRect = pygame.Rect(cellSize * 13, cellSize * self.middle + cellSize * 6,
                                 cellSize * 2,
                                 cellSize * 2)
        self.ŠRect = pygame.Rect(cellSize * 16, cellSize * self.middle + cellSize * 6,
                                 cellSize * 2,
                                 cellSize * 2)
        self.TRect = pygame.Rect(cellSize * 19, cellSize * self.middle + cellSize * 6,
                                 cellSize * 2,
                                 cellSize * 2)

        self.URect = pygame.Rect(cellSize, cellSize * self.middle + cellSize * 9,
                                 cellSize * 2,
                                 cellSize * 2)
        self.VRect = pygame.Rect(cellSize * 4, cellSize * self.middle + cellSize * 9,
                                 cellSize * 2,
                                 cellSize * 2)
        self.ZRect = pygame.Rect(cellSize * 16, cellSize * self.middle + cellSize * 9,
                                 cellSize * 2,
                                 cellSize * 2)
        self.ŽRect = pygame.Rect(cellSize * 19, cellSize * self.middle + cellSize * 9,
                                 cellSize * 2,
                                 cellSize * 2)
        self.SpaceRect = pygame.Rect(cellSize * 7, cellSize * self.middle + cellSize * 9,
                                 cellSize * 8,
                                 cellSize * 2)
        #self.ŠRect = pygame.Rect(cellSize * 16, cellSize * (screen.get_height() // 2 // cellSize) + cellSize * 6,
                                 #cellSize * 2,
                                 #cellSize * 2)
        #self.TRect = pygame.Rect(cellSize * 19, cellSize * (screen.get_height() // 2 // cellSize) + cellSize * 6,
                                 #cellSize * 2,
                                 #cellSize * 2)



    def draw(self, screen):
        colour = "#869d22"



        screen.blit(self.A, self.ARect)
        screen.blit(self.B, self.BRect)
        screen.blit(self.C, self.CRect)
        screen.blit(self.Č, self.ČRect)
        screen.blit(self.D, self.DRect)
        screen.blit(self.E, self.ERect)
        screen.blit(self.F, self.FRect)

        screen.blit(self.G, self.GRect)
        screen.blit(self.H, self.HRect)
        screen.blit(self.I, self.IRect)
        screen.blit(self.J, self.JRect)
        screen.blit(self.K, self.KRect)
        screen.blit(self.L, self.LRect)
        screen.blit(self.M, self.MRect)

        screen.blit(self.N, self.NRect)
        screen.blit(self.O, self.ORect)
        screen.blit(self.P, self.PRect)
        screen.blit(self.R, self.RRect)
        screen.blit(self.S, self.SRect)
        screen.blit(self.Š, self.ŠRect)
        screen.blit(self.T, self.TRect)

        screen.blit(self.U, self.URect)
        screen.blit(self.V, self.VRect)
        screen.blit(self.Z, self.ZRect)
        screen.blit(self.Ž, self.ŽRect)







class logic:
    state = 4
    def __init__(self):
        self.mainGame = mainGame()
        self.mainScreen = mainScreen(screen)
        self.gameOverScreen = gameOverScreen()
        self.nameScreen = nameScreen()

    def events(self, event):
        if event.type == SCREEN_UPDATE and logic.state == 2:
            self.mainGame.update()
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_w or event.key == pygame.K_UP) and self.mainGame.snake.currentDirection.y != 1:
                self.mainGame.snake.direction = Vector2(0, -1)
            elif (event.key == pygame.K_s or event.key == pygame.K_DOWN) and self.mainGame.snake.currentDirection.y != -1:
                self.mainGame.snake.direction = Vector2(0, 1)
            elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and self.mainGame.snake.currentDirection.x != -1:
                self.mainGame.snake.direction = Vector2(1, 0)
            elif (event.key == pygame.K_a or event.key == pygame.K_LEFT) and self.mainGame.snake.currentDirection.x != 1:

                self.mainGame.snake.direction = Vector2(-1, 0)

    def drawAndUpdate(self, screen):
        if logic.state == 1:
            self.mainScreen.draw(screen)
        elif logic.state == 2:
            self.mainGame.draw(screen)
        elif logic.state == 3:
            self.gameOverScreen.draw(screen)
        elif logic.state == 4:
            self.nameScreen.draw(screen)



game = logic()

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

