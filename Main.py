import random
import pygame
from colors import colors
from gui import *
import json

pygame.init()

#https://www.petercollingridge.co.uk/tutorials/pygame-physics-simulation/creating-pygame-window/


#https://www.youtube.com/watch?v=aqhp_-CbE_w
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
       
        self.grid = self.addTextBox(GamePlatform(self.properties, self.display, self.participants))
        self.display = "gs"
        self.grid.draw(scn, self.display)
        # Back Btn
        self.backBtn = self.addTextBox(TextBox(self.properties, 150, 60, color=colors["Primary1"], centerX=False, centerY=False, y="max-20", x=20, text='Back', command=lambda x="main": self.changeScreen(x)))
        self.backBtn.draw(scn)

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
                elif self.items[it][0] == self.display and self.items[it][1] == "platform":
                    it.isOver(pos)
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
                        self.participants = it.getOver(pos).command()
                        break
                elif itemDisplay == self.display and itemType == "platform":
                    if it.isOver(pos) == True:
                        if isinstance(it.getOver(pos), Dice):
                            it.getOver(pos).dice.command()
                        else:
                            it.getOver(pos).pawn.command()
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

class GamePlatform:
    def __init__(self, properties, mode, participants, centerX=True, centerY=True) -> None:
        self.mode = mode
        self.properties = properties
        self.participants = participants
        self.centerX = centerX
        self.centerY = centerY
        self.playerColors = ["Red", "Orange", "Yellow", "Green"]
        self.players = {}
        self.tiles = {}
        self.endTiles = {}
        self.bases = {}
        if self.mode == "mgo":
            for i in range(self.participants):
                self.players[self.playerColors[i]] = Player(self.playerColors[i], self)
        elif self.mode == "sgo":
            self.players[self.playerColors[0]] = Player(self.playerColors[0], self)
            for i in range(self.participants-1):
                self.players[self.playerColors[i+1]] = Player(self.playerColors[i+1], self, bot=True)
        with open('map.json') as file:
            self.mapData = json.load(file)
        self.turn = self.players[self.playerColors[0]]
        self.rolled = False

        
    
    def draw(self, scn, display):
        self.gridSize = self.mapData["dimentions"]
        self.display = display
        self.scn = scn
        
        def getCoords(cor, gridSize=self.gridSize):
            """converts grid cordinates to screen cordinates

            Args:
                cor (int): x or y grid cordinates
                gridSize (int, optional): the size of the grid. Defaults to self.gridSize.

            Returns:
                int: the converted cordinate x or y
            """
            y= int(((cor-1))/(gridSize-1)*(self.properties.height-gridSize*8) - (self.properties.height-gridSize*8)/2)
            return y
        tbSize = int(self.properties.height/self.gridSize)-5
        
        # adds the public road
        for gridData in self.mapData["map"]:
            x = getCoords(self.mapData["map"][gridData][0])
            y = getCoords(self.mapData["map"][gridData][1])*-1
            gridNum = gridData.split("-")[0]
            gridType = gridData.split("-")[1]
            for i in range(self.mapData["participants"]):
                i += 1
                if gridType[-1] == str(i) and i <= self.participants:
                    color = colors[self.playerColors[i-1]]
                    break
                else:
                    color = colors["DarkGrey"]
            tile = Tile(self.properties, tbSize, tbSize, self.centerX, self.centerY, x, y, color, gridData)
            tileInfo = tile.draw(scn)
            self.tiles[tileInfo[0]] = tileInfo[1]

        # adds private roads  
        for gridData in self.mapData["map-end"]:
            x = getCoords(self.mapData["map-end"][gridData][0])
            y = getCoords(self.mapData["map-end"][gridData][1])*-1
            gridType = gridData.split("-")[1]
            if gridType[-1] == "S" or int(gridType[-1]) <= self.participants:
                for i in range(self.mapData["participants"]):
                    i += 1
                    if gridType[-1] == str(i):
                        color = colors[self.playerColors[i-1]]
                        break
                    else:
                        color = colors["White"]
                tile = Tile(self.properties, tbSize, tbSize, self.centerX, self.centerY, x, y, color, gridData)
                tileInfo = tile.draw(scn)
                self.endTiles[tileInfo[0]] = tileInfo[1]

        # adds the home bases
        for gridData in self.mapData["map-base"]:
            x = getCoords(self.mapData["map-base"][gridData][0])
            y = getCoords(self.mapData["map-base"][gridData][1])*-1
            gridType = gridData
            for i in range(self.mapData["participants"]):
                i += 1
                if gridType[-1] == str(i):
                    if (i <= self.participants):
                        color = colors[self.playerColors[i-1]]
                        break
                    else:
                        color = colors["Secondary"]
                        break
                else:
                    color = colors["White"]
            if color != colors["Secondary"]:
                tile = Tile(self.properties, tbSize*2, tbSize*2, self.centerX, self.centerY, x, y, color, gridData)
                tileInfo = tile.draw(scn)
                self.bases[tileInfo[0]] = tileInfo[1]
        
        # set pawn home
        baseNum = 0
        for player in self.players.values():
            baseNum += 1
            player.givePawnsInfo(self.bases["b"+str(baseNum)], scn, self.properties)

        # set dice
        self.dice = Dice(self, self.properties, tbSize, tbSize, self.centerX, self.centerY)
        self.dice.draw(self.scn)

        # Player Display
        self.playerDisplay = PlayerDisplay(self.properties, tbSize, tbSize, colors[list(self.players)[0]], x=20, y=20, text=list(self.players)[0] + ", Roll the Dice")
        self.playerDisplay.draw(self.scn, 40)

    def isOver(self, pos):
        for player in self.players.values():
            for pawn in player.pawns:
                if pawn.isOver(pos):
                    return True
        if self.dice.isOver(pos):
            return True
        return False

    def getOver(self, pos):
        for player in self.players.values():
            for pawn in player.pawns:
                if pawn.isOver(pos):
                    return pawn
        if self.dice.isOver(pos):
            return self.dice
        return None
    
    def nextPlayer(self, dice):
        self.rolled = False
        index = self.players.values().index(self.turn)
        if dice == 1:
            self.playerDisplay.changeText(self.players.keys()[index] + ", Roll the Dice Again")
            return self.turn
        try:
            self.turn = self.players.values()[index+1]
            self.playerDisplay.changeColor(colors[self.players.keys()[index+1]])
            self.playerDisplay.changeText(self.players.keys()[index+1] + ", Roll the Dice")
        except:
            self.turn = self.players.values()[0]
            self.playerDisplay.changeColor(colors[self.players.keys()[0]])
            self.playerDisplay.changeText(self.players.keys()[0] + ", Roll the Dice")
        return self.turn
    
    def diceRoll(self, value):
        self.rolled = True
        if len(self.turn.home.pawn) == 4:
            self.playerDisplay.changeText(self.turn.color + ", Pick a Pawn")
            return
        

