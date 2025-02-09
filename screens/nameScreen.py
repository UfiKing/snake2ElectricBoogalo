import pygame
from constants import cellSize, cellNumber
from functions import *

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

        self.apple = pygame.image.load("graphics/jabloko16.bad.png")
        self.apple = pygame.transform.scale(self.apple, (cellSize * 2, cellSize * 2))
        self.appleRect = self.apple.get_rect()
        self.appleRect.left = self.inputRect.left
        self.appleRect.bottom = self.inputRect.top - (cellSize * 4)

        self.appleSelectRect = pygame.Rect(self.appleRect.left, self.appleRect.bottom + cellSize, self.appleRect.width, self.appleRect.height)

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

        surface.blit(self.apple, self.appleRect)
        pygame.draw.rect(surface, "#AF65FA", self.appleSelectRect)

    def submit(self):
        if len(self.name) < 1:
            username = "anon"
        else:
            username = "".join(self.name)
        changeUsername(username)
        self.name.clear()
        changeState(2)
