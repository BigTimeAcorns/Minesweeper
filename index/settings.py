# Some global variables I can use to change key things about the project
width = 600
height = 600
gridSize = 4
cellCount = gridSize ** 2 
numMines = (cellCount) // 4

# simple percent calculators for positioning
def heightPrct(percentage):
    return (height / 100) * percentage
def widthPrct(percentage):
    return (width / 100) * percentage