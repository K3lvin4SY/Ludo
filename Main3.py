import pygame

colours = {"White":(255, 255, 255), "Black":(0, 0, 0), "Red":(255, 0, 0), "Green":(0, 255, 0), "Blue":(0, 0, 255)}

class Screen():
    def __init__(self, title, width=640, height=445, fill=colours["White"]):
        self.title = title
        self.width = width
        self.height = height
        self.fill = fill
        self.current = False

    def makeCurrent (self):
        pygame.display.set_caption(self.title)
        self.current=True
        self.screen=pygame.display.set_mode((self.width, self.height))

    def endCurrent(self):
        self.current=False

    def checkUpdate(self):
        return self.current

    def screenUpdate(self):
        if(self.current):
            self.screen.fill(self.fill)

    def returnTitle(self):
        return self.screen

class Button():
    def __init__(self, x, y, sx, sy, bcolour, fbcolour, font, fontsize, fcolour, text):
        self.x=x
        self.y=y
        self.sx=sx
               
        self.sy=sy
        self.bcolour=bcolour
        self.fbcolour=fbcolour
        self.fcolour=fcolour
        self.fontsize=fontsize
        self.text=text
        self.current=False
        self.buttonf=pygame.font.SysFont(font, fontsize)

    def showButton(self, display):
        if(self.current):
            pygame.draw.rect(display, self.fbcolour, (self.x, self.y, self.sx, self.sy))
        else:
            pygame.draw.rect(display, self.bcolour, (self.x, self.y, self.sx, self.sy))

        textsurface=self.buttonf.render(self.text, False, self.fcolour)
        display.blit(textsurface, ((self.x+(self.sx/2)-(self.fontsize/2)*(len(self.text)/2)-5, (self.y+(self.sy/2)-(self.fontsize/2) -4))))


    def focusCheck(self, mousepos, mouseclick):
        if(mousepos[0] >= self.x and mousepos[0] <= self.x+self.sx and mousepos[1] >= self.y and mousepos[1] <= self.y+self.sy):
            self.current=True
            return mouseclick[0]
        else:
            self.current = False
            return False

pygame.init()
pygame.font.init()

menuScreen=Screen("Menu Screen")
screen2=Screen("Screen 2")

win=menuScreen.makeCurrent()
done=False
testButton=Button(0, 0, 150, 50, colours["Black"], colours["Red"], "arial", 20, colours["White"], "Test")
returnButton=Button(0, 0, 150, 50, colours["White"], colours["Blue"], "arial", 20, colours["Black"], "Return")
toggle=False
while not done:
    menuScreen.screenUpdate()
    screen2.screenUpdate()
    mouse_pos=pygame.mouse.get_pos()
    mouse_click=pygame.mouse.get_pressed()
    keys=pygame.key.get_pressed()
    #menuscreen Page Code
    if menuScreen.checkUpdate():
        screen2button=testButton.focusCheck(mouse_pos, mouse_click)
        testButton.showButton(menuScreen.returnTitle())

        if screen2button:
            win=screen2.makeCurrent()
            menuScreen.endCurrent()
    
    #screen2 Page Code
    elif screen2.checkUpdate():
    #Back Button
        returnm=returnButton.focusCheck(mouse_pos, mouse_click)
        returnButton.showButton(screen2.returnTitle())

        if returnm:
            win=menuScreen.makeCurrent()
            screen2.endCurrent()
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            done=True

    pygame.display.update()
pygame.quit()