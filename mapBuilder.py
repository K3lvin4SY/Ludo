import sys
from gui import *
from colors import colors
import json
from os.path import exists

class BuildGrid:
    def __init__(self, gridSize, gridPlayers, properties, system) -> None:
        self.system = system
        self.gridSize = gridSize
        self.gridPlayers = gridPlayers
        self.properties = properties
        self.pathTiles = {}
        self.endTiles = {}
        self.baseTiles = {}
        self.goal = []
        self.dice = []
        self.status = "N"
        self.blockPlaced = False
        self.playerColors = [
            "Blue",
            "Yellow",
            "Lime",
            "Red",
            "Purple",
            "Orange",
            "Pink",
            "Cyan",
            "Green"
            ]
        
        self.statList = ["N"]#, "E1", "E2", "E3", "E4", "X1", "X2", "X3", "X4", "S1", "S2", "S3", "S4", "G", "D"]
        for e in range(1, self.gridPlayers+1):
            self.statList.append("E"+str(e))
        for x in range(1, self.gridPlayers+1):
            self.statList.append("X"+str(x))
        for s in range(1, self.gridPlayers+1):
            self.statList.append("S"+str(s))
        for b in range(1, self.gridPlayers+1):
            self.statList.append("b"+str(b))
        self.statList.append("G")
        self.statList.append("D")
        self.statList.append("F")

        self.tiles = {}
        for x in range(self.gridSize):
            x += 1
            for y in range(self.gridSize):
                y += 1
                self.tiles[(x, y)] = None

    def draw(self, display):
        self.display = display

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
            #y= int(((cor-1))/(gridSize-1)*(self.properties.height-gridSize*8))
            return y
        tbSize = int((self.properties.height/self.gridSize)*0.93)

        for coords in self.tiles:
            self.tiles[coords] = Tile(self.properties, tbSize, getCoords(coords[0]), getCoords(coords[1])*-1, self, coords[0], coords[1])
            self.tiles[coords].draw(self.display)
        self.interface = BuildInterface(self.properties, tbSize, self)
        self.interface.draw(self.display)

    def isOver(self, pos):
        for tile in list(self.tiles.values()):
            if tile.isOver(pos):
                return True
        if self.interface.nxtBtn.isOver(pos):
            return True
        return False

    def getOver(self, pos):
        for tile in list(self.tiles.values()):
            if tile.isOver(pos):
                return tile.tile
        if self.interface.nxtBtn.isOver(pos):
            return self.interface.nxtBtn
        return None

    def setStatus(self):
        
        found = False
        for stat in self.statList:
            if found:
                self.status = stat
                break
            if stat == self.status:
                found = True
        
        if self.status[0] == "E":
            self.interface.instruction.changeText("Place Player "+str(self.status[-1])+" Entry")
        elif self.status[0] == "X":
            self.interface.changeText("Place Player "+str(self.status[-1])+" Exit")
        if self.status[0] == "S":
            self.interface.changeText("Place Player "+str(self.status[-1])+" Exit Path")
        if self.status[0] == "b":
            self.interface.changeText("Place Player "+str(self.status[-1])+" Home")
        if self.status[0] == "G":
            self.interface.changeText("Place Goal")
        if self.status[0] == "D":
            self.interface.changeText("Place Dice")
            self.interface.nxtBtn.changeText("Done")
        if self.status[0] == "F":
            self.createMap()
    
    def createMap(self):
        mapDict = {
            "dimentions":self.gridSize,
            "participants":self.gridPlayers,
            "colors":[],
            "map":{},
            "map-end":{},
            "map-base":{},
            "dice":[]
        }
        for pc in range(self.gridPlayers):
            mapDict["colors"].append(self.playerColors[pc])
        for pt in self.pathTiles:
            mapDict["map"][pt] = [self.pathTiles[pt].gx, self.pathTiles[pt].gy]
        for et in self.endTiles:
            mapDict["map-end"][et] = [self.endTiles[et].gx, self.endTiles[et].gy]
        for bt in self.baseTiles:
            mapDict["map-base"][bt] = [self.baseTiles[bt].gx, self.baseTiles[bt].gy]
        endPosNums = []
        for et in mapDict["map-end"]:
            endPosNums.append(int(et.split("-")[0]))
        mapDict["map-end"][str(max(endPosNums)+1)+"-S"] = [self.goal.gx, self.goal.gy]
        mapDict["dice"] = [self.dice.gx, self.dice.gy]
        self.saveMap(mapDict)
    
    def saveMap(self, map):
        filePath = "maps/"
        file = "myMap"
        if exists(filePath+file+".json"):
            fileNum = 1
            while True:
                fileNum += 1
                file = "myMap ("+str(fileNum)+")"
                if not exists(filePath+file+".json" or fileNum == 1000):
                    break

        with open(filePath+file+".json", "w") as outfile:
            json.dump(map, outfile, indent=4)
        self.system.changeScreen("main")
        

    def addTileToList(self, tile):
        '''
        for tl in self.tiles:
            if self.tiles[tl] == tile:
                self.pathTiles[str(len(self.pathTiles))+"-N"] = tl
        '''
        if self.status == "N":
            if tile.status is None:
                self.pathTiles[str(len(self.pathTiles)+1)+"-"+self.status] = tile
                tile.tile.changeText(str(len(self.pathTiles)))
                tile.tile.changeColor(colors["White"])
                tile.setStatus(self.status)
        elif self.status[0] == "E":
            if tile.status == "N":
                if self.blockPlaced != self.status:
                    tile.setStatus(self.status)
                    tile.tile.changeColor(colors[self.playerColors[int(self.status[-1])-1]])
                    tmpDict = dict(self.pathTiles)
                    for pt in self.pathTiles:
                        if tmpDict[pt] == tile:
                            del tmpDict[pt]
                            tmpDict[pt.replace("N", self.status)] = tile
                    self.pathTiles = dict(tmpDict)
                    self.blockPlaced = self.status
        elif self.status[0] == "X":
            if tile.status == "N":
                if self.blockPlaced != self.status:
                    tile.setStatus(self.status)
                    tile.tile.changeColor(colors[self.playerColors[int(self.status[-1])-1]])
                    tmpDict = dict(self.pathTiles)
                    for pt in self.pathTiles:
                        if tmpDict[pt] == tile:
                            del tmpDict[pt]
                            tmpDict[pt.replace("N", self.status)] = tile
                    self.pathTiles = dict(tmpDict)
                    self.blockPlaced = self.status
        elif self.status[0] == "S":
            if tile.status is None:
                sNum = 0
                for et in self.endTiles:
                    if et.split("-")[1] == self.status:
                        sNum += 1
                tile.setStatus(self.status)
                tile.tile.changeColor(colors[self.playerColors[int(self.status[-1])-1]])
                tile.tile.changeText(str(sNum+1))
                self.endTiles[str(sNum+1)+"-"+self.status] = tile
        elif self.status[0] == "b":
            if tile.status is None:
                if self.blockPlaced != self.status:
                    tile.setStatus(self.status)
                    tile.tile.changeColor(colors[self.playerColors[int(self.status[-1])-1]])
                    tile.tile.changeText("H"+str(self.status[-1]))
                    self.baseTiles[self.status] = tile
                    self.blockPlaced = self.status
        elif self.status[0] == "G":
            if tile.status is None:
                if self.blockPlaced != self.status:
                    tile.setStatus(self.status)
                    tile.tile.changeColor(colors["White"])
                    tile.tile.changeText("G")
                    self.goal = tile
                    self.blockPlaced = self.status
        elif self.status[0] == "D":
            if tile.status is None or tile.status == "G":
                if self.blockPlaced != self.status:
                    tile.setStatus(self.status)
                    tile.tile.changeColor(colors["White"])
                    tile.tile.changeText("D")
                    self.dice = tile
                    self.blockPlaced = self.status

                

