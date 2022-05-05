from codeop import CommandCompiler
from turtle import width
import pygame
import sys

from setuptools import Command

pygame.init()

#https://www.petercollingridge.co.uk/tutorials/pygame-physics-simulation/creating-pygame-window/
def test():
    print("lol")

colors = {"White":(255, 255, 255), "Black":(0, 0, 0), "Red":(255, 0, 0), "Green":(0, 255, 0), "Blue":(0, 0, 255), "bg":(195, 200, 219), "Secondary":(36, 42, 56), "DarkGrey":(78, 89, 111), "Primary1":(245, 75, 100), "Primary2":(250, 134, 98)}

class Screen():
    def __init__(self, title, width=1280, height=720, fill=colors["Secondary"]) -> None:
        
        self.properties = Properties(width, height)

        self.title = title
        self.width = self.properties.width
        self.height = self.properties.height
        self.fill = fill
        self.enabled = False
    
    def enable(self):
        pygame.display.set_caption(self.title)
        self.enabled = True
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill(self.fill)

    def disable(self):
        self.enabled = False
    
    def checkState(self):
        return self.enabled

    def update(self):
        if not self.enabled:
            self.screen.fill(self.fill)
        
    def getTitle(self):
        return self.screen

class WindowSystem:

    def __init__(self) -> None:

        self.items = {}
        self.properties = Properties(1280, 720)

        #self.mainScreen = pygame.display.set_mode((self.properties.width, self.properties.height))

        #pygame.display.flip()
        self.running = True

        #pygame.draw.rect(self.mainScreen, (195, 200, 219), pygame.Rect(0, 0, self.properties.width, self.properties.height))
        #pygame.draw.rect(self.mainScreen, (255,255,0), pygame.Rect(30, 30, 60, 60))
        startScreen = Screen("Start Screen")
        sGameOptionsScreen = Screen("Singleplayer Game Options")
        mGameOptionsScreen = Screen("Multiplayer Game Options")
        gameScreen = Screen("Game")

        self.screens = {
            "main":startScreen,
            "sgo":sGameOptionsScreen,
            "mgo":mGameOptionsScreen,
            "gs":gameScreen
        }

        self.screensFunc = {
            "main":self.main,
            "sgo":self.singleGameOptScn,
            "mgo":self.multiGameOptScn,
            "gs":self.gameScn
        }

        startScreen.enable()

        self.main(startScreen.getTitle())


        while self.running:
            
            


            for event in pygame.event.get():
                self.update(event)
                if event.type == pygame.QUIT:
                    self.running = False
    
    def main(self, scn):
        
        self.display = "main"
        self.singlePlayerBtn = self.addTextBox(TextBox(self.properties, 500, 70, centerX=True, y=100, text='Ludo', color=colors["Primary2"]))
        self.singlePlayerBtn.draw(scn)
        self.singlePlayerBtn = self.addTextBox(TextBox(self.properties, 230, 60, centerX=True, centerY=True, y=0, text='Singleplayer', color=colors["DarkGrey"], hoverColor=colors["White"], command=lambda x="sgo": self.changeScreen(x)))
        self.singlePlayerBtn.draw(scn, outline=colors["Primary1"], size=40)
        self.multiPlayerBtn = self.addTextBox(TextBox(self.properties, 230, 60, centerX=True, centerY=True, y=100, text='Multiplayer', color=colors["DarkGrey"], hoverColor=colors["White"], command=lambda x="mgo": self.changeScreen(x)))
        
        self.multiPlayerBtn.draw(scn, outline=colors["Primary1"], size=40)

    def multiGameOptScn(self, scn):
        self.display = "mgo"
        self.singlePlayerBtn = self.addTextBox(TextBox(self.properties, 100, 150, centerX=True, centerY=True, y=100, text='Ping!', command=lambda x="main": self.changeScreen(x)))
        self.singlePlayerBtn.draw(scn)

    def singleGameOptScn(self, scn):
        self.display = "sgo"
        self.singlePlayerBtn = self.addTextBox(TextBox(self.properties, 100, 150, centerX=True, centerY=True, y=-100, text='Pong!', command=lambda x="main": self.changeScreen(x)))
        self.singlePlayerBtn.draw(scn)
    
    def gameScn(self, scn):
        self.display = "gs"

    def changeScreen(self, to):
        """method for changing screens by enabaling the new and disableing the old

        Args:
            to (string): gets the string code of a screen.
        """
        if to != self.display: # if screen code id not current
            self.screens[to].enable() # enable requested screen
            self.screens[self.display].disable() # disable current
            self.screensFunc[to](self.screens[to].getTitle()) # activate new screen
    
    def update(self, event): # method that gets called aas quicly as possible (main loop)
        
        
        pos = pygame.mouse.get_pos()

        # update items here
        pygame.display.flip()
        self.screens[self.display].update()
        
        if event.type == pygame.MOUSEMOTION:
            
            for it in self.items:
                if self.items[it][0] == self.display and self.items[it][1] == "textbox":
                    it.isOver(pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            for it in self.items:
                if self.items[it][0] == self.display:
                    if it.isOver(pos) == True:
                        if it.command != None:
                            it.command()
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                            break

        pass
        

    def addTextBox(self, tb):
        """adds the textbox to a dictionary

        Args:
            tb (TextBox): the textBox created

        Returns:
            TextBox: returns the given textbox
        """
        self.items[tb] = [self.display, "textbox"]
        return tb

class Pawn:
    def __init__(self, color) -> None:
        self.color = color
        pass

#https://www.youtube.com/watch?v=4_9twnEduFA&ab_channel=TechWithTim
class TextBox():
    """Class for creating a textbox. Can be used a a button, text info or a simple block
    """
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

        self.hover = False
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

    def draw(self, display, outline=None, size=60):
        #Call this method to draw the button on the screen
        self.display = display
        self.outline = outline
        self.size = size
        if outline:
            pygame.draw.rect(display, outline, (self.x-2,self.y-2,self.width+4,self.height+4), 0, border_radius=9)
            
        pygame.draw.rect(display, self.color, (self.x,self.y,self.width,self.height), 0, border_radius=8)
        
        if self.text != '':
            font = pygame.font.SysFont('marvel', size)
            text = font.render(self.text, 1, (0,0,0))
            display.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

        

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                if self.hover == False:
                    self.color = self.hoverColor
                    self.draw(self.display, self.outline, self.size)
                    if self.command != None:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    self.hover = True
                return True
        if self.hover == True:
            self.color = self.originalColor
            self.draw(self.display, self.outline, self.size)
            if self.command != None:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            self.hover = False
        return False

class Properties():
    def __init__(self, width, height) -> None:
        self.width =width
        self.height =height


game = WindowSystem()