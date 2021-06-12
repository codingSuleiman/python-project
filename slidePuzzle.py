import pygame as pg
import random

pg.init()
win=pg.display.set_mode()  

gameBoardWidth = 4
gameBoardHeight = 4
tileSize = 100
fontSize = 30

tileFont = pg.font.Font(None,fontSize)
counterFont = pg.font.Font(None,50)

#screenWidth = 1600
#screenHeight = 720

screenHeight = 1600
screenWidth = 720

moveUp = 'u'
moveDown = 'd'
moveLeft = 'l'
moveRight = 'r'

miliSec = 0
sec = 0

def getMainGameBoard():
    gameBoard = []
    boardFigures = 1
    
    for boardColumn in range(gameBoardWidth):
        innergameBoard = []
        
        for boardRow in range(gameBoardHeight):
            innergameBoard.append(boardFigures)
            boardFigures += gameBoardWidth
        boardFigures -= gameBoardWidth * (gameBoardHeight-1) + (gameBoardWidth-1)                  
        gameBoard.append(innergameBoard)
    gameBoard[gameBoardWidth - 1][gameBoardHeight - 1] = ''
    
    return gameBoard
    
def checkWinBoard(gameBoard):
    checkBoard = getMainGameBoard()
    if gameBoard == checkBoard:
        pass
    
        
def getEmptySpace():
    for tileX in range(gameBoardWidth):
        for tileY in range(gameBoardHeight):
            if gameBoard[tileX][tileY] == '':
                return tileX,tileY
                
def makeTileMove(boardMove):
     boardSpaceX,boardSpaceY=getEmptySpace()
     if boardMove == moveLeft:
        gameBoard[boardSpaceX][boardSpaceY], gameBoard[boardSpaceX-1][boardSpaceY] = gameBoard[boardSpaceX-1][boardSpaceY], gameBoard[boardSpaceX][boardSpaceY]

     if boardMove == moveRight:
         gameBoard[boardSpaceX][boardSpaceY], gameBoard[boardSpaceX+1][boardSpaceY] = gameBoard[boardSpaceX+1][boardSpaceY], gameBoard[boardSpaceX][boardSpaceY]
         
     if boardMove == moveUp:
         gameBoard[boardSpaceX][boardSpaceY], gameBoard[boardSpaceX][boardSpaceY-1] = gameBoard[boardSpaceX][boardSpaceY-1], gameBoard[boardSpaceX][boardSpaceY]
         
     if boardMove == moveDown:
         gameBoard[boardSpaceX][boardSpaceY], gameBoard[boardSpaceX][boardSpaceY+1] = gameBoard[boardSpaceX][boardSpaceY+1], gameBoard[boardSpaceX][boardSpaceY]
         
def isValidMove(tileMove):
    boardSpaceX,boardSpaceY=getEmptySpace()
    return ((tileMove == moveLeft and boardSpaceX != 0) or (tileMove == moveRight and boardSpaceX < len(gameBoard)-1) or (tileMove == moveUp and boardSpaceY != 0) or (tileMove == moveDown and boardSpaceY < len(gameBoard[0])-1))
    
def drawTile(row, column):
    boardPosX = (row*tileSize)+(screenWidth*0.5)-0.5*(tileSize*gameBoardWidth)
    boardPosY = (column*tileSize)+(screenHeight*0.5)-0.5*(tileSize*gameBoardHeight)

    borderPosX = (tileSize)+(screenWidth*0.5)-0.5*(tileSize*gameBoardWidth)-tileSize
    borderPosY = (tileSize)+(screenHeight*0.5)-0.5*(tileSize*gameBoardHeight)-tileSize
    
    pg.draw.rect(win,(255,100,100),(boardPosX, boardPosY, tileSize,tileSize))
    pg.draw.rect(win,(100,255,100),(boardPosX, boardPosY, tileSize,tileSize),1)
    pg.draw.rect(win,(100,255,100),(borderPosX, borderPosY, tileSize*gameBoardWidth, tileSize*gameBoardHeight),1) 
    
def drawTileFigure(tileFigure,row, column):
    boardPosX = (row*tileSize)+(screenWidth*0.5)-0.5*(tileSize*gameBoardWidth)
    boardPosY = (column*tileSize)+(screenHeight*0.5)-0.5*(tileSize*gameBoardHeight)
    
    tileNumber = tileFont.render(str(tileFigure),1,'white') 
    tileNumberRect = tileNumber.get_rect() 
    win.blit(tileNumber,((boardPosX+(tileSize//2)-fontSize//2+7), boardPosY+(tileSize//2)-fontSize//2+7))

def getSpotClick(x,y):
    for posX, valueX in enumerate(gameBoard):
        for posY, valueY in enumerate(valueX):
            boardPosX = (posX*tileSize)+(screenWidth*0.5)-0.5*(tileSize*gameBoardWidth)
            boardPosY = (posY*tileSize)+(screenHeight*0.5)-0.5*(tileSize*gameBoardHeight)
            tileRect = pg.Rect(boardPosX, boardPosY,tileSize,tileSize)
            if tileRect.collidepoint(x,y):
                return (posX,posY)
                   
    return (None, None)  
      
def drawBoardTile(gameBoard):
    boardSpaceX,boardSpaceY = getEmptySpace()
    for posX, valueX in enumerate(gameBoard):
        for posY, valueY in enumerate(valueX):
            if (boardSpaceX, boardSpaceY) != (posX, posY):
                drawTile(posX, posY)
                drawTileFigure(valueY,posX,posY)          
                
gameBoard = getMainGameBoard()

def showTime():
    global sec, miliSec
    borderPosX = ((tileSize)+(screenWidth*0.5)-0.5*(tileSize*gameBoardWidth)-tileSize)+(tileSize+0.5*tileSize-20)
    borderPosY = ((tileSize)+(screenHeight*0.5)-0.5*(tileSize*gameBoardHeight)-tileSize)-50
    gameCounter = counterFont.render(str(sec) +':'+ str(miliSec),1,'black')
    win.blit(gameCounter, (borderPosX, borderPosY))
    miliSec += 1
    if miliSec == 85:
        sec += 1
        miliSec = 0
def scatter():
    for i in range(300):
        shuffle = random.choice(['u','d','l','r'])
        if isValidMove(shuffle):
            makeTileMove(shuffle) 
        
scatter()     
while True:
    slideTo = None 
    win.fill((0,255,255))
    
    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONUP:
            pos = pg.mouse.get_pos()
            spotX,spotY = getSpotClick(pos[0],pos[1])
            if (spotX,spotY) != (None,None):
                boardSpaceX, boardSpaceY = getEmptySpace()
                if spotX == boardSpaceX and spotY == boardSpaceY-1:
                    slideTo = moveUp
                elif spotX == boardSpaceX and spotY == boardSpaceY+1:
                    slideTo = moveDown
                elif spotX == boardSpaceX-1 and spotY == boardSpaceY:
                    slideTo = moveLeft
                elif spotX == boardSpaceX+1 and spotY == boardSpaceY:
                    slideTo = moveRight
                        
    if isValidMove(slideTo):
        makeTileMove(slideTo)          
    drawBoardTile(gameBoard)
    checkWinBoard(gameBoard)
    showTime()
    pg.display.flip()
    