from gui import *
from colors import colors

class BuildGrid:
    def __init__(self, gridSize, gridPlayers, properties) -> None:
        self.gridSize = gridSize
        self.gridPlayers = gridPlayers
        self.properties = properties

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
            self.tiles[coords] = Tile(self.properties, tbSize, getCoords(coords[0]), getCoords(coords[1])*-1, self.gridSize)
            self.tiles[coords].draw(self.display)
        self.interface = BuildInterface(self.properties, tbSize)
        self.interface.draw(self.display)

    def isOver(self, pos):
        pass

class Tile:
    def __init__(self, properties, dim, x, y, gridSize):
        self.width = dim
        self.height = dim
        self.x = x
        self.y = y
        self.gridSize = gridSize
        self.properties = properties
        self.tile = TextBox(self.properties, self.width, self.height, True, True, self.x + int((self.properties.width - self.properties.height-self.gridSize*8)/2), self.y, colors["DarkGrey"], command=lambda: self.clicked(), textColor=colors["White"])
    
    def draw(self, display):
        self.display = display
        self.tile.draw(self.display)
    
    def clicked(self):
        pass

class BuildInterface:
    def __init__(self, properties, dim) -> None:
        self.properties = properties
        self.dim = dim
        self.instruction = TextBox(self.properties, self.dim, self.dim, False, False, int(dim*2.6), dim*1, colors["Secondary"], "Select Game Path", textColor=colors["White"])
        self.nxtBtn = TextBox(self.properties, 150, 60, False, False, int(dim*2.1), "max-"+str(dim*1), colors["Primary1"], "Next", textColor=colors["Black"], command=lambda: self.clicked())
    
    def draw(self, display):
        self.display = display
        self.instruction.draw(display)
        self.nxtBtn.draw(display)
    
    def clicked(self):
        pass