class Tile:
    def __init__(self, properties, dim, x, y, grid, gx, gy):
        self.width = dim
        self.height = dim
        self.x = x
        self.y = y
        self.gx = gx
        self.gy = gy
        self.grid = grid
        self.status = None
        self.gridSize = grid.gridSize
        self.properties = properties
        self.tile = TextBox(self.properties, self.width, self.height, True, True, self.x + int((self.properties.width - self.properties.height-self.gridSize*8)/2), self.y, colors["DarkGrey"], command=lambda: self.clicked(), textColor=colors["Black"])
    
    def draw(self, display):
        self.display = display
        self.tile.draw(self.display)
    
    def setStatus(self, status):
        self.status = status
    
    def clicked(self):
        self.grid.addTileToList(self)
        pass

    def isOver(self, pos):
        return self.tile.isOver(pos)



class BuildInterface:
    def __init__(self, properties, dim, grid) -> None:
        self.properties = properties
        self.grid = grid
        self.dim = dim
        self.instruction = TextBox(self.properties, self.dim*6, self.dim, False, False, int(dim*0.1), dim*1, colors["Secondary"], "Select Game Path", textColor=colors["White"])
        self.nxtBtn = TextBox(self.properties, 150, 60, False, False, int(dim*2.1), "max-"+str(dim*1), colors["Primary1"], "Next", textColor=colors["Black"], command=lambda: self.clicked())
    
    def draw(self, display):
        self.display = display
        self.instruction.draw(display)
        self.nxtBtn.draw(display)
    
    def clicked(self):
        self.grid.setStatus()

    def changeText(self, text):
        self.instruction.changeText(text)