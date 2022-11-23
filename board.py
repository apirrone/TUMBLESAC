import numpy as np
import pygame

COLORS = {
    1 : (255, 0, 0), 
    2 : (0, 255, 0), 
    3 : (0, 0, 255),
    4 : (255, 0, 255),
    5 : (255, 255, 0),
    6 : (0, 0, 0)
}

class Board:
    def __init__(self, pos, w=5, h=15, nbColors=4, buffer_size=3):
        self.__pos         = pos
        self.__w           = w
        self.__h           = h
        self.__grid        = np.zeros((h, w))
        self.__buffer_size = buffer_size
        self.__buffer      = np.zeros(self.__buffer_size)
        self.__colors      = list(COLORS.keys())[:nbColors]
        self.__grid_backup = None

    def __getPossiblePositions(self):
        positions = []
        for j in range(self.__w):
            for i in range(0, self.__h):
                color = self.__grid[i][j]
                if color == 0:
                    positions.append((i, j))
                    break

        return positions

    def __getHighlightedBlock(self, charJPos):
        for i in range(self.__h):
            color = self.__grid[i][charJPos]
            if color == 0:
                if i == 0: # no blocks on this column
                    return None
                else:
                    return (i-1, charJPos)

    def getState(self):
        state = {}
        state["w"]           = self.__w
        state["h"]           = self.__h
        state["grid"]        = self.__grid
        state["buffer_size"] = self.__buffer_size
        state["buffer"]      = self.__buffer
        state["colors"]      = self.__colors

        return state

    def getSize(self):
        return self.__w, self.__h

    def populate(self, nb_blocks):

        self.__grid = np.zeros((self.__h, self.__w))

        # nb_blocks must be a multiple of 3
        while not (nb_blocks%self.__buffer_size == 0):
            nb_blocks += 1

        nb_blocks = min(nb_blocks, (self.__w*self.__h)-self.__h*2)
        
        for i in range(0, nb_blocks, self.__buffer_size):
            color = np.random.choice(self.__colors)
            possiblePositions = self.__getPossiblePositions()
            indicesPositions  = np.random.choice(len(possiblePositions), self.__buffer_size, replace=False)

            for index in indicesPositions:
                pos = possiblePositions[index]
                self.__grid[pos[0]][pos[1]] = color

        self.__grid_backup = self.__grid.copy()

    def populateFromState(self, state):
        self.__w           = state["w"]
        self.__h           = state["h"]
        self.__grid        = state["grid"]
        self.__buffer_size = state["buffer_size"]
        self.__buffer      = state["buffer"]
        self.__colors      = state["colors"]
        self.__grid_backup = self.__grid.copy()

    def reset(self):
        self.__grid = self.__grid_backup.copy()
        self.__buffer = np.zeros(self.__buffer_size)

    def getGridSize(self):
        return (self.__w, self.__h)

    def getPos(self):
        return self.__pos

    def __checkBuffer(self):
        if np.count_nonzero(self.__buffer) == len(self.__buffer):
            if np.all(self.__buffer == self.__buffer[0]): # are all the colors in the buffer the same
                self.__buffer = np.zeros(self.__buffer_size)
            else:
                self.reset()

    def isBoardEmpty(self):
        return np.count_nonzero(self.__grid) == 0

    def shoot(self, charJPos):
        blockPos = self.__getHighlightedBlock(charJPos)
        if blockPos is not None:
            color = self.__grid[blockPos[0]][blockPos[1]]
            self.__buffer[np.count_nonzero(self.__buffer)] = color
            self.__grid[blockPos[0]][blockPos[1]] = 0

            self.__checkBuffer()

    def highlightBlock(self, surface, scale, charJPos):
        blockPos = self.__getHighlightedBlock(charJPos)
        if blockPos is not None:
            pygame.draw.rect(surface, (255, 100, 255), ((self.__pos[1] + blockPos[1])*scale, (self.__pos[0] + blockPos[0])*scale, scale, scale), 5)

    def draw(self, surface, scale):
        # draw grid
        pygame.draw.rect(surface, (0, 0, 0), (self.__pos[1]*scale, self.__pos[0]*scale, self.__w*scale, self.__h*scale), 2)
        for i in range(self.__h):
            for j in range(self.__w):
                color = self.__grid[i][j]
                pos_i = (self.__pos[0] + i)*scale
                pos_j = (self.__pos[1] + j)*scale

                # when drawing, i and j are inverted
                if color != 0.:
                    pygame.draw.rect(surface, COLORS[color], (pos_j, pos_i, scale, scale))
                else:
                    pygame.draw.rect(surface, (100, 100, 100), (pos_j, pos_i, scale, scale))

        # draw buffer
        for i, color in enumerate(self.__buffer):
            pygame.draw.rect(surface, (0, 0, 0), ((self.__pos[1]+i)*scale, (self.__pos[0]-1)*scale, scale, scale), 2)
            if color != 0.:
                pygame.draw.rect(surface, COLORS[color], ((self.__pos[1]+i)*scale, (self.__pos[0]-1)*scale, scale, scale))


