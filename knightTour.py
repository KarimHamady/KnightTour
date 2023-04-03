import numpy as np


import random
import numpy
import pygame
from pygame.locals import*
import itertools
import heapq
import os

SIZE = (650, 650)
NUMBER_OF_COLUMNS = 24
BOARDBLOCKS = NUMBER_OF_COLUMNS
BOXSIZE = SIZE[1]// BOARDBLOCKS
SCREEN = pygame.display.set_mode(SIZE)
QUEENIMAGE = pygame.transform.scale(pygame.image.load(f'{os.path.abspath(os.getcwd())}\pngtree-black-chess-knight-horse-stallion-png-image_8864303.png').convert_alpha(), (BOXSIZE, BOXSIZE))
QUEENCOLOR = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (133,94,66)
pygame.display.set_caption("AI Algorithms")


class Render:
    def drawBoard(self):
        whiteBox = True
        for rowNumber, boardRow in enumerate(self.board):
            for boxNumber, box in enumerate(boardRow):
                boxColor = WHITE if whiteBox else BLACK
                pygame.draw.rect(SCREEN, boxColor, pygame.Rect(BOXSIZE*rowNumber, BOXSIZE*boxNumber, BOXSIZE, BOXSIZE))
                if box:
                    self.drawQueen(BOXSIZE*rowNumber, BOXSIZE*boxNumber)
                pygame.display.update()
                whiteBox = not whiteBox
            whiteBox = not whiteBox

    def drawQueen(self, row, column):
        # SCREEN.blit(QUEENIMAGE,(row, column))
        pygame.draw.circle(SCREEN, QUEENCOLOR, (row, column), BOXSIZE // 3)
        print(row, column)


class ChessBoard(Render):
    def __init__(self):
        self.board = numpy.zeros((BOARDBLOCKS, BOARDBLOCKS))
    
    def getBoard(self):
        return self.board
    
    def setValueAtBox(self, queenLocation, value):
        self.board[queenLocation[0]][queenLocation[1]] = value
    
    def placeQueen(self, queenLocation):
        self.setValueAtBox(queenLocation, 1)


class Grid:
    def __init__(self, numberOfColumns):
        self.numberOfColumns = numberOfColumns
        self.matrix = [[-1 for i in range(numberOfColumns)] for j in range(numberOfColumns) ]

    def possibleMovementsFromPos(self, currentPos):
        possibleMovements = [(currentPos[0]+i, currentPos[1]+j) for i, j in [(1, 2), (2, 1), (-1, -2), (-2, -1), (1, -2), (-2, 1), (-1, 2), (2, -1)]]
        acceptedMovements = []
        for newPos in possibleMovements:
            if 0 <= newPos[0] < self.numberOfColumns and 0 <= newPos[1] < self.numberOfColumns and self.matrix[newPos[0]][newPos[1]] == -1:
                acceptedMovements.append(newPos)
        return acceptedMovements
    
    def applyHeuristicOnPositions(self, possibleMovements):
        orderOfPositions = []
        for position in possibleMovements:
            orderOfPositions.append(len(self.possibleMovementsFromPos(position)))
        orderedPositions = [pos for idx, pos in sorted(zip(orderOfPositions, possibleMovements))]
        return orderedPositions
        
    def knightTour(self, current, pos, path=[]):
        path += [current]
        if pos == NUMBER_OF_COLUMNS**2:
            return path
        possibleMovements = self.possibleMovementsFromPos(current)
        arrangedMovements = self.applyHeuristicOnPositions(possibleMovements)
        for neighbor in arrangedMovements:
            self.matrix[neighbor[0]][neighbor[1]] = pos
            if self.knightTour(neighbor, pos+1, path):
                return path
            self.matrix[neighbor[0]][neighbor[1]] = -1
        return False
                
       

g = Grid(NUMBER_OF_COLUMNS)
g.matrix[2][2] = 0
path = g.knightTour((2,2), 1)
for j in range(NUMBER_OF_COLUMNS):
    print(path, g.matrix[j])
gameRunning = True
pygame.init()
SCREEN.fill(WHITE)
chess = ChessBoard()
chess.drawBoard()
counter = 1
for r, c in path:
    # chess.drawQueen(r*BOXSIZE + BOXSIZE/2, c*BOXSIZE + BOXSIZE/2)
    # pygame.draw.rect(SCREEN, (240, 240, 240), pygame.Rect(BOXSIZE*r, BOXSIZE*c, BOXSIZE, BOXSIZE))
    SCREEN.blit(QUEENIMAGE,(r*BOXSIZE, c*BOXSIZE))
    pygame.display.update()
    # pygame.time.delay(100)
    rect = pygame.Rect(BOXSIZE*r, BOXSIZE*c, BOXSIZE, BOXSIZE)
    pygame.draw.rect(SCREEN, (0, 255, 0), rect)

    font = pygame.font.Font(None, int(300/NUMBER_OF_COLUMNS))
    number_surface = font.render(str(counter), True, (255, 255, 255))
    center = rect.center
    number_center = number_surface.get_rect().center
    blit_position = (center[0] - number_center[0], center[1] - number_center[1])
    SCREEN.blit(number_surface, blit_position)
    counter += 1

    pygame.display.update()
    
while gameRunning:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
              carryOn = False

pygame.quit()
    