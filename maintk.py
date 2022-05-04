import tkinter as tk

class WindowHandler():
    def __init__(self):
        root = tk.Tk()
        root.title('Reverse Hang Man')
        properties = Properties(600, 600)
        root.geometry(str(properties.width) + 'x' + str(properties.height))
        root.resizable(False, False)

        # Define Frames
        menu = tk.Frame(root, width=properties.width, height=properties.height)
        gamePlatform = tk.Frame(root, width=properties.width, height=properties.height)
        endScreen = tk.Frame(root, width=properties.width, height=properties.height)
        scoreboardScreen = tk.Frame(root, width=properties.width, height=properties.height)
        menu.pack()

        root.mainloop()

class Properties():
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height

game = WindowHandler()