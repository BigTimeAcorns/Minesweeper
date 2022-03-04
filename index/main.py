'''
Final Project: Minesweeper

By: Cade Dannels
Course: ICP2
Date: 2/10/2022
Description: This is a game written in Python using the Tkinter gui lirbrary. The object of the game is to find all the mines using the numbers in each square without clicking one.
'''

# This imports Tkinter(the GUI library im using), random, cell.py, settings.py, Pillow library(for images), os, andsys
import tkinter as tk
from tkinter import *
from random import randint
from cell import Cell
import settings
from PIL import ImageTk, Image
import os
import sys

main = tk.Tk()
main.title("Minesweeper")

# Command function for the reset button
def reset():
    python = sys.executable
    os.execl(python, python, * sys.argv)

# Setups the window and makes the grid of objects
def setup():

    # This centers the page in the middle of your screen, sets the height and width of the window, and puts it above all your other windows
    screenWidth = main.winfo_screenwidth()
    screenHeight = main.winfo_screenheight()
    center_x = int(screenWidth/2 - settings.height/2)
    center_y = int(screenHeight/2 - settings.width/2)
    main.geometry(f'{settings.width}x{settings.width}+{center_x}+{center_y}')
    main.attributes('-topmost', 1)

    # This is the top section of the window, for the counter and reset button
    topFrame = Frame(main, bd=8, relief=SUNKEN, width=settings.width, height=settings.heightPrct(10))
    topFrame.place(x=0,y=0)

    # This is the bottom section of the Window for the board
    centerFrame = Frame(main,bg='gray', bd=12 , relief=SUNKEN, width=settings.width, height=settings.heightPrct(90))
    centerFrame.place(x=0,y=settings.widthPrct(10) )

    # This is the Reset button right above the board
    smile = Image.open('images/minesweeper.png')
    resized = smile.resize((65, 65), Image.ANTIALIAS)
    newSmile = ImageTk.PhotoImage(resized)
    resetButton = Button(main, width= int(settings.heightPrct(8)), height = int(settings.heightPrct(8)), image=newSmile, command=reset)
    resetButton.image = newSmile
    resetButton.place(x = settings.width/2, y = 8)


    # This makes the grid of Objects/Buttons
    for x in range(settings.gridSize):
        for y in range(settings.gridSize):
            c = Cell(x, y)
            c.createCell(centerFrame)
            c.button.grid(row=x, column=y)
    Cell.createLabel(topFrame)
    Cell.mineCountLabel.place(x=0,y=0)
    Cell.placeMines()

def winning():
    pass

setup()


# This loops the code so you see the window, and everything on it, otherwise the window would appear and disappear instantly
main.mainloop()