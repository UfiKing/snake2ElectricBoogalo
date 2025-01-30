import sys
import pygame
from snake import Snake
from fruit import Fruit
from pygame import Vector2
from constants import cellSize, cellNumber
import sqlite3

connection = sqlite3.connect("leaderboard.db")
cursor = connection.cursor()

pygame.init()

screen = pygame.display.set_mode( (cellSize * cellNumber, cellSize * cellNumber) )
clock = pygame.time.Clock()


SCREEN_UPDATE = pygame.USEREVENT#tle nardimo svoj event
pygame.time.set_timer(SCREEN_UPDATE, 150)#in executamo tale event vsakih 150ms



def changeState(newState):
    logic.state = newState
    getLeaderboard()

def changeUsername(newUsername):
    logic.name = newUsername

def addToDB(name, score):
    data = [name, score]
    print(type(name))
    cursor.execute("INSERT INTO leaderboard (name, score) VALUES (?, ?)", data)
    connection.commit()

def updateDB(name, score):
    data = [name, score]
    cursor.execute("UPDATE `movies` SET score=? WHERE name=?", data)
    connection.commit()


def getLeaderboard():
    result = cursor.execute("SELECT * FROM leaderboard ORDER BY score DESC limit 10").fetchall()
    print(result)

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
        addToDB(logic.name, self.score)
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
            changeState(4)

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
            changeState(4)

