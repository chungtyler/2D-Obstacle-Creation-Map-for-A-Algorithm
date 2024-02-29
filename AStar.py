import pygame
import numpy as np
import math
import time

#Initialize Grid
pygame.init()
SCREEN_SIZE = 700
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
WATER = (114, 210, 237)
SAND = (247, 204, 101)
ROCK = (63, 63, 64)
screen.fill(WATER)
clock = pygame.time.Clock()
running = True

#Tile Class
class Tile:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.col = x // size
        self.row = y // size
        self.hCost = 1000000000
        self.gCost = 1000000000
        self.fCost = 1000000000
        self.parent = None

    def setColour(self, colour):
        rect = pygame.Rect(self.x + 2, self.y + 2, self.size - 4, self.size - 4)
        pygame.draw.rect(screen, colour, rect)

#Algorithm Functions
def initTiles(numTiles):
    tileSize = SCREEN_SIZE // numTiles
    tileMatrix = np.empty((numTiles, numTiles), dtype=Tile)
    for y in range(0, SCREEN_SIZE, tileSize):
        for x in range(0, SCREEN_SIZE, tileSize):
            xIndex = x // tileSize
            yIndex = y // tileSize
            currentTile = Tile(x, y, tileSize)
            currentTile.setColour(SAND)
            tileMatrix[yIndex][xIndex] = currentTile
    return tileMatrix

def setObstacle(x, y):
    pxPerTile = SCREEN_SIZE // TILE_NUMBER
    tileRow = y // pxPerTile
    tileCol = x // pxPerTile
    currentTile = TILE_MATRIX[tileRow][tileCol]

    mouseInputs = pygame.mouse.get_pressed()
    if mouseInputs[0]:
        OPEN = []
        OPEN.append(startNode)
        CLOSED = []
        if currentTile in OPEN:
            OPEN.remove(currentTile)
        elif currentTile in CLOSED:
            CLOSED.remove(currentTile)
        OBSTACLE.append(currentTile)
        currentTile.setColour(ROCK)
    elif mouseInputs[2]:
        OPEN = []
        OPEN.append(startNode)
        CLOSED = []
        if currentTile in OBSTACLE:
            OBSTACLE.remove(currentTile)
        currentTile.setColour(SAND)

def AStarSearch(currentTile, radius):
    OPEN.remove(currentTile)
    CLOSED.append(currentTile)
    currentTile.setColour((242, 145, 158))
    for col in range(-radius, radius + 1):
        for row in range(-radius, radius + 1):
            neighborCol = col + currentTile.col
            neighborRow = row + currentTile.row
            neighbor = TILE_MATRIX[neighborRow][neighborCol]
            if neighbor is currentTile or neighbor in OBSTACLE or neighbor in CLOSED:
                continue
            gCost = round(10 * math.sqrt(math.pow(neighborCol - currentTile.col,2) + math.pow(neighborRow - currentTile.row,2))) + currentTile.gCost
            hCost = round(10 * math.sqrt(math.pow(neighborCol - endNode.col,2) + math.pow(neighborRow - endNode.row,2)))
            fCost = gCost + hCost
            print("X: ", neighborCol, " Y: ", neighborRow, " gCost: ", gCost, " hCost: ", hCost, " fCost: ", fCost)
            if neighbor.fCost > fCost or neighbor not in OPEN:
                neighbor.fCost = fCost
                neighbor.gCost = gCost
                neighbor.hCost = hCost
                if neighbor not in OPEN:
                    OPEN.append(neighbor)
                    neighbor.parent = currentTile
                    neighbor.setColour((163, 255, 163))

def findAStarPath(tile):
    if not tile.parent:
        return
    parent = tile.parent
    parent.setColour((143, 143, 255))
    findAStarPath(parent)

#Initialize Settings
TILE_NUMBER = 20
TILE_MATRIX = initTiles(TILE_NUMBER)
OPEN = []
CLOSED = []
OBSTACLE = []

startNode = TILE_MATRIX[10][2]
OPEN.append(startNode)
startNode.setColour((46, 240, 75))

endNode = TILE_MATRIX[5][14]
endNode.setColour((224, 20, 85))

startNode.gCost = 0
startNode.hCost = round(10 * math.dist([startNode.col, endNode.col], [startNode.row, endNode.row]))
startNode.fCost = startNode.gCost + startNode.hCost

pygame.display.flip()
toggle = False
pathFound = False
#Run Events
while running:
    #Quit When Exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                toggle = True

    #Edit Terrain
    (mouseX, mouseY) = pygame.mouse.get_pos()
    setObstacle(mouseX, mouseY)

    if not toggle:
        pygame.time.wait(10)
        pygame.display.flip()
        continue
    #Algorithm Code Here
    lowestFCost = 10000000000
    for tile in OPEN:
        if tile.fCost < lowestFCost:
            currentTile = tile
            lowestFCost = tile.fCost

    if currentTile is not endNode:
        AStarSearch(currentTile, 1)
        pygame.time.wait(100)
    elif not pathFound:
        CLOSED.sort(key=lambda x: x.fCost,reverse=True)

        for tile in CLOSED:
            print(tile.fCost)
            if tile is startNode:
                pathFound = True
                break
            print("we have finished");
            findAStarPath(endNode);
    #Algorithm Code End
    startNode.setColour((46, 240, 75))
    endNode.setColour((224, 20, 85))
    #Update screen
    pygame.display.flip()
    pygame.time.wait(10)
    #clock.tick(60)

pygame.quit()
