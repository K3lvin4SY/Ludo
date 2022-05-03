from codeop import CommandCompiler
from turtle import width
import pygame
import sys

from setuptools import Command

pygame.init()

#https://www.petercollingridge.co.uk/tutorials/pygame-physics-simulation/creating-pygame-window/
def test():
    print("lol")
class WindowHandler:

    def __init__(self) -> None:

        self.properties = Properties(1280, 720)

        self.items = {}

        self.mainScreen = pygame.display.set_mode((self.properties.width, self.properties.height))

        pygame.display.flip()
        self.running = True

        pygame.draw.rect(self.mainScreen, (195, 200, 219), pygame.Rect(0, 0, self.properties.width, self.properties.height))
        pygame.draw.rect(self.mainScreen, (255,255,0), pygame.Rect(30, 30, 60, 60))

        self.main()
        


        while self.running:
            
            for event in pygame.event.get():
                self.update(event)
                if event.type == pygame.QUIT:
                    self.running = False
    
    def main(self):
        
        self.win = "main"
        self.singlePlayerBtn = self.addTextBox(TextBox(self.properties, 100, 50, centerX=True, centerY=True, y=-100, text='Tesadwawdwdawt'))
        self.singlePlayerBtn.draw(self.mainScreen)
        self.multiPlayerBtn = self.addTextBox(TextBox(self.properties, 100, 50, centerX=True, centerY=True, y=100, text='Test', color=(255,0,255)))
        
        self.multiPlayerBtn.draw(self.mainScreen, outline=(0,0,255))

    def changeScreen(self, start, end):
        pass # Change screen by looping throu items
    
    def update(self, event):
        pygame.display.flip()
        pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEMOTION:
            for it in self.items:
                if self.items[it][0] == self.win and self.items[it][1] == "textbox":
                    it.isOver(pos)
                    print("d")
        if event.type == pygame.MOUSEBUTTONDOWN:
            for it in self.items:
                if self.items[it][0] == self.win:
                    if it.isOver(pos) == True:
                        if it.command != None:
                            it.command()
        pass

    def addTextBox(self, tb):
        self.items[tb] = [self.win, "textbox"]
        return tb

class Pawn:
    def __init__(self, color) -> None:
        self.color = color
        pass

#https://www.youtube.com/watch?v=4_9twnEduFA&ab_channel=TechWithTim
class TextBox():
    def __init__(self, properties, width, height, centerX=False, centerY=False, x=0 , y=0, color=(255,255,0), text='', hoverColor=None, command=None):
        if centerX == True:
            self.x = int((properties.width - width) / 2)
            self.x += x
        else:
            self.x = x
        if centerY == True:
            self.y = int((properties.height - height) / 2)
            self.y += y
        else:
            self.y = y

        self.color = color
        self.originalColor = color
        if hoverColor != None:
            self.hoverColor = hoverColor
        else:
            self.hoverColor = color
        self.width = width
        self.height = height
        self.text = text
        if command != None:
            self.command = lambda: command()
        else:
            self.command = None

    def draw(self,win,outline=None, size=60):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4), 0, border_radius=8)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height), 0, border_radius=8)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', size)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

        

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:

                self.color = self.hoverColor
                return True
        self.color = self.originalColor
        return False

class Properties():
    def __init__(self, width, height) -> None:
        self.width =width
        self.height =height


game = WindowHandler()