class nameScreen:
    def __init__(self):


        self.font = pygame.font.Font('font.ttf', int(cellSize *1))

        self.middle = (screen.get_height() // 2 // cellSize) - 1

        self.name = []
        self.pressed = False
        self.inputRect = pygame.Rect(cellSize * 2, cellSize * self.middle - cellSize * 2, cellSize * 18, cellSize * 3)

        self.nameText = self.font.render("".join(self.name), False, "#FFFFFF")
        self.nameTextRect = self.nameText.get_rect()
        self.backspace = False

        self.defaultText = self.font.render("ime", False, "#FFFFFF")
        self.defaultTextRect = self.defaultText.get_rect()
        self.defaultTextRect.bottomleft = self.inputRect.bottomleft
        self.defaultTextRect.y -= cellSize

        self.nameTextRect.bottomleft = self.inputRect.bottomleft
        self.nameTextRect.y -= cellSize

        self.submitText = self.font.render("Go!", False, "#FFFFFF")
        self.submitTextRect = self.submitText.get_rect()

        self.submitTextRect.y = self.defaultTextRect.y + cellSize * 4
        self.submitTextRect.centerx = self.inputRect.centerx
        self.submitTextRect.width += cellSize * 2
        self.submitTextRect.height += cellSize

    def update(self, surface):
        mousePos = pygame.mouse.get_pos()
        mousePressed = pygame.mouse.get_pressed()

        if self.inputRect.topleft[0] <= mousePos[0] <= self.inputRect.bottomright[0] and self.inputRect.topleft[1] <= mousePos[1] <= \
                self.inputRect.bottomright[1] :
            #this checks if the mouse is inside the text enter box
            if not self.pressed:
                #if it is and the pressed variable isnt on, it colours the box the hover colour
                pygame.draw.rect(surface, "#AF65FA", self.inputRect)
            if mousePressed[0]:
                #if its inside and the user presses the mouse, it sets the pressed variable to True
                self.pressed = True
        else:
            # if it isnt inside the box draw the default colour
            pygame.draw.rect(screen, "#888888", self.inputRect)

        if self.pressed:
            #if the button is pressed, draw the pressed colour (overwriting any colour drawn before)
            pygame.draw.rect(surface, "#000000", self.inputRect)

        #if the name list is less than 1 (so its empty and no name has been entered yet)
        #display the default text (ime)
        #else display the text inputed by the user
        if len(self.name) < 1:
            screen.blit(self.defaultText, self.defaultTextRect)
        else:
            screen.blit(self.nameText, self.nameTextRect)

        #if the user presses outside the input text thingi, set self.pressed to false
        if (self.inputRect.topleft[0] > mousePos[0] or mousePos[0] > self.inputRect.bottomright[0] or self.inputRect.topleft[1] > mousePos[1] or \
                mousePos[1] > self.inputRect.bottomright[1]) and mousePressed[0]:
            self.pressed = False

        #this rerenders the text
        self.nameText = self.font.render("".join(self.name), False, "#FFFFFF")
        self.nameTextRect = self.nameText.get_rect()
        self.nameTextRect.bottomleft = self.inputRect.bottomleft
        self.nameTextRect.y -= cellSize

        self.submitTextRect.centerx -= cellSize
        self.submitTextRect.y -= cellSize * .5
        if self.submitTextRect.topleft[0] <= mousePos[0] <= self.submitTextRect.bottomright[0] and \
                self.submitTextRect.topleft[1] <= mousePos[1] <= self.submitTextRect.bottomright[1]:
            pygame.draw.rect(surface, "#30FF30", self.submitTextRect)

            if mousePressed[0]:
                self.submit()
        else:
            pygame.draw.rect(surface, "#30af30", self.submitTextRect)

        self.submitTextRect.centerx += cellSize
        self.submitTextRect.y += cellSize * 0.5

        screen.blit(self.submitText, self.submitTextRect)

    def submit(self):
        if len(self.name) < 1:
            username = "anon"
        else:
            username = "".join(self.name)
        logic.name = username
        changeState(2)

class leaderboardScreen:
    def __init__(self):
        self.font = pygame.font.Font('font.ttf', cellSize)
        self.fontBig = pygame.font.Font('font.ttf', int(cellSize * 1.5))

        self.leaderBoardText = self.fontBig.render("Leaderboard", False, "#FFFFFF")
        self.leaderBoardTextRect = self.leaderBoardText.get_rect()
        self.leaderBoardTextRect.centerx = screen.get_width() // 2
        self.leaderBoardTextRect.centery += cellSize

        self.left = cellSize
        self.right = screen.get_width() - screen.get_width() // 4

        self.firstPlace = self.font.render("1. Anon: 0", False, "#FFFFFF")
        self.firstPlaceRect = self.firstPlace.get_rect()
        self.firstPlaceRect.left = self.left
        self.firstPlaceRect.y += cellSize * 3

        self.secondPlace = self.font.render("2. Anon: 0", False, "#FFFFFF")
        self.secondPlaceRect = self.secondPlace.get_rect()
        self.secondPlaceRect.left = self.left
        self.secondPlaceRect.y += self.firstPlaceRect.y + cellSize * 2

        self.thirdPlace = self.font.render("3. Anon: 0", False, "#FFFFFF")
        self.thirdPlaceRect = self.thirdPlace.get_rect()
        self.thirdPlaceRect.left = self.left
        self.thirdPlaceRect.y += self.secondPlaceRect.y + cellSize * 2

        self.fourthPlace = self.font.render("4. Anon: 0", False, "#FFFFFF")
        self.fourthPlaceRect = self.fourthPlace.get_rect()
        self.fourthPlaceRect.left = self.left
        self.fourthPlaceRect.y += self.thirdPlaceRect.y + cellSize * 2

        self.fifthPlace = self.font.render("5. Anon: 0", False, "#FFFFFF")
        self.fifthPlaceRect = self.fifthPlace.get_rect()
        self.fifthPlaceRect.left = self.left
        self.fifthPlaceRect.y += self.fourthPlaceRect.y + cellSize * 2

        self.sixthPlace = self.font.render("6. Anon: 0", False, "#FFFFFF")
        self.sixthPlaceRect = self.sixthPlace.get_rect()
        self.sixthPlaceRect.left = self.left
        self.sixthPlaceRect.y += self.fifthPlaceRect.y + cellSize * 2

        self.seventhPlace = self.font.render("7. Matej Zorec: 0", False, "#FFFFFF")
        self.seventhPlaceRect = self.seventhPlace.get_rect()
        self.seventhPlaceRect.left = self.left
        self.seventhPlaceRect.y = self.sixthPlaceRect.y + cellSize * 2

        self.eightPlace = self.font.render("8. Anon: 0", False, "#FFFFFF")
        self.eightPlaceRect = self.eightPlace.get_rect()
        self.eightPlaceRect.left = self.lef
        self.eightPlaceRect.y = self.seventhPlaceRect.y + cellSize * 2

        self.ninthPlace = self.font.render("9. Anon: 0", False, "#FFFFFF")
        self.ninthPlaceRect = self.ninthPlace.get_rect()
        self.ninthPlaceRect.left = self.left
        self.ninthPlaceRect.y += self.eightPlaceRect.y + cellSize * 2

        self.tenthPlace = self.font.render("10. Anon: 0", False, "#FFFFFF")
        self.tenthPlaceRect = self.tenthPlace.get_rect()
        self.tenthPlaceRect.left = self.left
        self.tenthPlaceRect.y += self.ninthPlaceRect.y + cellSize * 2

    def update(self, surface):
        surface.blit(self.leaderBoardText, self.leaderBoardTextRect)

        surface.blit(self.firstPlace, self.firstPlaceRect)
        surface.blit(self.secondPlace, self.secondPlaceRect)
        surface.blit(self.thirdPlace, self.thirdPlaceRect)
        surface.blit(self.fourthPlace, self.fourthPlaceRect)
        surface.blit(self.fifthPlace, self.fifthPlaceRect)
        surface.blit(self.sixthPlace, self.sixthPlaceRect)
        surface.blit(self.seventhPlace, self.seventhPlaceRect)
        surface.blit(self.eightPlace, self.eightPlaceRect)
        surface.blit(self.ninthPlace, self.ninthPlaceRect)
        surface.blit(self.tenthPlace, self.tenthPlaceRect)

class logic:
    state = 5
    name = "anon"
    def __init__(self):
        self.mainGame = mainGame()
        self.mainScreen = mainScreen(screen)
        self.gameOverScreen = gameOverScreen()
        self.nameScreen = nameScreen()
        self.leaderboardScreen = leaderboardScreen()

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
        if event.type != SCREEN_UPDATE:
            #print(pygame.event.event_name(event.type))
            pass
        if event.type == pygame.TEXTINPUT and self.nameScreen.pressed:
            print(pygame.event.event_name(event.type))
            print(event.text)
            self.nameScreen.name.append(event.text)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE and len(self.nameScreen.name) > 0 and self.nameScreen.pressed:
            self.nameScreen.name.pop()
            print("back")

    def drawAndUpdate(self, screen):
        if logic.state == 1:
            self.mainScreen.draw(screen)
        elif logic.state == 2:
            self.mainGame.draw(screen)
        elif logic.state == 3:
            self.gameOverScreen.draw(screen)
        elif logic.state == 4:
            self.nameScreen.update(screen)
        elif logic.state == 5:
            self.leaderboardScreen.update(screen)



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

