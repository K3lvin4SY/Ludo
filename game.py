from colors import colors
from myRange import myRange
import random
import json
from gui import *

class GamePlatform:
    def __init__(self, properties, bots, participants, system, selectedMap, centerX=True, centerY=True) -> None:
        """
        It creates a class called Game.
        
        :param properties: A list of the properties in the game
        :param mode: The mode of the game
        :param participants: The number of players in the game
        :param system: The system that the game is being played on
        :param centerX: Whether or not the game should be centered horizontally, defaults to True
        (optional)
        :param centerY: If the game should be centered on the Y axis, defaults to True (optional)
        """
        self.properties = properties
        self.participants = participants
        self.bots = bots
        self.centerX = centerX
        self.centerY = centerY
        self.players = {}
        self.tiles = {}
        self.endTiles = {}
        self.bases = {}
        self.system = system
        self.selectedMap = selectedMap
        with open('maps/'+self.selectedMap+'.json') as file:
            self.mapData = json.load(file)
        self.playerColors = self.mapData["colors"]
        # Creating a player object for each player in the game.
        for i in range(self.participants):
            i += 1
            if self.participants-i < self.bots:
                self.players[self.playerColors[i-1]] = Player(self.playerColors[i-1], self, bot=True)
            else:
                self.players[self.playerColors[i-1]] = Player(self.playerColors[i-1], self, bot=False)
        '''
        if self.mode == "mgo":
            for i in range(self.participants):
                self.players[self.playerColors[i]] = Player(self.playerColors[i], self)
        elif self.mode == "sgo":
            self.players[self.playerColors[0]] = Player(self.playerColors[0], self, bot=False)
            for i in range(self.participants-1):
                self.players[self.playerColors[i+1]] = Player(self.playerColors[i+1], self, bot=True)
        '''

        self.turn = self.players[self.playerColors[0]]
        self.rolled = False

        
    
    def draw(self, scn, display):
        """
        It draws the board.
        
        :param scn: the scene
        :param display: the display object
        """
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
            # Calculating the y-coordinate of the grid.
            y= int(((cor-1))/(gridSize-1)*(self.properties.height-gridSize*8) - (self.properties.height-gridSize*8)/2)
            return y
        tbSize = int((self.properties.height/self.gridSize)*0.93)
        
        # adds the public road
        # Creating a tile object for each tile on the board.
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
        dicex = getCoords(self.mapData["dice"][0])
        dicey = getCoords(self.mapData["dice"][1])*-1
        self.dice = Dice(self, self.properties, tbSize, tbSize, self.centerX, self.centerY, dicex, dicey)
        self.dice.draw(self.scn)

        # Player Display
        self.playerDisplay = PlayerDisplay(self.properties, tbSize, tbSize, colors[list(self.players)[0]], x=20, y=20, text=list(self.players)[0] + ", Roll the Dice")
        self.playerDisplay.draw(self.scn, int(tbSize*0.58))

        #self.nextPlayer(2)

    def isOver(self, pos):
        """
        It checks if the mouse is over a pawn or the dice.
        
        :param pos: The position of the mouse
        :return: a boolean value.
        """
        for player in self.players.values():
            for pawn in player.pawns:
                if pawn.isOver(pos):
                    return True
        if self.dice.isOver(pos):
            return True
        return False

    def getOver(self, pos):
        """
        It returns the pawn that is over the position pos, or the dice if the dice is over the position
        pos, or None if nothing is over the position pos
        
        :param pos: The position of the mouse
        :return: the pawn that is over the position.
        """
        for player in self.players.values():
            for pawn in player.pawns:
                if pawn.isOver(pos):
                    return pawn
        if self.dice.isOver(pos):
            return self.dice
        return None

    def getEndTiles(self, playerColor):
        """
        It takes a player color and returns a dictionary of the end tiles that are dedicated to that
        player
        
        :param playerColor: the color of the player
        :return: A dictionary of the end tiles for the player.
        """
        playerNum = self.playerColors.index(playerColor)+1
        tempDict = {}
        for endTile in self.endTiles:
            if endTile[-1] == str(playerNum) or endTile[-1].lower() == "s": # if tile is player dedicated tile (tileplayer number equals player number)
                tempDict[int(endTile.split("-")[0])] = self.endTiles[endTile]
        return tempDict

    def nextPlayer(self, dice):
        """
        It takes the current player, checks if they have won, if not, it checks if they rolled a 6, if
        not, it sets the next player as the current player. It also sends a new message
        
        :param dice: the number that was rolled
        :return: The next player in the game.
        """
        # Checking if the player has won the game.
        index = list(self.players.values()).index(self.turn)
        if len(self.turn.pawnsOut) == 4:
            # self.turn won the game
            self.system.setWinner(list(self.players.keys())[index])
            return
        self.rolled = False

        # Checking if the dice is 6, if it is, it will return the turn. If it is not, it will try to
        # change the turn to the next player. If it cannot, it will change the turn to the first
        # player.
        if dice == 6:
            self.playerDisplay.changeText(list(self.players.keys())[index] + ", Roll the Dice Again")
            if self.turn.bot == True:
                #self.playerDisplay.changeText("Click to continue")
                # wait for confirmation
                #pygame.time.wait(200)
                self.dice.roll()
            return self.turn

        try:
            self.turn = list(self.players.values())[index+1]
            self.playerDisplay.changeColor(colors[list(self.players.keys())[index+1]])
            self.playerDisplay.changeText(list(self.players.keys())[index+1] + ", Roll the Dice")
        except:
            self.turn = list(self.players.values())[0]
            self.playerDisplay.changeColor(colors[list(self.players.keys())[0]])
            self.playerDisplay.changeText(list(self.players.keys())[0] + ", Roll the Dice")
        
        if self.turn.bot == True:
            #self.playerDisplay.changeText("Click to continue")
            # wait for confirmation
            #pygame.time.wait(200)
            self.dice.roll()
            #return

        return self.turn
    
    def diceRoll(self, value):
        """
        If the player has 4 pawns out, and they roll a 1 or 6, they can pick a pawn. Otherwise, they
        can't.
        
        :param value: the value of the dice roll
        :return: the value of the dice roll.
        """
        self.rolled = True

        if len(self.turn.home.pawn) +  len(self.turn.pawnsOut) == 4:
            if value == 1 or value == 6:
                self.playerDisplay.changeText(self.turn.color + ", Pick a Pawn")
            else:
                self.nextPlayer(value)
            if self.turn.bot == False:
                return
        elif len(self.turn.home.pawn) + len(self.turn.pawnsOut) == 3:
            if value == 1 or value == 6:
                self.playerDisplay.changeText(self.turn.color + ", Pick a Pawn")
            else:
                self.playerDisplay.changeText(self.turn.color + ", Click the Pawn")
        else:
            self.playerDisplay.changeText(self.turn.color + ", Pick a Pawn")
        if self.turn.bot == True:
            self.turn.autoPlay(value)
        
