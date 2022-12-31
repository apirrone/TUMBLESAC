import numpy as np
import pygame
import time

COLORS = {
    1: (255, 0, 0),
    2: (0, 255, 0),
    3: (0, 0, 255),
    4: (255, 0, 255),
    5: (255, 255, 0),
    6: (0, 0, 0),
}


class Board:
    def __init__(self, pos, w=5, h=15, nbColors=4, buffer_size=3, infinite=False):
        self.__pos = pos
        self.__w = w
        self.__h = h
        self.__grid = np.zeros((h, w))
        self.__grid_buffer = None
        self.__buffer_size = buffer_size
        self.__infinite = infinite
        self.__i_offset = 0
        self.__buffer = np.zeros(self.__buffer_size)
        self.__colors = list(COLORS.keys())[:nbColors]
        self.__grid_backup = None

        self.__blocksShot = 0
        self.__lastTimeShot = time.time()
        self.__speed = 0

    def __shiftBoardDown(self):
        if (
            self.__grid_buffer is None or np.all(self.__grid_buffer[-1, :]) == 0
        ):  # if contains one zero
            self.__grid_buffer = self.__populateGrid(
                30, grid=self.__grid_buffer, reverse=True
            )

        row = self.__grid_buffer[-1, :]
        self.__grid = np.vstack((row, self.__grid))
        self.__grid = self.__grid[:-1, :]
        self.__grid_buffer = np.vstack((np.zeros(self.__w), self.__grid_buffer))
        self.__grid_buffer = self.__grid_buffer[:-1, :]

    def __getPossiblePositions(self, grid, reverse=False):
        positions = []
        for j in range(self.__w):
            if not reverse:
                for i in range(0, self.__h):
                    color = grid[i][j]
                    if color == 0:
                        positions.append((i, j))
                        break
            else:
                for i in range(self.__h - 1, 0, -1):
                    color = grid[i][j]
                    if color == 0:
                        positions.append((i, j))
                        break

        return positions

    def __getHighlightedBlock(self, charJPos):
        for i in range(self.__h):
            color = self.__grid[i][charJPos]
            if color == 0:
                if i == 0:  # no blocks on this column
                    return None
                else:
                    return (i - 1, charJPos)

    def __getSpeed(self):

        # speed = max(1, np.exp(self.__blocksShot/17))
        speed = max(1, (self.__blocksShot / 17) ** 2)
        return speed

    def getBlocksShot(self):
        return self.__blocksShot

    def getState(self):
        state = {}
        state["w"] = self.__w
        state["h"] = self.__h
        state["grid"] = self.__grid
        state["buffer_size"] = self.__buffer_size
        state["buffer"] = self.__buffer
        state["colors"] = self.__colors

        return state

    def getSize(self):
        return self.__w, self.__h

    def __populateGrid(self, nb_blocks, grid=None, reverse=False):
        if grid is None:
            grid = np.zeros((self.__h, self.__w))

        # nb_blocks must be a multiple of buffer_size
        while not (nb_blocks % self.__buffer_size == 0):
            nb_blocks += 1

        nb_blocks = min(nb_blocks, (self.__w * self.__h) - self.__h * 2)

        for i in range(0, nb_blocks, self.__buffer_size):
            color = np.random.choice(self.__colors)
            possiblePositions = self.__getPossiblePositions(grid, reverse=reverse)
            try:
                indicesPositions = np.random.choice(
                    len(possiblePositions), self.__buffer_size, replace=False
                )
            except ValueError as e:
                print(e)
                continue

            for index in indicesPositions:
                pos = possiblePositions[index]
                grid[pos[0]][pos[1]] = color

        return grid

    def populate(self, nb_blocks):
        self.__grid = self.__populateGrid(nb_blocks)

        self.__grid_backup = self.__grid.copy()

    def populateFromState(self, state):
        self.__w = state["w"]
        self.__h = state["h"]
        self.__grid = state["grid"]
        self.__buffer_size = state["buffer_size"]
        self.__buffer = state["buffer"]
        self.__colors = state["colors"]
        self.__grid_backup = self.__grid.copy()

    def reset(self):
        self.__grid = self.__grid_backup.copy()
        self.__buffer = np.zeros(self.__buffer_size)

    def getGridSize(self):
        return (self.__w, self.__h)

    def getPos(self):
        return self.__pos

    def isBoardLost(self):
        ok = False
        if self.__infinite and np.any(self.__grid[-1, :]) != 0:
            ok = True
        return ok

    def __checkBuffer(self):
        ok = True

        colors = self.__buffer[np.nonzero(self.__buffer)]

        if len(colors) > 1:
            if np.all(colors == colors[0]):
                if len(colors) == self.__buffer_size:
                    self.__buffer = np.zeros(self.__buffer_size)
                    self.__blocksShot += self.__buffer_size

            else:
                if self.__infinite:
                    ok = False
                else:
                    self.reset()

        return ok

    def checkLastShot(self, color):
        """
        Checks if last shot is the same color as the previous block in buffer
        to avoid one missed input.
        :param: color: the color of the last shot
        """
        nz = np.count_nonzero(self.__buffer) + 1
        if nz == 1:  # buffer empty
            self.__lastColorShot = color
            self.__missedShot = False
            return True
        # as we anticipate, we are above real number of blocks inside buffer
        if nz >= 1:  # at least one color block in buffer
            if not self.__lastColorShot:  # first color entering buffer
                raise ValueError("lastColorShot")
            else:
                if self.__lastColorShot == color:
                    self.__missedShot = False
                else:
                    if not self.__missedShot:
                        self.__missedShot = True
                        return False
        else:
            raise ValueError("nz")
        return True

    def isBoardEmpty(self):
        return np.count_nonzero(self.__grid) == 0

    def shoot(self, charJPos):
        self.__lastTimeShot = time.time()
        ok = True
        blockPos = self.__getHighlightedBlock(charJPos)
        if blockPos is not None:
            color = self.__grid[blockPos[0]][blockPos[1]]

            if self.checkLastShot(color):
                self.__buffer[np.count_nonzero(self.__buffer)] = color
                self.__grid[blockPos[0]][blockPos[1]] = 0

                ok = self.__checkBuffer()

        if not self.__infinite:
            ok = True

        return ok

    def highlightBlock(self, surface, scale, charJPos):
        blockPos = self.__getHighlightedBlock(charJPos)
        if blockPos is not None:
            pygame.draw.rect(
                surface,
                (255, 100, 255),
                (
                    (self.__pos[1] + blockPos[1]) * scale,
                    (self.__pos[0] + blockPos[0]) * scale + self.__i_offset,
                    scale,
                    scale,
                ),
                5,
            )

    def draw(self, surface, scale, charJPos, dt):
        if self.__infinite:

            elapsedSinceLastShot = time.time() - self.__lastTimeShot
            if elapsedSinceLastShot > 0.3 and self.__blocksShot > 1:
                self.__speed += elapsedSinceLastShot*0.01
            self.__i_offset += scale * (dt * 0.0001) * self.__speed
            # self.__i_offset += scale * (dt * 0.0001) * self.__getSpeed()
            if self.__i_offset >= scale:
                self.__shiftBoardDown()
                self.__i_offset = 0
        # draw grid background
        pygame.draw.rect(
            surface,
            (100, 100, 100),
            (
                self.__pos[1] * scale,
                self.__pos[0] * scale,
                self.__w * scale,
                self.__h * scale,
            ),
        )

        # draw ray
        rayStartX = (self.__pos[1] + charJPos) * scale + scale // 2
        rayStartY = (self.__h - 1 + self.__pos[0]) * scale
        rayEndY = (self.__pos[1] + 1) * scale
        pygame.draw.line(
            surface, (255, 0, 0), (rayStartX, rayStartY), (rayStartX, rayEndY), width=5
        )

        # draw grid
        for i in range(self.__h):
            for j in range(self.__w):
                color = self.__grid[i][j]
                pos_i = (self.__pos[0] + i) * scale + self.__i_offset
                pos_j = (self.__pos[1] + j) * scale

                # when drawing, i and j are inverted
                if color != 0.0:
                    pygame.draw.rect(
                        surface, COLORS[color], (pos_j, pos_i, scale, scale)
                    )
                # else:
                #     pygame.draw.rect(surface, (100, 100, 100), (pos_j, pos_i, scale, scale))

        # draw buffer
        for i, color in enumerate(self.__buffer):
            pygame.draw.rect(
                surface,
                (0, 0, 0),
                (
                    (self.__pos[1] + i) * scale,
                    (self.__pos[0] - 1) * scale,
                    scale,
                    scale,
                ),
                2,
            )
            if color != 0.0:
                pygame.draw.rect(
                    surface,
                    COLORS[color],
                    (
                        (self.__pos[1] + i) * scale,
                        (self.__pos[0] - 1) * scale,
                        scale,
                        scale,
                    ),
                )

        if self.__infinite:
            pygame.draw.rect(
                surface,
                (255, 255, 255),
                (self.__pos[1] * scale, self.__pos[0] * scale, self.__w * scale, scale),
            )
