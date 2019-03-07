
#Import required libraries
 
from graphics import* #graphics.py by John Zelle

import random # Random number generator 


#Set constatnts to be used in program
#These can be changes to adjust dificulty or game length
# For a playable game NUMMBER_OF_MINES must be less than BOARD_WIDTH * BOARD_HEIGHT
 
SQUARE_WIDTH = 30
BOARD_WIDTH = 40
BOARD_HEIGHT = 20
NUMBER_OF_MINES = 100



def makeBoard():
    startx = 30
    starty = 30

    for r in range(BOARD_HEIGHT):
        
        y = starty + SQUARE_WIDTH*r
        
        row = []
        
        for c in range(BOARD_WIDTH):

            x = startx + SQUARE_WIDTH*c
        
            square = Rectangle(Point(x,y), Point(x+SQUARE_WIDTH, y+ SQUARE_WIDTH))
            bomb = False
            revealed = False
            
            tile = [square, bomb, revealed]

            tile[0].setFill('red')
            tile[0].draw(win)
            
            row.append(tile)
        board.append(row)

def inBoard(mouse):
    
    output = None
    for r in range(len(board)):
        if(output != None):
            break
        for c in range(len(board[r])):
            square = board[r][c][0]
      
            if inRectangle(mouse, square):
                output = [r,c]

                break
    return output
	
def inRectangle(mouse,rectangle):
    ptX = mouse.getX()
    ptY = mouse.getY()
    
    minPt = rectangle.getP1()
    maxPt = rectangle.getP2()
            
    minX = minPt.getX()
    minY = minPt.getY()

    maxX = maxPt.getX()
    maxY = maxPt.getY()

    if( ptX >= minX and ptX <= maxX and ptY >= minY and ptY <= maxY):
        return True
    else:
        return False
		
def setMines(loc):
    mines = chooseMineLocations(loc)
    for r in range(len(board)):
        for c in range(len(board[0])):
            board[r][c][1] = ([r,c] in mines)
			
def chooseMineLocations(loc):
    mines = []
                
    while(True):
        c = random.randint(0, BOARD_WIDTH - 1)
        r = random.randint(0, BOARD_HEIGHT - 1)
        tile = [r,c]
        if( tile not in mines and tile != loc):
            mines.append(tile)

        if(len(mines) >= (NUMBER_OF_MINES)):
           break
    
    return mines
			
def checkTile(loc):
    tile = board[loc[0]][loc[1]]
    
    if tile[1]:
        return True
    else:
        if not tile[2]:
            updateTile(loc)
        return False

def updateTile(loc):
    locs = []
    locs.append(loc)
    while(True):
        if(len(locs) == 0):
            break
        loc = locs[0]
        safe = []
        numBombs, safe = checkPerimeter(loc)
        
        tile = board[loc[0]][loc[1]]
        number = Text(tile[0].getCenter(), numBombs)
        tile[2] = True
        tile[0].undraw()
        tile[0].setFill('white')
        tile[0].draw(win)
        locs.remove(loc)
        if(numBombs != 0):
           number.draw(win)
        else:
            for space in safe:
                if(space not in locs):
                    
                    locs.append(space)		

def checkPerimeter(loc):
    
    x = loc[1]
    y = loc[0]
    numBombs = 0
    locs = []
    colRange = range(-1,2)
    rowRange = range(-1,2)

    
    if y == 0:
        rowRange = range(0,2)
    if x == 0:
        colRange = range(0,2)
 
    for dy in rowRange:
            for dx in colRange:
                try:
                    tile = board[y + dy][x + dx]
                    if(tile[1]):
                        numBombs += 1
                    if ( not tile[1] and not tile[2] ):
                        
                        locs.append([y+dy,x+dx])     
                except:
                    pass
    
    return (numBombs,locs)

def checkWin():
    i = 0
    for r in board:
        for c in r:
            if not c[2]:
                i+=1
    
    if i == NUMBER_OF_MINES:
        return True
    else:
        return False

def endGame(message):
    
    #Create second window for end game
    endWin = GraphWin('Mine Sweeper', 300, 200)
    endWin.setBackground('grey')
    
    #Create the objects for to be drawn on the end game window
    newGame = Rectangle(Point(50,50), Point(250,90))
    newGame.setFill('green')

    newGameLabel = Text(newGame.getCenter(),'Play Again')
    newGameLabel.setSize(20)

    end = Rectangle(Point(50,100),Point(250,140))
    end.setFill('red')
	
    endLabel = Text(end.getCenter(),'Quit')
    endLabel.setSize(20)
	
    label = Text(Point(150,20),message)
    label.setSize(20)
    label.setStyle('bold')
	
    #Draw the five objects onto the end game window
    newGame.draw(endWin)
    newGameLabel.draw(endWin)
    end.draw(endWin)
    endLabel.draw(endWin)
    label.draw(endWin)
    
    #Waits for one of the two rectangles to be clicked then decides the return value based on which one is clicked
    while(True):
        mouse = endWin.getMouse()
        if inRectangle(mouse, newGame):
            output = False
            break
        elif inRectangle(mouse, end):
            output = True
            break
    
    endWin.close()
    return output


    
def main():
    
    #Create the main window for the game and set up size and color
    global win
    win = GraphWin("Mine Sweeper", 60 + SQUARE_WIDTH*BOARD_WIDTH ,60 + SQUARE_WIDTH * BOARD_HEIGHT)
    win.setBackground('grey')
    
    #Makes the game board a global variable
    global board
    
    #Will restart the game until quit is pressed on the end game window breaking the while loop and closing the windows
    while(True):
		
        board = []
        message = ''
		
        makeBoard()
        loc = inBoard(win.getMouse())
        setMines(loc)
        checkTile(loc)

        while True:
            mouse = win.getMouse()
            loc = inBoard(mouse)
            if loc != None: 
                if checkTile(loc):
                    message = 'You Lose' 
                    break
                if checkWin():
                    message = 'You Win'
                    break
        if endGame(message):
            break
    win.close()
    

main()