class PlayerDisplay:
    def __init__(self, properties, width, height, color=colors["Red"], centerX=False, centerY=False, x=0 , y=0, text='', textColor=colors["White"]) -> None:
        """
        This function creates a textbox object that can be used to display text on the screen
        
        :param properties: The properties of the window
        :param width: The width of the box
        :param height: The height of the box
        :param color: The color of the box
        :param centerX: If True, the x coordinate will be the center of the object. If False, the x
        coordinate will be the top left corner of the object, defaults to False (optional)
        :param centerY: If True, the y coordinate will be the center of the box. If False, the y
        coordinate will be the top of the box, defaults to False (optional)
        :param x: The x coordinate of the top left corner of the box, defaults to 0 (optional)
        :param y: The y coordinate of the top left corner of the box, defaults to 0 (optional)
        :param text: The text that will be displayed
        :param textColor: The color of the text
        """
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
        self.turnMessage = TextBox(self.properties, self.width*8, self.height*1, self.centerX, self.centerY, self.x-int(self.width*0.4), int(self.y+self.width*2.75), colors["Secondary"], self.text, textColor=self.textColor, textbgSize=True)
    
    def draw(self, scn, size):
        """
        draws the playercolor box and the message text
        
        :param scn: the scene to draw on
        :param size: the size of the text
        """
        self.size = size
        self.turnMonitor.draw(scn)
        self.turnMessage.draw(scn, size=self.size)

    def changeColor(self, color):
        """
        The function changeColor() takes in a color and changes the color of the playercolorbox to that color
        
        :param color: The color of the player
        """
        self.color = color
        self.turnMonitor.changeColor(color)
    
    def changeText(self, text):
        """
        It changes the text of the turnMessage object to the text that is passed in.
        
        :param text: The text to be displayed
        """
        self.text = text
        self.turnMessage.changeText(text)