class PlayerDisplay:
    def __init__(self, properties, width, height, color=colors["Red"], centerX=False, centerY=False, x=0 , y=0, text='', textColor=colors["White"]) -> None:
        self.properties = properties
        self.width = width
        self.height = height
        self.centerX = centerX
        self.centerY = centerY
        self.x = x
        self.y = y
        self.color = color
        self.text = text
        self.textColor = textColor
        self.turnMonitor = TextBox(self.properties, self.width, self.height, self.centerX, self.centerY, self.x, self.y, self.color)
        self.turnMessage = TextBox(self.properties, self.width*4, self.height*1, self.centerX, self.centerY, self.x, int(self.y+self.width*1.5), colors["Secondary"], self.text, textColor=self.textColor)
    
    def draw(self, scn, size):
        self.size = size
        self.turnMonitor.draw(scn)
        self.turnMessage.draw(scn, size=self.size)

    def changeColor(self, color):
        self.color = color
        self.turnMonitor.changeColor(color)
    
    def changeText(self, text):
        self.text = text
        self.turnMessage.changeText(text)

class Tile:
    def __init__(self, properties, width, height, centerX=False, centerY=False, x=0 , y=0, color=(255,255,0), gridData="") -> None:
        self.properties = properties
        self.width = width
        self.height = height
        self.centerX = centerX
        self.centerY = centerY
        self.x = x
        self.y = y
        self.color = color
        self.pawn = None
        self.gridData = gridData
        if not gridData[0].lower() == "b":
            self.gridNum = int(gridData.split("-")[0])
            self.gridType = gridData.split("-")[1]
        else:
            self.gridNum = 0
            self.gridType = gridData
        self.tile = TextBox(self.properties, self.width, self.height, self.centerX, self.centerY, self.x, self.y, self.color)
    
    def draw(self, display):
        self.tile.draw(display)
        return [self.gridType, self]
    
    def addPawn(self, pawn):
        if not self.gridData[0].lower() == "b":
            if self.pawn != None:
                self.pawn.sendHome()
            self.pawn = pawn
        else:
            if self.pawn == None:
                self.pawn = []
            self.pawn.append(pawn)
        
    def getPawnHomeCordinates(self, pawn):
        offsetCoords = {0:(-30, -30), 1:(-30, 30), 2:(30, -30), 3:(30, 30)}
        index = self.pawn.index(pawn)
        x = self.x + offsetCoords[index][0]
        y = self.y + offsetCoords[index][1]
        return x, y
        
    def getPawnCordinates(self):
        x = self.x
        y = self.y
        return x, y

    
    def removePawn(self, pawn=None):
        if not self.gridData[0].lower() == "b":
            self.pawn = None
        else:
            if pawn in self.pawn:
                del self.pawn[pawn]

