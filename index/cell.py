# Imports Tkinter, random and settings.py
from tkinter import *
import random
import tkinter.messagebox
import settings

# This makes the Cell class and the button object
class Cell:
    # These are all the Class variables
    field = []
    revealed = []
    cellCount = settings.cellCount
    mineCount = settings.numMines
    newMineCount = settings.numMines
    mineCells = []
    guessedMines = []
    mineCountLabel = None
    gameOver = False
    def __init__(self,x, y, isMine=False):
        # These are all the button attributes
        self.isMine = isMine
        self.isRevealed = False
        self.button = None
        self.mineMaybe = False
        self.x = x
        self.y = y
        Cell.field.append(self)

    # This creates the button object
    def createCell(self,location):
        btn = Button(location, width=4, height=2,  bd=2, relief=RAISED)
        btn.bind('<Button-1>', self.left_Click)
        btn.bind("<Button-3>", self.right_Click)
        self.button = btn
    
    # This creates the label for the mine counter
    @staticmethod
    def createLabel(location):
        lbl = Label(location, bg='black',fg='red',text=Cell.newMineCount, font=('',40))
        Cell.mineCountLabel = lbl
        
    # This is a variable that runs everytime you click on a cell
    def left_Click(self, event):
        # First it checks if it's the first click
        if len(Cell.revealed) == 0:
            # It checks if the first cell you click on is a mine and removes it
            if self.isMine:
                print('dude it happened')
                self.isMine = False
                Cell.mineCount -= 1
                Cell.newMineCount -= 1
                Cell.mineCountLabel.configure(text=Cell.newMineCount)
        # Then it checks if any other time you click its a mine
        if self.isMine:
            # If you click on a mine it shows all the mines and stops you from playing
            for i in Cell.field:
                # Reveals every mine
                if i.isMine:
                    i.button.configure(bg='red')
                # This unbinds Left and Right click for all the cells
                for i in Cell.field:
                    i.button.unbind('<Button-1>')
                    i.button.unbind('<Button-3>')
        else:
            # If its not a mine it reveals the cell
            self.showCell()
            # If the number of mines surrounding the cell is 0 it reveals all those surrounding cells
            if self.surrMineCount == 0:
                for cell in self.surroundingCells:
                    cell.showCell()
            
        
    # This gets the position of the cell
    def getCellPos(self,x,y):
        for i in Cell.field:
            if i.x == x and i.y ==y:
                return i

    # This is a list of all the x,y coordinates of the surrounding cells
    '''
        
        {TOP LEFT(x-1, y-1)}     {TOP MID(x, y-1)}    {TOP RIGHT(x+1, y-1)}
    
        {MID LEFT(x-1, y)}       {MID(x, y)}          {MID RIGHT(x+1, y)}

        {BOTTOM LEFT(x-1, y+1)}  {BOTTOM MID(x, y+1)} {BOTTOM LEFT(x+1, y)}
    
    '''
    @property
    def surroundingCells(self):
        surrounding = [
            # It runs the 'getCellPos' function everytime with different parameters and puts all the return values in a list
            self.getCellPos(self.x - 1, self.y - 1),
            self.getCellPos(self.x - 1, self.y),
            self.getCellPos(self.x - 1, self.y + 1),
            self.getCellPos(self.x, self.y - 1),
            self.getCellPos(self.x + 1, self.y - 1),
            self.getCellPos(self.x + 1, self.y),
            self.getCellPos(self.x + 1, self.y + 1),
            self.getCellPos(self.x, self.y + 1),
        ]
        
        # This removes all the None values from the list incase you click on the edge of the board
        surrounding = [cell for cell in surrounding if cell is not None]
        return surrounding

    # This counts all the mines in the surrounding cells
    @property
    def surrMineCount(self):
        sum = 0
        for cell in self.surroundingCells:
            if cell.isMine:
                sum += 1
        return sum

    # This function runs everytime you want to reveal a cell/surrounding cell
    def showCell(self):
        # It changes the background colr
        self.button.configure(bg='gray')
        # Checks to make sure its not already revealed
        if not self.isRevealed:
            self.button.configure(text=self.surrMineCount, bd=1)
            # Changes the text of the cell to the number of surrounding mines
            if self.surrMineCount == 0:
                self.button.configure(text=" ")
            self.isRevealed = True
            Cell.revealed.append(self)
        # This checks to see if you win when you reveal that cell
        if len(Cell.revealed) == (Cell.cellCount - Cell.mineCount):
            self.win()

    # This runs if you win the game
    def win(self):
        # Shows a popup menu saying you won the game!
        tkinter.messagebox.showinfo('Won!','Congrats you won minesweeper!')
        # This unbinds left and right click for all the cells
        for i in Cell.field:
            i.button.unbind('<Button-1>')
            i.button.unbind('<BUtton-3>')


    # This funciton runs everytime you right click on a cell
    def right_Click(self, event):
        # Checks if its already revealed
        if self.isRevealed:
            return
        # Checks to see if you already guessed that cell
        if self.mineMaybe == False:
            # If it is a mine then it adds it to a list of correctly guessed mines
            if self.isMine:
                Cell.guessedMines.append(self)
            # If the number of correctly guessed mines equals the number of mines on the board then you win
            if len(Cell.guessedMines) == Cell.mineCount:
                self.win
            # Changes the text to ?
            self.button.configure(text="?")
            self.mineMaybe = True
            Cell.newMineCount -= 1
            #Then it changes the text of mine counter
            self.mineCountLabel.configure(text=Cell.newMineCount)
        # Checks to see if you already guessed that cell
        elif self.mineMaybe:
            # If its a mine it removes it from the correctly guessed mines list
            if self.isMine:
                Cell.guessedMines.remove(self)
            # reverts the text back to ' '
            self.button.configure(text=' ')
            self.mineMaybe = False
            Cell.newMineCount += 1
            # Then change the text of the mines counter
            self.mineCountLabel.configure(text=Cell.newMineCount)

    # This function randomly places mines in the board
    @staticmethod
    def placeMines():
        Cell.mineCells = random.sample(Cell.field, settings.numMines)
        for i in Cell.mineCells:
            i.isMine = True
        
    # This is just so that if you want to print the position of the cells it prints in a (x, y) format
    # For example Cell(0, 3)
    def __repr__(self):
        return f'Cell({self.x}, {self.y})'