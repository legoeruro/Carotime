import tkinter as tk
from functools import partial
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
import caroAI, platform, pygame, os, threading, time
from PIL import ImageTk, Image
import time
os.chdir(os.path.realpath(__file__)[:-9]+"assets")
class Window(tk.Tk):
    def __init__(self, search, Ox, Oy, consc):
        super().__init__()
        self.title("Caro")
        self.Buts = {}
        self.memory = []
        #xsize, ysize, winning condition, layers to search
        self.caro = caroAI.caro(Ox, Oy, consc, search)
        self.geometry('1000x600')
        self.Ox = Ox
        self.Oy = Oy


    def showFrame(self):
        bg = tk.PhotoImage(file="alfea.ppm")
        bglabel = tk.Label(self, image = bg)
        bglabel.PhotoImage = bg
        bglabel.place(x=0, y=0, relwidth=1, relheight=1)

        frame1 = tk.Frame(self)
        frame1.pack(padx = 0, pady = 48)
        frame2 = tk.Frame(self)
        frame2.pack()

        Undo = tk.Button(frame1, text = "Undo", width = 10, command = partial(self.Undo))
        Undo.grid(row = 0, column = 0, padx = 30)
        
        for x in range(self.Ox):   # tạo ma trận button Ox * Oy
            for y in range(self.Oy):
                self.Buts[x, y] = tk.Button(frame2, font = ('arial', 15, 'bold'), height = 1, width = 3, borderwidth = 2, command = partial(self.handleButton, x = x, y = y))
                self.Buts[x, y].grid(row = x, column = y)
    
    def Undo(self):
        if (len(self.memory) > 0):
            x = self.memory[len(self.memory) - 1][0]
            y = self.memory[len(self.memory) - 1][1]
            self.Buts[x, y]['text'] = ""
            self.memory.pop()
            self.caro.gameBoard[x][y] = ''
            x = self.memory[len(self.memory) - 1][0]
            y = self.memory[len(self.memory) - 1][1]
            self.Buts[x, y]['text'] = ""
            self.memory.pop()
            self.caro.gameBoard[x][y] = ''

    def handleButton(self, x, y):
        # self.movep1up()
        winning = ''
        if self.Buts[x,y]['text'] =="":
            if self.memory.count([x, y]) == 0:
                self.memory.append([x, y])
            if len(self.memory):
                self.Buts[x, y]['text'] = 'O'

                (x, y, winning) = self.caro.run(x, y)
                self.Buts[x, y].fg="red"
                self.Buts[x, y]['text'] = 'X'
                self.memory.append([x, y])
            res = winning
            if winning:
                self.destroy()

        
def rungame(search):
    Ox = 7 # Số lượng ô theo trục X
    Oy = 7 # Số lượng ô theo trục Y
    window = Window(search, Ox, Oy, 5)
    window.showFrame()
    os.environ['SDL_WINDOWID'] = str(window.winfo_id())
    os.environ['SDL_VIDEODRIVER'] = 'windib'
    window.mainloop()
    return window.caro.checkCondition()

if __name__ == "__main__":
    print(rungame(3))