class Tile:
    def __init__(self, properties, width, height, centerX=False, centerY=False, x=0 , y=0, color=(255,255,0), gridData="") -> None:
        """
        Assigns the riht values to the right valueables
        
        :param properties: window dimetions
        :param width: The width of the tile
        :param height: The height of the tile
        :param centerX: If True, the tile will be centered on the x axis. If False, the x value will
        be the top left corner of the tile, defaults to False (optional)
        :param centerY: If True, the tile will be centered on the y axis, defaults to False (optional)
        :param x: The x position of the tile, defaults to 0 (optional)
        :param y: The y coordinate of the tile, defaults to 0 (optional)
        :param color: The color of the tile
        :param gridData: This is the data
        """
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
        """
        It draws the tile and returns the gridType, gridData, or gridNum depending on the first letter
        of gridType.
        
        :param display: The display that the grid is being drawn on
        :return: The gridType, gridData, or gridNum.
        """
        self.display = display
        self.tile.draw(display)
        if self.gridType[0].lower() =="b":
            return [self.gridType, self]
        elif self.gridType[0].lower() =="s":
            return [self.gridData, self]
        else:
            return [self.gridNum, self]
    
    def addPawn(self, pawn):
        """
        If the gridData[0] is not "b", then the pawn is set to the pawn. 
        If the gridData[0] is "b", then the pawn is set to an empty list (if pawn == None). later adds pawn to pawn list
        
        :param pawn: The pawn object that is being added to the grid
        """
        if not self.gridData[0].lower() == "b":
            if self.pawn != None:
                self.pawn.sendHome()
            self.pawn = pawn
        else:
            if self.pawn == None:
                self.pawn = []
            self.pawn.append(pawn)
        
    def getPawnHomeCordinates(self, pawn):
        """
        It returns the coordinates of the home position of a pawn on a tile
        
        :param pawn: The pawn that you want to get the home coordinates of
        :return: The x and y coordinates of the pawn's home position.
        """
        offsetCoords = {0:(-1*self.width*0.2, -1*self.width*0.2), 1:(-1*self.width*0.2, self.width*0.2), 2:(self.width*0.2, -1*self.width*0.2), 3:(self.width*0.2, self.width*0.2)}
        index = self.pawn.index(pawn)
        x = self.x + int(offsetCoords[index][0])
        y = self.y + int(offsetCoords[index][1])
        return x, y
        
    def getPawnCordinates(self):
        """
        It returns the x and y coordinates of the pawn
        :return: The x and y coordinates of the pawn.
        """
        x = self.x
        y = self.y
        return x, y

    
    def removePawn(self, pawn=None):
        """
        If the gridData[0] is not equal to "b", then set the pawn to None. Otherwise, if the pawn is in
        the pawn list, then remove the pawn from the list.
        
        :param pawn: The pawn to be removed
        """
        if not self.gridData[0].lower() == "b":
            self.pawn = None
        else:
            if pawn in self.pawn:
                self.pawn.remove(pawn)
        self.update()

    def update(self):
        """
        It draws the tile and then updates the pawns.
        """
        self.tile.draw(self.display)
        if self.gridType[0].lower() == "b":
            for pawn in self.pawn:
                pawn.update()

