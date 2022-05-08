from colors import colors
import random
import json
from gui import *

class GamePlatform:
    def __init__(self, properties, mode, participants, centerX=True, centerY=True) -> None:
        self.mode = mode
        self.properties = properties
        self.participants = participants
        self.centerX = centerX
        self.centerY = centerY
        self.players = {}
        self.tiles = {}
        self.endTiles = {}
        self.bases = {}
        with open('map.json') as file:
            self.mapData = json.load(file)
        self.playerColors = self.mapData["colors"]
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

    def getEndTiles(self, playerColor):
        playerNum = self.playerColors.index(playerColor)+1
        tempDict = {}
        for endTile in self.endTiles:
            if endTile[-1] == str(playerNum) or endTile[-1].lower() == "s": # if tile is player dedicated tile (tileplayer number equals player number)
                tempDict[int(endTile.split("-")[0])] = self.endTiles[endTile]
        return tempDict

    def nextPlayer(self, dice):
        self.rolled = False
        index = list(self.players.values()).index(self.turn)
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
        self.rolled = True
        if len(self.turn.home.pawn) +  len(self.turn.pawnsOut) == 4:
            if value == 1 or value == 6:
                self.playerDisplay.changeText(self.turn.color + ", Pick a Pawn")
            else:
                self.nextPlayer(value)
            return
        elif len(self.turn.home.pawn) == 3 and len(self.turn.pawnsOut) < 1:
            if value == 1 or value == 6:
                self.playerDisplay.changeText(self.turn.color + ", Pick a Pawn")
            else:
                self.playerDisplay.changeText(self.turn.color + ", Click the Pawn")
        else:
            self.playerDisplay.changeText(self.turn.color + ", Pick a Pawn")
        

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
        self.turnMessage = TextBox(self.properties, self.width*8, self.height*1, self.centerX, self.centerY, self.x-int(self.width/1), int(self.y+self.width*2.75), colors["Secondary"], self.text, textColor=self.textColor)
    
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
        self.display = display
        self.tile.draw(display)
        if self.gridType[0].lower() =="b":
            return [self.gridType, self]
        elif self.gridType[0].lower() =="s":
            return [self.gridData, self]
        else:
            return [self.gridNum, self]
    
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
                self.pawn.remove(pawn)
        self.update()

    def update(self):
        self.tile.draw(self.display)
        if self.gridType[0].lower() == "b":
            for pawn in self.pawn:
                pawn.update()

class Player():
    def __init__(self, color, platform, bot=False) -> None:
        self.color = color
        self.bot = bot
        self.pawns = []
        self.pawnsOut = []
        for i in range(4):
            self.pawns.append(Pawn(self.color, platform, self))
        pass
    def givePawnsInfo(self, home, display, properties):
        self.home = home
        for pawn in self.pawns:
            pawn.setHome(home)
            pawn.draw(display, properties)
    
    def takeOutPawn(self, pawn):
        self.pawnsOut.append(pawn)

class Pawn():
    def __init__(self, color, platform, player) -> None:
        self.color = color
        self.platform = platform
        self.player = player
        self.out = False
        pass

    def draw(self, display, properties):
        self.properties = properties
        self.display = display
        self.pawn = TextBox(properties, 30, 30, True, True, self.x, self.y, colors[self.color], command=lambda: self.clicked())
        self.pawn.draw(display, colors["White"])

    def setHome(self, home):
        self.home = home
        home.addPawn(self)
        self.tile = home
        (self.x, self.y) = home.getPawnHomeCordinates(self)
        (self.ox, self.oy) = (self.x, self.y)

    def sendHome(self):
        
        self.home.addPawn(self)
        self.tile = self.home
        (self.x, self.y) = (self.ox, self.oy) # maybe move this 1 line down?
        self.home.update()

    def isOver(self, pos):
        if self.out == False:
            return self.pawn.isOver(pos)

    def clicked(self):
        if self.platform.turn == self.player: # players turn
            if self.platform.rolled == True: # player has rolled dice
                if self.tile == self.home and (self.platform.dice.value not in [6, 1]):
                    return
                # move pawn
                self.movePawn(self.tile.gridNum, self.platform.dice.value)
                pass
    
    def movePawn(self, prevLocation, diceValue):
        location = prevLocation
        stepsLeft = 0
        playerNum = self.platform.playerColors.index(self.color)+1 # gets the player num (id) ex: red = 1, orange = 2, green = 4
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
            loc = endLocation
            def getRange():
                if self.tile.gridType[0].lower() == "s":
                    return range(location, location + stepsLeft)
                else:
                    return range(endLocation, endLocation + stepsLeft)
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
            else:
                endTiles[endLocation].addPawn(self)
                self.tile.removePawn(self)
                self.tile.update()
                self.tile = endTiles[endLocation]
                self.x = endTiles[endLocation].x
                self.y = endTiles[endLocation].y
                self.draw(self.display, self.properties)

            pass # code for exit tiles here

        self.platform.nextPlayer(diceValue)
    
    def update(self):
        self.draw(self.display, self.properties)


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