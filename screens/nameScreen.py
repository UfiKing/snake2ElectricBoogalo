import pygame
from constants import cellSize, cellNumber
from gameLogic import *

class nameScreen:
    def __init__(self):
        self.font = pygame.font.Font('graphics/font.ttf', int(cellSize * 1))

        self.middle = (cellNumber // 2 * cellSize)

        self.backButton = pygame.image.load("graphics/backArrowLeft32.png")
        self.backButton = pygame.transform.scale(self.backButton, (cellSize * 3, cellSize * 3))
        self.backButtonRect = self.backButton.get_rect()
        self.backButtonRect.centerx = 2 * cellSize
        self.backButtonRect.centery = cellSize * 2

        self.name = []
        self.pressed = False
        self.inputRect = pygame.Rect(cellSize * 2, self.middle - cellSize, (cellNumber - 4) * cellSize, cellSize * 3)

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

        self.appleBad = pygame.image.load("graphics/jabolko16.bad.png")
        self.appleBad = pygame.transform.scale(self.appleBad, (cellSize * 2, cellSize * 2))
        self.appleBadRect = self.appleBad.get_rect()
        self.appleBadRect.left = self.inputRect.left
        self.appleBadRect.bottom = self.inputRect.top - (cellSize * 2)

        self.apple = pygame.image.load("graphics/jabolko16.png")
        self.apple = pygame.transform.scale(self.apple, (cellSize * 2, cellSize * 2))
        self.appleRect = self.apple.get_rect()
        self.appleRect.left = self.inputRect.left
        self.appleRect.bottom = self.inputRect.top - (cellSize * 2)

        self.badAppleOn = False
        self.applePressed = False

        self.numberApple1 = pygame.image.load("graphics/jabolko16_1.png")
        self.numberApple1 = pygame.transform.scale(self.numberApple1, (cellSize * 2, cellSize * 2))
        self.numberAppleRect = self.numberApple1.get_rect()
        self.numberAppleRect.left = self.appleRect.right + cellSize
        self.numberAppleRect.bottom = self.inputRect.top - (cellSize * 2)

        self.numberApple3 = pygame.image.load("graphics/jabolko16_3.png")
        self.numberApple3 = pygame.transform.scale(self.numberApple3, (cellSize * 2, cellSize * 2))

        self.numberApple5 = pygame.image.load("graphics/jabolko16_5.png")
        self.numberApple5 = pygame.transform.scale(self.numberApple5, (cellSize * 2, cellSize * 2))


        self.numberApple1Bad = pygame.image.load("graphics/jabolko16_1.bad.png")
        self.numberApple1Bad = pygame.transform.scale(self.numberApple1Bad, (cellSize * 2, cellSize * 2))

        self.numberApple3Bad = pygame.image.load("graphics/jabolko16_3.bad.png")
        self.numberApple3Bad = pygame.transform.scale(self.numberApple3Bad, (cellSize * 2, cellSize * 2))

        self.numberApple5Bad = pygame.image.load("graphics/jabolko16_5.bad.png")
        self.numberApple5Bad = pygame.transform.scale(self.numberApple5Bad, (cellSize * 2, cellSize * 2))

        self.currentNumberApple = 1
        self.numberApplePressed = False

        self.pacifistOn = pygame.image.load("graphics/pacifistOn.png")
        self.pacifistOn = pygame.transform.scale(self.pacifistOn, (cellSize * 2, cellSize * 2))
        self.pacifistRect = self.pacifistOn.get_rect()
        self.pacifistRect.bottom = self.inputRect.top - (cellSize * 2)
        self.pacifistRect.left = self.numberAppleRect.right + cellSize

        self.pacifistOff = pygame.image.load("graphics/pacifistOff.png")
        self.pacifistOff = pygame.transform.scale(self.pacifistOff, (cellSize * 2, cellSize * 2))

        self.pacifist = True
        self.pacifistPressed = False

    def update(self, surface):
        mousePos = pygame.mouse.get_pos()
        mousePressed = pygame.mouse.get_pressed()
        surface.blit(self.backButton, self.backButtonRect)

        if self.backButtonRect.topleft[0] <= mousePos[0] <= self.backButtonRect.bottomright[0] and \
                self.backButtonRect.topleft[1] <= mousePos[1] <= self.backButtonRect.bottomright[0] and mousePressed[0] :
            changeState(1)

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
            pygame.draw.rect(surface, "#888888", self.inputRect)

        if self.pressed:
            #if the button is pressed, draw the pressed colour (overwriting any colour drawn before)
            pygame.draw.rect(surface, "#000000", self.inputRect)

        #if the name list is less than 1 (so its empty and no name has been entered yet)
        #display the default text (ime)
        #else display the text inputed by the user
        if len(self.name) < 1:
            surface.blit(self.defaultText, self.defaultTextRect)
        else:
            surface.blit(self.nameText, self.nameTextRect)

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

        surface.blit(self.submitText, self.submitTextRect)

        #here we check if the bad apple variavle is on
        # if it is
        if self.badAppleOn:
            #we blit it on the screnn
            surface.blit(self.appleBad, self.appleBadRect)
            #if the mouse is hovering wer display the normal apple
            if self.appleBadRect.topleft[0] <= mousePos[0] <= self.appleBadRect.bottomright[0] and \
                    self.appleBadRect.topleft[1] <= mousePos[1] <= self.appleBadRect.bottomright[1] and not self.applePressed:
                surface.blit(self.apple, self.appleRect)
                #and if the user presses the left mouse button while hovering we set the variable to false
                if getMouseButtonUp():
                    self.badAppleOn = False
                    self.applePressed = True#
        #if the bad apple variable is off we just the the same but in reverse
        else:
            surface.blit(self.apple, self.appleRect)
            if self.appleBadRect.topleft[0] <= mousePos[0] <= self.appleBadRect.bottomright[0] and \
                    self.appleBadRect.topleft[1] <= mousePos[1] <= self.appleBadRect.bottomright[1] and not self.applePressed:
                surface.blit(self.appleBad, self.appleBadRect)
                if getMouseButtonUp():
                    self.badAppleOn = True
                    self.applePressed = True

        if self.appleBadRect.topleft[0] > mousePos[0] or mousePos[0] > self.appleBadRect.bottomright[0] or \
                self.appleBadRect.topleft[1] > mousePos[1] or mousePos[1] > self.appleBadRect.bottomright[1]:
            self.applePressed = False



        if self.currentNumberApple == 1 :
            surface.blit(self.numberApple1, self.numberAppleRect)
            if self.numberAppleRect.topleft[0] <= mousePos[0] <= self.numberAppleRect.bottomright[0] and \
                    self.numberAppleRect.topleft[1] <= mousePos[1] <= self.numberAppleRect.bottomright[
                1] and not self.numberApplePressed:
                surface.blit(self.numberApple3Bad, self.numberAppleRect)
                if getMouseButtonUp():
                    self.currentNumberApple = 3
                    self.numberApplePressed = True

        elif self.currentNumberApple == 3 :
            surface.blit(self.numberApple3, self.numberAppleRect)
            if self.numberAppleRect.topleft[0] <= mousePos[0] <= self.numberAppleRect.bottomright[0] and \
                    self.numberAppleRect.topleft[1] <= mousePos[1] <= self.numberAppleRect.bottomright[
                1] and not self.numberApplePressed:
                surface.blit(self.numberApple5Bad, self.numberAppleRect)
                if getMouseButtonUp():
                    self.currentNumberApple = 5
                    self.numberApplePressed = True
        elif self.currentNumberApple == 5 :
            surface.blit(self.numberApple5, self.numberAppleRect)
            if self.numberAppleRect.topleft[0] <= mousePos[0] <= self.numberAppleRect.bottomright[0] and \
                    self.numberAppleRect.topleft[1] <= mousePos[1] <= self.numberAppleRect.bottomright[
                1] and not self.numberApplePressed:
                surface.blit(self.numberApple1Bad, self.numberAppleRect)
                if getMouseButtonUp():
                    self.currentNumberApple = 1
                    self.numberApplePressed = True
        else:
            raise Exception(f"oppsie doopsie neki se je zjebal, v nameScreen.py, okoli vrstice 168 v matchcase stavku\n Unexpected value, expected 1, 3 or 5, instead got {self.currentNumberApple} ")

        if self.numberAppleRect.topleft[0] > mousePos[0] or mousePos[0] > self.numberAppleRect.bottomright[0] or \
                self.numberAppleRect.topleft[1] > mousePos[1] or mousePos[1] > self.numberAppleRect.bottomright[1]:
            self.numberApplePressed = False

        if self.pacifist:

            if self.pacifistRect.topleft[0] <= mousePos[0] <= self.pacifistRect.bottomright[0] and self.pacifistRect.topleft[1] <= mousePos[1] <= self.pacifistRect.bottomright[1] and not self.pacifistPressed:
                surface.blit(self.pacifistOff, self.pacifistRect)
                if getMouseButtonUp():
                    self.pacifist = False
                    self.pacifistPressed = True
            else:
                surface.blit(self.pacifistOn, self.pacifistRect)
        else:
            if self.pacifistRect.topleft[0] <= mousePos[0] <= self.pacifistRect.bottomright[0] and \
                    self.pacifistRect.topleft[1] <= mousePos[1] <= self.pacifistRect.bottomright[
                1] and not self.pacifistPressed:
                surface.blit(self.pacifistOn, self.pacifistRect)
                if getMouseButtonUp():
                    self.pacifist = True
                    self.pacifistPressed = False
            else:
                surface.blit(self.pacifistOff, self.pacifistRect)

        if self.pacifistRect.topleft[0] > mousePos[0] or mousePos[0] > self.pacifistRect.bottomright[0] or \
                self.pacifistRect.topleft[1] > mousePos[1] or mousePos[1] > self.pacifistRect.bottomright[1]:
            self.pacifistPressed = False

    def submit(self):
        if len(self.name) < 1:
            username = "anon"
        else:
            username = "".join(self.name)
        changeUsername(username)
        self.name.clear()
        setBadApples(self.badAppleOn)
        changeState(2)
        setNumberOfApples(self.currentNumberApple)
        setPacifist(self.pacifist)