# The Player class is used to create a player object, which has a color, pawns, and pawnsOut
class Player():
    def __init__(self, color, platform, bot=False) -> None:
        """
        It creates a player object with a color, a platform, and a bot boolean.
        
        :param color: The color of the player
        :param platform: The platform that the pawns are on
        :param bot: If the player is a bot or not, defaults to False (optional)
        """
        self.color = color
        self.bot = bot
        self.pawns = []
        self.pawnsOut = []
        for i in range(4):
            self.pawns.append(Pawn(self.color, platform, self))

    def givePawnsInfo(self, home, display, properties):
        """
        It sets the home of each pawn to the home of the player, and then draws each pawn
        
        :param home: the home position of the pawns
        :param display: The pygame display
        :param properties: a dictionary containing the following keys:
        """
        self.home = home
        for pawn in self.pawns:
            pawn.setHome(home)
            pawn.draw(display, properties)
    
    def takeOutPawn(self, pawn):
        """
        It takes a pawn and adds it to the list of pawns that are out of the game
        
        :param pawn: The pawn that is being taken out of the game
        """
        self.pawnsOut.append(pawn)

    def autoPlay(self, diceValue):
        """
        It chooses a pawn to move based on the dice value and the current state of the board.
        
        :param diceValue: The value of the dice
        :return: nothing.
        """
        if self.bot == True:
            targets = {
                "bad-end":[],
                "out":[],
                "good-end":[],
                "end":[],
                "normal":[],
                "destroy":[],
                "suicide":[],
                "home":[],
                "home-destroy":[]
            }
            if len(self.home.pawn) == 4:
                if diceValue in [1, 6]:
                    self.home.pawn[0].movePawn(self.home.pawn[0].tile.gridNum, diceValue, getTile=False)
                return

            for pawn in self.pawns:
                if pawn not in self.home.pawn:
                    if pawn not in self.pawnsOut:
                        tile1 = pawn.movePawn(pawn.tile.gridNum, diceValue, getTile=True)
                        if tile1 == "out":
                            targets["out"].append(pawn)
                            continue
                        if tile1.pawn == None:
                            if pawn.tile.gridType[0].lower() == "s" and tile1.gridType[0].lower() != "s":
                                targets["bad-end"].append(pawn)
                            if pawn.tile.gridType[0].lower() != "s" and tile1.gridType[0].lower() == "s":
                                targets["good-end"].append(pawn)
                            if pawn.tile.gridType[0].lower() == "s" and tile1.gridType[0].lower() == "s":
                                targets["end"].append(pawn)
                            if pawn.tile.gridType[0].lower() != "s" and tile1.gridType[0].lower() != "s":
                                targets["normal"].append(pawn)
                        elif tile1.pawn not in self.pawns:
                            targets["destroy"].append(pawn)
                        else:
                            targets["suicide"].append(pawn)
                        
                else:
                    if diceValue in [1, 6]:
                        tile1 = pawn.movePawn(pawn.tile.gridNum, diceValue, getTile=True)
                        if tile1.pawn == None:
                            targets["home"].append(pawn)
                        elif tile1.pawn not in self.pawns:
                            targets["home-destroy"].append(pawn)
            
            # Choosing a pawn to move.
            pawnToMove = None
            if targets["home-destroy"]: # take out opponent by takeing out a pawn from home
                pawnToMove = random.choice(targets["home-destroy"])
            elif targets["destroy"]: # take out an opponent the normal way
                pawnToMove = random.choice(targets["destroy"])
            elif targets["out"]: # takeing a pawn to the goal
                pawnToMove = random.choice(targets["out"])
            elif targets["home"]: # takeing a pawn out from home (if not entry ocupied)
                pawnToMove = random.choice(targets["home"])
            elif targets["good-end"]: # entering the end roads (private roads)
                pawnToMove = random.choice(targets["good-end"])
            elif targets["normal"]: # normal jump
                pawnToMove = random.choice(targets["normal"])
            elif targets["end"]: # useless move on private roads
                pawnToMove = random.choice(targets["end"])
            elif targets["bad-end"]: # going out of the priovate roads to the public
                pawnToMove = random.choice(targets["bad-end"])
            elif targets["suicide"]: # killing your own =(
                pawnToMove = random.choice(targets["suicide"])
            else:
                print("WARN: Unfinished Path!")

            pawnToMove.movePawn(pawnToMove.tile.gridNum, diceValue, getTile=False)
    
    def disableFirstTurn(self):
        self.firstTurn = False


