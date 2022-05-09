from colors import colors
import random
import json
from gui import *

class GamePlatform:
    def __init__(self, properties, mode, participants, system, centerX=True, centerY=True) -> None:
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
        self.mode = mode
        self.properties = properties
        self.participants = participants
        self.centerX = centerX
        self.centerY = centerY
        self.players = {}
        self.tiles = {}
        self.endTiles = {}
        self.bases = {}
        self.system = system
        with open('map.json') as file:
            self.mapData = json.load(file)
        self.playerColors = self.mapData["colors"]
        # Creating a player object for each player in the game.
        if self.mode == "mgo":
            for i in range(self.participants):
                self.players[self.playerColors[i]] = Player(self.playerColors[i], self)
        elif self.mode == "sgo":
            self.players[self.playerColors[0]] = Player(self.playerColors[0], self)
            for i in range(self.participants-1):
                self.players[self.playerColors[i+1]] = Player(self.playerColors[i+1], self, bot=True)
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
        tbSize = int(self.properties.height/self.gridSize)-5
        
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
        self.dice = Dice(self, self.properties, tbSize, tbSize, self.centerX, self.centerY)
        self.dice.draw(self.scn)

        # Player Display
        self.playerDisplay = PlayerDisplay(self.properties, tbSize, tbSize, colors[list(self.players)[0]], x=20, y=20, text=list(self.players)[0] + ", Roll the Dice")
        self.playerDisplay.draw(self.scn, 40)

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
            return self.turn
        try:
            self.turn = list(self.players.values())[index+1]
            self.playerDisplay.changeColor(colors[list(self.players.keys())[index+1]])
            self.playerDisplay.changeText(list(self.players.keys())[index+1] + ", Roll the Dice")
        except:
            self.turn = list(self.players.values())[0]
            self.playerDisplay.changeColor(colors[list(self.players.keys())[0]])
            self.playerDisplay.changeText(list(self.players.keys())[0] + ", Roll the Dice")
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
            return
        elif len(self.turn.home.pawn) + len(self.turn.pawnsOut) == 3:
            if value == 1 or value == 6:
                self.playerDisplay.changeText(self.turn.color + ", Pick a Pawn")
            else:
                self.playerDisplay.changeText(self.turn.color + ", Click the Pawn")
        else:
            self.playerDisplay.changeText(self.turn.color + ", Pick a Pawn")
        
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
        self.turnMessage = TextBox(self.properties, self.width*8, self.height*1, self.centerX, self.centerY, self.x-int(self.width/1), int(self.y+self.width*2.75), colors["Secondary"], self.text, textColor=self.textColor)
    
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
        offsetCoords = {0:(-30, -30), 1:(-30, 30), 2:(30, -30), 3:(30, 30)}
        index = self.pawn.index(pawn)
        x = self.x + offsetCoords[index][0]
        y = self.y + offsetCoords[index][1]
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
        self.pawnsOut.append(pawn)

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
        self.pawn = TextBox(properties, 30, 30, True, True, self.x, self.y, colors[self.color], command=lambda: self.clicked())
        self.pawn.draw(display, colors["White"])

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
    
    def movePawn(self, prevLocation, diceValue):
        """
        It moves the pawn to the next tile based on the dicevalue.
        
        :param prevLocation: the grid number of the tile the pawn is currently on
        :param diceValue: the value of the dice
        :return: the range of the steps left.
        """
        location = prevLocation
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
                            stepsLeft = diceValue - i
                            break
                else:
                    for tile in self.platform.tiles.values():
                        if tile.gridType.lower() == "e"+str(playerNum):
                            location = tile.gridNum
                            break
                    break
                location += 1
                if location == list(self.platform.tiles.keys())[-1]+1: # if location is over the maximum tile
                    location = 1
        else:
            stepsLeft = diceValue
        # Moving the pawn to the new location. (code used when moving on public road)
        if stepsLeft == 0:
            self.platform.tiles[location].addPawn(self)
            self.tile.removePawn(self)
            self.tile.update()
            self.tile = self.platform.tiles[location]
            self.x = self.platform.tiles[location].x
            self.y = self.platform.tiles[location].y
            self.draw(self.display, self.properties)
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
                        self.player.takeOutPawn(self)
                        self.tile.removePawn(self)
                        self.tile.update()
                        self.out = True
                        self.platform.nextPlayer(diceValue)
                        return
                if endLocation >= list(endTiles)[-1]:
                    endLocation = (list(endTiles)[-2]*2)-endLocation
            # Moving the pawn to the end location.
            if endLocation <= 0:
                for til in self.platform.tiles:
                    if self.platform.tiles[til].gridType.lower() == "x"+str(playerNum):
                        endLocation = til - (endLocation*-1)
                self.platform.tiles[endLocation].addPawn(self)
                self.tile.removePawn(self)
                self.tile.update()
                self.tile = self.platform.tiles[endLocation]
                self.x = self.platform.tiles[endLocation].x
                self.y = self.platform.tiles[endLocation].y
                self.draw(self.display, self.properties)
            # Moving the pawn to the end tile.
            else:
                endTiles[endLocation].addPawn(self)
                self.tile.removePawn(self)
                self.tile.update()
                self.tile = endTiles[endLocation]
                self.x = endTiles[endLocation].x
                self.y = endTiles[endLocation].y
                self.draw(self.display, self.properties)

        self.platform.nextPlayer(diceValue)
    
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
        self.dice.draw(display)
    
    def roll(self):
        """
        If the platform hasn't been rolled, then roll the dice and change the text to the value of the
        dice.
        """
        if self.platform.rolled == False:
            self.value = random.randint(1, 6)
            self.dice.changeText(str(self.value))
            self.platform.diceRoll(self.value)

    def isOver(self, pos):
        """
        It checks if the dice is over the position.
        
        :param pos: The position of the mouse
        :return: The dice.isOver(pos) method is being returned.
        """
        return self.dice.isOver(pos)