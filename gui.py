import pygame
from colors import colors

class Selection():
    """class for creating a selection
    """
    def __init__(self, properties, text, centerX=False, centerY=False, x=0 , y=0, color=colors["Primary1"], hoverColor=None, title=None, numMode=False) -> None:
        """initiates the creation of the selection but does not draw it down on screen

        Args:
            properties (Properites): the properties of the game such as window dimentions
            text (list): list of selectin options
            centerX (bool, optional): if selection should be centered in x axis. Defaults to False.
            centerY (bool, optional): if selection should be centered in y axis. Defaults to False.
            x (int, optional): x cordinates or offset. Defaults to 0.
            y (int, optional): y cordinates or offset. Defaults to 0.
            color (tuple, optional): color of the textbox outlines). Defaults to colors["Primary1"].
            hoverColor (tuple, optional): color of hovercolor. Defaults to None.
            title (string, optional): the title of the selection. Defaults to None.
        """
        self.centerX = centerX
        self.x = x
        self.centerY = centerY
        self.y = y
        self.color = color
        if hoverColor != None:
            self.hoverColor = hoverColor
        else:
            self.hoverColor = colors["Secondary"]
        self.properties = properties
        self.title=title
        self.numMode = numMode
        if self.numMode:
            self.text = ["<", text, ">"]
        else:
            self.text = text
    
    def draw(self, display, size):
        """draws and places the selection on screen

        Args:
            display (Screen): the screen selection should be placed on
            size (int): the size of text
        """
        self.display = display
        self.items = []
        self.size = size
        if self.title != None:
            # Title text for selector
            self.title = TextBox(self.properties, len(self.title)*self.size*1.5, self.size, self.centerX, self.centerY, self.x, self.y-50, colors["Secondary"], text=self.title, textColor=colors["White"])
            self.title.draw(display)
            self.items.append(self.title)
        # the border for all the selection options
        self.border = TextBox(self.properties, len(self.text)*self.size*1.5, self.size, centerX=self.centerX, centerY=self.centerY, y=self.y, x=self.x, color=colors["Secondary"], hoverColor=self.hoverColor)
        self.border.draw(display, outline=self.color)
        self.items.append(self.border)
        # the selection options
        for sel in self.text:
            # formula for x cordinate
            xPosAdjustment = int((len(self.text)*self.size-self.size*0.2)*(self.text.index(sel)/(len(self.text)-1)) - (len(self.text)*self.size-self.size*0.2)/2)
            if sel not in ["<", ">"] and self.numMode:
                opt = TextBox(self.properties, self.size*0.8, self.size*0.6, self.centerX, self.centerY, self.x + xPosAdjustment, self.y, color=colors["DarkGrey"], text=sel)
            else:
                opt = TextBox(self.properties, self.size*0.8, self.size*0.6, self.centerX, self.centerY, self.x + xPosAdjustment, self.y, color=colors["DarkGrey"], text=sel, command=lambda x=sel: self.updateValue(x))
            opt.draw(display, self.color, self.size)
            self.items.append(opt)

    def updateValue(self, val):
        """updates the value selection (the choosen option)

        Args:
            val (string): the choosen option

        Returns:
            int: the shoosen value
        """
        
        if not self.numMode:
            self.value = val
            for it in self.items:
                if it == self.border or it == self.title: # if looped item is border or the title
                    continue
                elif val == it.text:
                    it.changeColor(colors["White"]) # selected
                    continue
                it.changeColor(colors["DarkGrey"]) # not selected
            return int(self.value)
        else:
            if val == "<":
                self.items[-2].text = str(int(self.items[-2].text)-1)
            elif val == ">":
                self.items[-2].text = str(int(self.items[-2].text)+1)
            self.update()

    def update(self):
        for it in self.items:
            if not (it == self.border or it == self.title):
                it.draw(self.display, self.color, self.size)
    
    def isOver(self, pos):
        """checks if mouse cordinates is over one off the selction options

        Args:
            pos (tuple): the cordinates of the mouse
        """
        
        def check(list):
            """returns true if mouse is over one of selection options

            Args:
                list (list): list of TextBoxes

            Returns:
                bool: true, if mouse is over one of the selection options
            """
            for it in list:
                if it == self.border or it == self.title: # if looped item is border or the title
                    continue
                if it.isOver(pos):
                    return True
            return False

        if check(self.items):
            for it in self.items:
                if it == self.border or it == self.title:
                    continue
                it.draw(self.display, self.color, self.size)
            return True
        return False

    def getOver(self, pos):
        """returns the textbox of the option the mouse is over

        Args:
            pos (tuple): the mouses cordinates

        Returns:
            TextBox: the textbox the mouse is over
        """
        for it in self.items:
            if it == self.border or it == self.title:
                continue
            if it.isOver(pos):
                print(it)
                return it
        return None