class Pawn():
    def __init__(self, color, platform, player) -> None:
        """
        This function is a constructor for the class Ball. It takes in three parameters: color,
        platform, and player. It sets the color, platform, and player attributes to the parameters
        passed in. It also sets the out attribute to False
        
        :param color: The color of the platform
        :param platform: The platform that the player is on
        :param player: The player object
        """
        self.color = color
        self.platform = platform
        self.player = player
        self.out = False
        pass

    def draw(self, display, properties):
        """
        It draws a textbox with a color and a command.
        
        :param display: The display to draw the pawn on
        :param properties: A dictionary of properties that are used to draw the textbox
        """
        self.properties = properties
        self.display = display
        self.pawn = TextBox(properties, int((self.properties.height/self.platform.gridSize)*0.4), int((self.properties.height/self.platform.gridSize)*0.4), True, True, self.x, self.y, colors[self.color], command=lambda: self.clicked())
        self.pawn.draw(self.display, colors["White"])
        self.pawnBg = TextBox(properties, int((self.properties.height/self.platform.gridSize)*0.6), int((self.properties.height/self.platform.gridSize)*0.6), True, True, self.x, self.y, colors["Secondary"])

    def setHome(self, home):
        """
        It sets the home of the pawn to the home parameter, adds the pawn to the home, sets the tile of
        the pawn to the home, sets the x and y coordinates of the pawn to the home's pawn home
        coordinates, and sets the original x and y coordinates of the pawn to the x and y coordinates of
        the pawn.
        
        :param home: the home tile of the pawn
        """
        self.home = home
        home.addPawn(self)
        self.tile = home
        (self.x, self.y) = home.getPawnHomeCordinates(self)
        (self.ox, self.oy) = (self.x, self.y)

    def sendHome(self):
        """
        It moves a pawn to its home tile.
        """
        
        self.home.addPawn(self)
        self.tile = self.home
        (self.x, self.y) = (self.ox, self.oy) # maybe move this 1 line down?
        self.home.update()

    def isOver(self, pos):
        """
        If the pawn is not out, then return whether the pawn is over the position.
        
        :param pos: The position of the mouse
        :return: The isOver function is being returned.
        """
        if self.out == False:
            return self.pawn.isOver(pos)

    def clicked(self):
        """
        If it's the player's turn, and the player has rolled the dice, and the player is on the home
        tile, and the dice value is not 6 or 1, then return.
        :return: The return value of the last statement in the function.
        """
        if self.platform.turn == self.player: # players turn
            if self.platform.rolled == True: # player has rolled dice
                if self.tile == self.home and (self.platform.dice.value not in [6, 1]):
                    return
                # move pawn
                self.movePawn(self.tile.gridNum, self.platform.dice.value)
                pass
    
    def logicalMove(self, tile):
        """
        It moves the pawn from one tile to another
        
        :param tile: The tile that the pawn is moving to
        :return: the value of the last line of the function.
        """
        #return
        if not isinstance(self.logicalTile.pawn, list):
            try: self.lastTile
            except AttributeError: self.lastTile = None
            if self.lastTile is None:
                self.lastTile = self.tile
            tileWasOut = False
            if tile == 'out':
                tLi = []
                tileWasOut = True
                for t in self.platform.endTiles:
                    tLi.append(int(t.split("-")[0]))
                tile = self.platform.endTiles[str(max(tLi))+"-S"]
            if str(self.lastTile.x) + ", " + str(self.lastTile.y) == str(tile.x) + ", " + str(tile.y):
                return
            #print(str(self.lastTile.x) + ", " + str(self.lastTile.y))
            #print(str(tile.x) + ", " + str(tile.y))
            
            if self.lastTile.x == tile.x:
                range = myRange(self.lastTile.y, tile.y)
                for y in range:
                    self.x = tile.x
                    self.y = y
                    self.pawnBg.draw(self.display)

                    self.lastTile.update()
                    if self.lastTile.pawn != None:
                        if self.lastTile.pawn != self:
                            self.lastTile.pawn.update()
                    
                    self.logicalTile.update()
                    if self.logicalTile.pawn != None:
                        if self.logicalTile.pawn != self:
                            self.logicalTile.pawn.update()
                    self.draw(self.display, self.properties)
                    self.logicalTile = tile
                    pygame.display.flip()
                    pygame.time.wait(int(200*(1/(len(range)))))
            elif self.lastTile.y == tile.y:
                range = myRange(self.lastTile.x, tile.x)
                for x in range:
                    self.x = x
                    self.y = tile.y
                    self.pawnBg.draw(self.display)

                    self.lastTile.update()
                    if self.lastTile.pawn != None:
                        if self.lastTile.pawn != self:
                            self.lastTile.pawn.update()
                    
                    self.logicalTile.update()
                    if self.logicalTile.pawn != None:
                        if self.logicalTile.pawn != self:
                            self.logicalTile.pawn.update()
                    self.draw(self.display, self.properties)
                    self.logicalTile = tile
                    pygame.display.flip()
                    pygame.time.wait(int(200*(1/(len(range)))))
            elif abs(self.lastTile.y-tile.y) == abs(self.lastTile.x-tile.x):
                if tileWasOut:
                    return
                #https://stackoverflow.com/questions/16552508/python-loops-for-simultaneous-operation-two-or-possibly-more
                def conv(num):
                    for x in num:
                        yield x
                    return num
                rangex = conv(myRange(self.lastTile.x, tile.x))
                rangey = conv(myRange(self.lastTile.y, tile.y))
                for x, y in zip(rangex, rangey):
                    self.x = x
                    self.y = y
                    self.pawnBg.draw(self.display)

                    self.lastTile.update()
                    if self.lastTile.pawn != None:
                        if self.lastTile.pawn != self:
                            self.lastTile.pawn.update()
                    
                    self.logicalTile.update()
                    if self.logicalTile.pawn != None:
                        if self.logicalTile.pawn != self:
                            self.logicalTile.pawn.update()
                    self.draw(self.display, self.properties)
                    self.logicalTile = tile
                    pygame.display.flip()
                    pygame.time.wait(int(200*(1/(len(myRange(self.lastTile.x, tile.x))))))
            if self.lastTile is not tile:
                self.lastTile = tile

    def movePawn(self, prevLocation, diceValue, getTile = False):
        """
        It moves the pawn to the next tile based on the dicevalue.
        
        :param prevLocation: the grid number of the tile the pawn is currently on
        :param diceValue: the value of the dice
        """
        location = prevLocation
        self.logicalTile = self.tile
        stepsLeft = 0
        playerNum = self.platform.playerColors.index(self.color)+1 # gets the player num (id) ex: red = 1, orange = 2, green = 4
        # Checking if the tile is a s or not. If it is not a s, it will check if the tile is
        # the player's entry or exit. If it is the player's entry or exit, it will check if it is the
        # exit. If it is the exit, it will break the loop. If it is not the exit, it will continue the
        # loop. If the tile is not the player's entry or exit, it will continue the loop. If the
        # location is over the maximum tile, it will set the location to 1.
        if not self.tile.gridType[0].lower() == "s":
            for i in range(diceValue):
                if location != 0:
                    if self.platform.tiles[location].gridType[-1] == str(playerNum): # if tile standing on is players entry or exit
                        if self.platform.tiles[location].gridType[0].lower() == "x": # if it is exit
                            if getTile == False:
                                self.logicalMove(self.platform.tiles[location])
                            stepsLeft = diceValue - i
                            break
                else:
                    for tile in self.platform.tiles.values():
                        if tile.gridType.lower() == "e"+str(playerNum):
                            location = tile.gridNum
                            if getTile == False:
                                self.logicalMove(self.platform.tiles[location])
                            break
                    break
                if getTile == False:
                    self.logicalMove(self.platform.tiles[location])
                location += 1
                if location == max(list(self.platform.tiles.keys()))+1: # if location is over the maximum tile
                    location = 1
        else:
            stepsLeft = diceValue
        # Moving the pawn to the new location. (code used when moving on public road)
        if stepsLeft == 0:
            if getTile:
                return self.platform.tiles[location]
            self.placePawn(self.platform.tiles[location])
        else:
            
            endTiles = self.platform.getEndTiles(self.color)
            for til in self.platform.tiles:
                    if self.platform.tiles[til].gridType.lower() == "x"+str(playerNum):
                        gridNum = til
            endLocation = gridNum - location
            
            if self.tile.gridType[0].lower() == "s":
                loc = location
            else:
                loc = endLocation
            def getRange():
                if self.tile.gridType[0].lower() == "s":
                    return range(location, location + stepsLeft)
                else:
                    return range(endLocation, endLocation + stepsLeft)
            # Moving pawn on private roads
            for i in getRange():
                i += 1
                
                endLocation = i
                if endLocation == list(endTiles)[-1]:
                    if i == stepsLeft + loc:
                        # pawn out of game
                        if getTile:
                            return "out"
                        self.placePawn("out")
                        self.platform.nextPlayer(diceValue)
                        return
                if endLocation >= list(endTiles)[-1]:
                    endLocation = (list(endTiles)[-2]*2)-endLocation
                if getTile == False:
                    if endLocation <= 0:
                        for til in self.platform.tiles:
                            if self.platform.tiles[til].gridType.lower() == "x"+str(playerNum):
                                logicalLoc = til - (endLocation*-1)
                        if logicalLoc <= 0:
                            logicalLoc = max(list(self.platform.tiles.keys())) + logicalLoc
                        self.logicalMove(self.platform.tiles[logicalLoc])
                    else:
                        logicalLoc = endLocation
                        self.logicalMove(endTiles[logicalLoc])
            # Moving the pawn to the end location.
            if endLocation <= 0:
                for til in self.platform.tiles:
                    if self.platform.tiles[til].gridType.lower() == "x"+str(playerNum):
                        endLocation = til - (endLocation*-1)
                if endLocation <= 0:
                    endLocation = max(list(self.platform.tiles.keys())) + endLocation
                if getTile:
                    return self.platform.tiles[endLocation]
                self.placePawn(self.platform.tiles[endLocation])
            # Moving the pawn to the end tile.
            else:
                if getTile:
                    return endTiles[endLocation]
                self.placePawn(endTiles[endLocation])

        if getTile:
            return None
        self.platform.nextPlayer(diceValue)
        self.logicalTile = None

    def placePawn(self, newTile):
        """
        It takes a pawn and moves it to a new tile
        
        :param newTile: The tile that the pawn is being placed on
        """
        self.logicalMove(newTile)
        if newTile == "out":
            self.player.takeOutPawn(self)
            self.tile.removePawn(self)
            self.tile.update()
            self.out = True
            self.logicalTile.update()
            if self.logicalTile.pawn != None:
                if self.logicalTile.pawn != self:
                    self.logicalTile.pawn.update()
            self.logicalTile = None
        else:
            newTile.addPawn(self)
            self.tile.removePawn(self)
            self.tile.update()
            self.tile = newTile
            self.x = newTile.x
            self.y = newTile.y
            self.logicalTile.update()
            if self.logicalTile.pawn != None:
                if self.logicalTile.pawn != self:
                    if not isinstance(self.logicalTile.pawn, list):
                        self.logicalTile.pawn.update()
            self.draw(self.display, self.properties)
            self.logicalTile = None
    
    def update(self):
        """
        It takes the display and properties of the object and draws it to the screen
        """
        self.draw(self.display, self.properties)