class Player():
    def __init__(self, color, platform, bot=False) -> None:
        self.color = color
        self.bot = bot
        self.pawns = []
        for i in range(4):
            self.pawns.append(Pawn(self.color, platform, self))
        pass
    def givePawnsInfo(self, home, display, properties):
        self.home = home
        for pawn in self.pawns:
            pawn.setHome(home)
            pawn.draw(display, properties)

class Pawn():
    def __init__(self, color, platform, player) -> None:
        self.color = color
        self.platform = platform
        self.player = player
        pass

    def draw(self, display, properties):
        self.properties = properties
        self.pawn = TextBox(properties, 30, 30, True, True, self.x, self.y, colors[self.color], command=lambda: self.clicked())
        self.pawn.draw(display, colors["White"])

    def setHome(self, home):
        self.home = home
        home.addPawn(self)
        (self.x, self.y) = home.getPawnHomeCordinates(self)
        (self.ox, self.oy) = (self.x, self.y)

    def sendHome(self):
        (self.x, self.y) = (self.ox, self.oy) # maybe move this 1 line down?
        self.home.addPawn(self)

    def isOver(self, pos):
        return self.pawn.isOver(pos)

    def clicked(self):
        if self.platform.turn == self.player: # players turn
            if self.platform.rolled == True: # player has rolled dice
                # move pawn
                self.movePawn(self.home.gridNum, self.platform.dice.value)
                pass
    
    def movePawn(self, prevLocation, diceValue):
        for i in range(diceValue):
            if self.platform.tiles[prevLocation].gridType[-1] == self.platform.playerColors.index(self.color)+1: # if tile standing on is players entry or exit
                self.platform.tiles[prevLocation+1]


class Dice:
    def __init__(self, platform, properties, width, height, centerX=True, centerY=True, x=0 , y=0, color=colors["White"]) -> None:
        self.properties = properties
        self.width = width
        self.height = height
        self.centerX = centerX
        self.centerY = centerY
        self.x = x
        self.y = y
        self.color = color
        self.value = 6
        self.platform = platform
        self.dice = TextBox(self.properties, self.width, self.height, centerX, centerY, self.x, self.y, self.color, str(self.value), command=lambda: self.roll())
    
    def draw(self, display):
        self.dice.draw(display)
    
    def roll(self):
        if self.platform.rolled == False:
            self.value = random.randint(1, 6)
            self.dice.changeText(str(self.value))
            self.platform.diceRoll(self.value)

    def isOver(self, pos):
        return self.dice.isOver(pos)

class Properties():
    def __init__(self, width, height) -> None:
        self.width =width
        self.height =height


game = WindowSystem()