#https://www.youtube.com/watch?v=4_9twnEduFA&ab_channel=TechWithTim
class TextBox():
    """Class for creating a textbox. Can be used a a button, text info or a simple block
    """
    def __init__(self, properties, width, height, centerX=False, centerY=False, x=0 , y=0, color=(255,255,0), text='', hoverColor=None, command=None, textColor=(0,0,0)):
        """initates the textbox but does not draw and place it on screen

        Args:
            properties (Properies): the properties of the game such as window dimentions 
            width (int): the width of the textbox
            height (int): the height of the textbox
            centerX (bool, optional): if selection should be centered in x axis. Defaults to False.
            centerY (bool, optional): if selection should be centered in y axis. Defaults to False.
            x (int, optional): x cordinates or offset. Defaults to 0.
            y (int, optional): y cordinates or offset. Defaults to 0.
            color (tuple, optional): color of textbox bg. Defaults to (255,255,0).
            text (str, optional): the text of the textbox. Defaults to ''.
            hoverColor (tuple, optional): hovercolor. Defaults to None.
            command (lambda?, optional): the command that should be run if textbox clicked. Defaults to None.
            textColor (tuple, optional): the color of the text. Defaults to (0,0,0).
        """
        if isinstance(x, str): # translates string into dimentions
            x= x.replace("max", str(properties.width))
            x= int(eval(x)-width)
            
        if isinstance(y, str): # translates string into dimentions
            y= y.replace("max", str(properties.height))
            y= int(eval(y)-height)

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
        self.textColor = textColor
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
        """draws and places the textbox on screen

        Args:
            display (Screen): the screen the textbox should be placed on
            outline (tuple, optional): color of outline. Defaults to None.
            size (int, optional): text size. Defaults to 60.
        """
        #Call this method to draw the button on the screen
        self.display = display
        self.outline = outline
        self.size = size
        if outline:
            pygame.draw.rect(display, outline, (self.x-2,self.y-2,self.width+4,self.height+4), 0, border_radius=9)
            
        pygame.draw.rect(display, self.color, (self.x,self.y,self.width,self.height), 0, border_radius=8) # draw rectangle
        
        if self.text != '':
            font = pygame.font.SysFont(None, size)
            text = font.render(self.text, 1, self.textColor)
            display.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def changeColor(self, color):
        """changes the color of the bg. Used for selection options

        Args:
            color (tuple): the color to change to
        """
        self.color = color
        self.originalColor = color
        self.hoverColor = color
        self.draw(self.display, self.outline, self.size)

    def changeText(self, text):
        """method for changeing text on textbox

        Args:
            text (string): the new text to display
        """
        self.text = str(text) # updates text to new
        self.draw(self.display, self.outline, self.size) # draws the updated version

    def isOver(self, pos):
        """if mouse is over textbox:
        * change pointer
        * change color to hover and vise versa
        it also redraws the texbox

        Args:
            pos (tuple): cordinates of mouse

        Returns:
            bool: true, if mouse is over textbox
        """ 
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width: # if mouse is in x cordinate intervall
            if pos[1] > self.y and pos[1] < self.y + self.height: # if mouse is in y cordinate intervall
                if self.hover == False:
                    self.color = self.hoverColor
                    self.draw(self.display, self.outline, self.size)
                    if self.command != None: # if textbox have a command
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