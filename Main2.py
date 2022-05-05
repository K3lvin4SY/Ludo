from codeop import CommandCompiler
import pygame
from colors import colors
from gui import *
import json

pygame.init()

#https://www.petercollingridge.co.uk/tutorials/pygame-physics-simulation/creating-pygame-window/
def test():
    print("lol")



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
        self.titleTB = self.addTextBox(TextBox(self.properties, 500, 70, centerX=True, y=100, text='Ludo', color=colors["Primary2"]))
        self.titleTB.draw(scn)
        self.singlePlayerBtn = self.addTextBox(TextBox(self.properties, 230, 60, centerX=True, centerY=True, y=0, text='Singleplayer', color=colors["DarkGrey"], hoverColor=colors["White"], command=lambda x="sgo": self.changeScreen(x)))
        self.singlePlayerBtn.draw(scn, outline=colors["Primary1"], size=40)
        self.multiPlayerBtn = self.addTextBox(TextBox(self.properties, 230, 60, centerX=True, centerY=True, y=100, text='Multiplayer', color=colors["DarkGrey"], hoverColor=colors["White"], command=lambda x="mgo": self.changeScreen(x)))
        
        self.multiPlayerBtn.draw(scn, outline=colors["Primary1"], size=40)

    def multiGameOptScn(self, scn):
        """GUI for multiplayer options

        Args:
            scn (Screen): the linked screen to this gui layout
        """
        self.display = "mgo"
        # Title
        self.titleTB = self.addTextBox(TextBox(self.properties, 500, 70, centerX=True, y=100, text='Multiplayer Options', color=colors["Primary2"]))
        self.titleTB.draw(scn)

        # Player selection
        self.botsSelect = self.addTextBox(Selection(self.properties, ["1", "2", "3", "4"], True, True, title="Players:"))
        self.botsSelect.draw(scn, 40)

        # Start Btn
        self.backBtn = self.addTextBox(TextBox(self.properties, 150, 60, color=colors["Primary1"], centerX=True, centerY=False, y="max-20", x=0, text='Start', command=lambda: self.startGame()))
        self.backBtn.draw(scn)

        # Back Btn
        self.backBtn = self.addTextBox(TextBox(self.properties, 150, 60, color=colors["Primary1"], centerX=False, centerY=False, y="max-20", x=20, text='Back', command=lambda x="main": self.changeScreen(x)))
        self.backBtn.draw(scn)

    def singleGameOptScn(self, scn):
        """GUI for singleplayer options

        Args:
            scn (Screen): the linked screen to this gui layout
        """
        self.display = "sgo"
        # Title
        self.titleTB = self.addTextBox(TextBox(self.properties, 500, 70, centerX=True, y=100, text='Singleplayer Options', color=colors["Primary2"]))
        self.titleTB.draw(scn)

        # Player selection
        self.botsSelect = self.addTextBox(Selection(self.properties, ["1", "2", "3"], True, True, title="Bots:"))
        self.botsSelect.draw(scn, 40)

        # Start Btn
        self.backBtn = self.addTextBox(TextBox(self.properties, 150, 60, color=colors["Primary1"], centerX=True, centerY=False, y="max-20", x=0, text='Start', command=lambda: self.startGame()))
        self.backBtn.draw(scn)

        # Back Btn
        self.backBtn = self.addTextBox(TextBox(self.properties, 150, 60, color=colors["Primary1"], centerX=False, centerY=False, y="max-20", x=20, text='Back', command=lambda x="main": self.changeScreen(x)))
        self.backBtn.draw(scn)
    
    def gameScn(self, scn):
        self.display = "gs"
        # Back Btn
        self.backBtn = self.addTextBox(TextBox(self.properties, 150, 60, color=colors["Primary1"], centerX=False, centerY=False, y="max-20", x=20, text='Back', command=lambda x="main": self.changeScreen(x)))
        self.backBtn.draw(scn)

    def changeScreen(self, to):
        """method for changing screens by enabaling the new and disableing the old

        Args:
            to (string): gets the string code of a screen.
        """
        if to != self.display: # if screen code id not current
            if to != self.screens["gs"]:
                self.participants = 0
            self.items = {} # Clear items from last Screen
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
                elif self.items[it][0] == self.display and self.items[it][1] == "select":
                    it.isOver(pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            for it in self.items:
                if self.items[it][0] == self.display and self.items[it][1] == "textbox":
                    if it.isOver(pos) == True:
                        if it.command != None:
                            it.command()
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                            break
                elif self.items[it][0] == self.display and self.items[it][1] == "select":
                    if it.isOver(pos) == True:
                        self.participants = it.getOver(pos).command()
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
        if isinstance(tb, Selection):
            self.items[tb] = [self.display, "select"]
        else:
            self.items[tb] = [self.display, "textbox"]
        return tb

    def startGame(self):
        if self.participants == 0:
            return
        print("Starting Game along with " + str(self.participants) + " participants!")
        self.changeScreen("gs")
        pass

class GamePlatform:
    def __init__(self, mode, participants, size) -> None:
        self.mode = mode
        self.participants = participants
        playerColors = ["Red", "Orange", "Yellow", "Green"]
        self.players = {}
        if self.mode == "mgo":
            for i in range(self.participants):
                self.players[playerColors[i]] = Player(playerColors[i])
        elif self.mode == "sgo":
            self.players[playerColors[0]] = Player(playerColors[0])
            for i in range(self.participants):
                self.players[playerColors[i+1]] = Player(playerColors[i+1], bot=True)

        
    
    def draw(self, display, size):
        pass

class Player():
    def __init__(self, color, bot=False) -> None:
        self.color = color
        self.bot = bot
        self.pawns = []
        for i in range(4):
            self.pawns.append(Pawn(self, self.color))
        pass

class Pawn(Player):
    def __init__(self, parent, color) -> None:
        super().__init__(self, parent)
        self.color = color
        pass


class Properties():
    def __init__(self, width, height) -> None:
        self.width =width
        self.height =height


game = WindowSystem()