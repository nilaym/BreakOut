import pygame
from pygame.locals import *

class Text(pygame.sprite.DirtySprite):
    def __init__(self, message, pos, font_size = 32, font_color = (0,0,0), highlight_color = (14, 124, 129), font_family = "Arial"):
        pygame.sprite.DirtySprite.__init__(self)
        self.font_size = font_size
        self.color = font_color
        self.original_color = font_color
        self.highlight_color = highlight_color
        self.font = pygame.font.SysFont(font_family, self.font_size)
        self.message = message

        self.image = self.font.render(self.message, 1, self.color)
        self.rect = self.image.get_rect(topleft = pos)


    def update(self):
        mousepos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousepos):
            if self.color == self.original_color:
                self.changeColor(self.highlight_color)
                
        else:
            if self.color == self.highlight_color:
                self.changeColor(self.original_color)
                
    def changeMessage(self, newMessage):
        self.image = self.font.render(newMessage, 1, self.color)
        self.message=newMessage
        self.dirty = 1

    def changeColor(self, newColor):
        self.color = newColor
        self.image = self.font.render(self.message, 1, self.color)
        self.dirty = 1

           