# It's a class that creates a dice object that can be rolled
class Dice:
    def __init__(self, platform, properties, width, height, centerX=True, centerY=True, x=0 , y=0, color=colors["White"]) -> None:
        """
        This function creates a TextBox object that has a width, height, centerX, centerY, x, y, color,
        value, platform, and dice
        
        :param platform: The platform that the dice is on
        :param properties: The properties of the window
        :param width: The width of the dice
        :param height: The height of the dice
        :param centerX: If True, the x value will be the center of the box. If False, the x value will
        be the left side of the box, defaults to True (optional)
        :param centerY: If True, the textbox will be centered vertically, defaults to True (optional)
        :param x: The x position of the dice, defaults to 0 (optional)
        :param y: The y coordinate of the dice, defaults to 0 (optional)
        :param color: The color of the dice
        """
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
        """
        It draws the dice on the display.
        
        :param display: The display to draw the dice on
        """
        self.dice.draw(display, size=int(self.width))
    
    def roll(self):
        """
        If the platform hasn't been rolled, then roll the dice and change the text to the value of the
        dice.
        """
        if self.platform.rolled == False:
            for i in range(8):
                i += 1
                pygame.time.wait(int(50*(1.2**i)))
                self.value = random.randint(1, 6)
                self.dice.changeText(str(self.value))

                pygame.display.flip()
            pygame.time.wait(800)
            self.platform.diceRoll(self.value)

    def isOver(self, pos):
        """
        It checks if the dice is over the position.
        
        :param pos: The position of the mouse
        :return: The dice.isOver(pos) method is being returned.
        """
        return self.dice.isOver(pos)