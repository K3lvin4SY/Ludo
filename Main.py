import pygame
from game import *
from colors import colors
from gui import *

pygame.init()

#https://www.petercollingridge.co.uk/tutorials/pygame-physics-simulation/creating-pygame-window/

#Största källan till min kod nedan:
#https://www.youtube.com/watch?v=OydU03jMXQo


#https://www.youtube.com/watch?v=aqhp_-CbE_w
class Screen():
    """The class for each screen.
    """
    def __init__(self, title, width=1280, height=720, fill=colors["Secondary"]) -> None:
        """creates the new screen by aplying some values

        Args:
            title (string): the window title
            width (int, optional): the width of the screen. Defaults to 1280.
            height (int, optional): the height od the screen. Defaults to 720.
            fill (tuple, optional): bg color of screen. Defaults to colors["Secondary"].
        """
        
        self.properties = Properties(width, height)

        self.title = title
        self.width = self.properties.width
        self.height = self.properties.height
        self.fill = fill
        self.enabled = False
    
    def enable(self):
        """enables the screen by changing the window title and changing self variables
        """
        pygame.display.set_caption(self.title) # updates window title
        self.enabled = True # turns to enabled
        self.screen = pygame.display.set_mode((self.width, self.height)) # updates width and height
        self.screen.fill(self.fill) # upddates bg

    def disable(self):
        """disable screen
        """
        self.enabled = False
    
    def checkState(self):
        """to check the status of a screen (enabled or disavbled)

        Returns:
            bool: true if screen is enabled
        """
        return self.enabled

    def update(self):
        """
        If the button is not enabled, fill the screen
        """
        if not self.enabled:
            self.screen.fill(self.fill)
        
    def getTitle(self):
        """
        This function returns the screen name
        :return: The screen
        """
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
        endScreen = Screen("End Screen")
        buildOptScreen = Screen("Map Builder Options")
        buildScreen = Screen("Map Builder")

        self.screens = {
            "main":startScreen,
            "sgo":sGameOptionsScreen,
            "mgo":mGameOptionsScreen,
            "gs":gameScreen,
            "es":endScreen,
            "bso":buildOptScreen,
            "bs":buildScreen
        }

        self.screensFunc = {
            "main":self.main,
            "sgo":self.singleGameOptScn,
            "mgo":self.multiGameOptScn,
            "gs":self.gameScn,
            "es":self.endScn,
            "bso":self.buildOptScn,
            "bs":self.buildScn
        }

        startScreen.enable()

        self.main(startScreen.getTitle())


        while self.running:
            
            


            for event in pygame.event.get():
                self.update(event)
                if event.type == pygame.QUIT:
                    self.running = False
    
    def main(self, scn):
        """
        It creates buttons that when clicked, changes the screen to other screens.
        
        :param scn: The screen to draw the textboxes on
        """
        
        self.display = "main"
        self.titleTB = self.addTextBox(TextBox(self.properties, 500, 70, centerX=True, y=100, text='Ludo', color=colors["Primary2"]))
        self.titleTB.draw(scn)
        self.singlePlayerBtn = self.addTextBox(TextBox(self.properties, 230, 60, centerX=True, centerY=True, y=0, text='Singleplayer', color=colors["DarkGrey"], hoverColor=colors["White"], command=lambda x="sgo": self.changeScreen(x)))
        self.singlePlayerBtn.draw(scn, outline=colors["Primary1"], size=40)
        self.multiPlayerBtn = self.addTextBox(TextBox(self.properties, 230, 60, centerX=True, centerY=True, y=100, text='Multiplayer', color=colors["DarkGrey"], hoverColor=colors["White"], command=lambda x="mgo": self.changeScreen(x)))
        
        self.multiPlayerBtn.draw(scn, outline=colors["Primary1"], size=40)

        # Quit Btn
        self.backBtn = self.addTextBox(TextBox(self.properties, 150, 60, color=colors["Primary1"], centerX=False, centerY=False, y="max-20", x=20, text='Quit', command=lambda: self.quitGame()))
        self.backBtn.draw(scn)

        # Builder Btn
        self.backBtn = self.addTextBox(TextBox(self.properties, 200, 60, color=colors["Primary1"], centerX=False, centerY=False, y="max-20", x="max-20", text='Builder', command=lambda x="bso": self.changeScreen(x)))
        self.backBtn.draw(scn)

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
        self.botsSelect = self.addTextBox(Selection(self.properties, ["2", "3", "4"], True, True, title="Players:"))
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
        """
        It creates a new instance of the GamePlatform class, and other buttons
        
        :param scn: The scene to draw the grid on
        """
       
        self.grid = self.addTextBox(GamePlatform(self.properties, self.display, self.participants, self))
        self.display = "gs"
        self.grid.draw(scn, self.display)
        # Quit Btn
        self.backBtn = self.addTextBox(TextBox(self.properties, 150, 60, color=colors["Primary1"], centerX=False, centerY=False, y="max-20", x=20, text='Quit', command=lambda x="main": self.changeScreen(x)))
        self.backBtn.draw(scn)
    
    def endScn(self, scn):
        self.display = "es"

        self.backBtn = self.addTextBox(TextBox(self.properties, 500, 60, color=colors["Primary1"], centerX=True, centerY=True, y=0, x=0, text=self.winner + ' has won the game!'))
        self.backBtn.draw(scn)

        # Back Btn
        self.backBtn = self.addTextBox(TextBox(self.properties, 250, 60, color=colors["Primary1"], centerX=False, centerY=False, y="max-20", x=20, text='Back', command=lambda x="main": self.changeScreen(x)))
        self.backBtn.draw(scn)

    def buildOptScn(self, scn):
        self.display = "bso"
        # Title
        self.titleTB = self.addTextBox(TextBox(self.properties, 500, 70, centerX=True, y=100, text='Builder Options - Comming Later', color=colors["Primary2"]))
        self.titleTB.draw(scn)

        # grid size selection
        self.gridsize = self.addTextBox(Selection(self.properties, "4", True, True, title="Players:", numMode=True, y=80))
        self.gridsize.draw(scn, 40)

        # grid size selection
        self.players = self.addTextBox(Selection(self.properties, "11", True, True, title="Grid Size:", numMode=True, y=-80))
        self.players.draw(scn, 40)

        # Start Btn
        self.backBtn = self.addTextBox(TextBox(self.properties, 150, 60, color=colors["Primary1"], centerX=True, centerY=False, y="max-20", x=0, text='Start'))
        self.backBtn.draw(scn)

        # Back Btn
        self.backBtn = self.addTextBox(TextBox(self.properties, 150, 60, color=colors["Primary1"], centerX=False, centerY=False, y="max-20", x=20, text='Back', command=lambda x="main": self.changeScreen(x)))
        self.backBtn.draw(scn)



    def buildScn(self, scn):
        self.display = "bs"

    def changeScreen(self, to):
        """method for changing screens by enabaling the new and disableing the old

        Args:
            to (string): gets the string code of a screen.
        """
        if to != self.display: # if screen code id not current
            if to != "gs":
                self.participants = 0
            self.items = {} # Clear items from last Screen
            self.screens[to].enable() # enable requested screen
            self.screens[self.display].disable() # disable current
            self.screensFunc[to](self.screens[to].getTitle()) # activate new screen
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
    def quitGame(self):
        self.running = False
    
    def update(self, event): # method that gets called aas quicly as possible (main loop)
        
        
        pos = pygame.mouse.get_pos()

        # update items here
        pygame.display.flip()
        self.screens[self.display].update()
        
        if event.type == pygame.MOUSEMOTION:
            
            hovers = []
            for it in self.items:
                if self.items[it][0] == self.display and self.items[it][1] == "textbox":
                    hover = it.isOver(pos)
                elif self.items[it][0] == self.display and self.items[it][1] == "select":
                    hover = it.isOver(pos)
                elif self.items[it][0] == self.display and self.items[it][1] == "platform":
                    hover = it.isOver(pos)
                hovers.append(hover)
            if not True in hovers: # fixes the problem when a just clikced button moves and pointer is locked to hand until hover on another button. (true if mouse is over no buttons at all)
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        if event.type == pygame.MOUSEBUTTONDOWN:
            for it in self.items:
                itemDisplay = self.items[it][0]
                itemType = self.items[it][1]
                if itemDisplay == self.display and itemType == "textbox":
                    if it.isOver(pos) == True:
                        if it.command != None:
                            it.command()
                            break
                elif itemDisplay == self.display and itemType == "select":
                    if it.isOver(pos) == True:
                        if not it.numMode:
                            self.participants = it.getOver(pos).command()
                            break
                        else:
                            it.getOver(pos).command()
                            break
                elif itemDisplay == self.display and itemType == "platform":
                    if it.isOver(pos) == True:
                        if isinstance(it.getOver(pos), Dice):
                            it.getOver(pos).dice.command()
                        else:
                            it.getOver(pos).pawn.command()
                        break
        

    def addTextBox(self, tb):
        """adds the textbox to a dictionary

        Args:
            tb (TextBox, Selection or GamePlatform): the object created

        Returns:
            TextBox: returns the given object
        """
        if isinstance(tb, Selection):
            self.items[tb] = [self.display, "select"]
        elif isinstance(tb, GamePlatform):
            self.items[tb] = ["gs", "platform"]
        else:
            self.items[tb] = [self.display, "textbox"]
        return tb

    def startGame(self):
        if self.participants == 0:
            return
        print("Starting Game along with " + str(self.participants) + " participants!")
        if self.display == "sgo":
            self.participants += 1
        self.changeScreen("gs")
        pass

    def setWinner(self, playerColor):
        self.winner = playerColor
        self.changeScreen("es")



class Properties():
    def __init__(self, width, height) -> None:
        self.width =width
        self.height =height


game = WindowSystem()