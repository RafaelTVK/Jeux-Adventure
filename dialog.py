import pygame
from AppConfig import *

class DialogBox:
    X_POSITION = 60
    Y_POSITION = 470 
    
    def __init__(self) -> None:
        self.box = pygame.image.load("dialogs/dialog_box.png")
        self.box = pygame.transform.scale(self.box, TAILLE_DIALOGBOX)
        self.texts = []
        self.textIndex = 0
        self.letterIndex = 0
        self.font = pygame.font.Font(FONT, POLICE)
        self.reading = False

    def execute(self, dialog=[]):
        if self.reading:
            self.nextText()
        else:
            self.reading = True
            self.textIndex = 0
            self.texts = dialog
    
    def render(self, screen):
        if self.reading:
            self.letterIndex += 1

            if self.letterIndex >= len(self.texts[self.textIndex]):
                self.letterIndex = self.letterIndex
            screen.blit(self.box, (self.X_POSITION,self.Y_POSITION))
            text = self.font.render(self.texts[self.textIndex][0:self.letterIndex], False, NOIR)
            screen.blit(text, (self.X_POSITION + 60, self.Y_POSITION + 30) )
    
    def nextText(self):
        self.textIndex += 1
        self.letterIndex = 0
        if self.textIndex >= len(self.texts):
            # close dialog
            self.reading = False