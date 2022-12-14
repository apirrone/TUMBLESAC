import pygame
from tumblesac.scenes.scene import Scene
from tumblesac.board import Board
from tumblesac.character import Character
import numpy as np


class GameScene(Scene):
    def __init__(self, w, h, scale, network=None, infinite=False):
        super().__init__(w, h, scale)

        self.__network = network
        self.__infinite = infinite
        self.__board = Board((2, 1), infinite=self.__infinite)
        self.__score = 0

        if self.__network is None:
            self.__board.populate(100)
        else:
            self.__board.populateFromState(self.__network.getInitialBoardState())

            self.__playersBoards = {}
            self.__playersNames = {}
            self.__playersCharacters = {}
            i = 1
            for id, player in self.__network.getPlayers().items():
                if id != self.__network.getMyID():
                    w, h = self.__board.getSize()
                    self.__playersBoards[id] = Board((2, 1 + w * i + i))
                    self.__playersBoards[id].populateFromState(
                        self.__network.getInitialBoardState()
                    )
                    self.__playersNames[id] = None
                    self.__playersCharacters[id] = Character(
                        (0, 0, 255),
                        self.__playersBoards[id].getGridSize(),
                        self.__playersBoards[id].getPos(),
                    )
                    i += 1

        self.__character = Character(
            (50, 50, 50), self.__board.getGridSize(), self.__board.getPos()
        )

        self.__next_action = None

    def input(self):
        events, action = super().input()
        ok = True
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        self.__character.move(-1)
                    else:
                        self.__character.move(-1000)
                elif event.key == pygame.K_RIGHT:
                    if not pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        self.__character.move(1)
                    else:
                        self.__character.move(1000)
                elif event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    ok = self.__board.shoot(self.__character.getJPos())
                elif event.key == pygame.K_DOWN:
                    if not self.__infinite:
                        self.__board.reset()

        if action == "esc" or not ok:
            if self.__infinite:
                action = "go_to_retry_scene"
            else:
                action = "go_to_title_scene"
        if self.__next_action is not None:
            action = self.__next_action

        return events, action

    def getScore(self):
        if self.__infinite:
            return self.__score
        else:
            return 0

    def getNetwork(self):
        return self.__network

    def update(self, dt):
        super().update(dt)

        if self.__network is not None:
            self.__network.sendUpdate(
                self.__board.getState(), self.__character.getJPos(), dt
            )
            self.__network.getUpdate(dt)

            for id, player in self.__network.getPlayers().items():
                if id != self.__network.getMyID():
                    name = player["name"]
                    if self.__playersNames[id] is None:
                        self.__playersNames[id] = name
                    boardState = player["boardState"]
                    if boardState is not None:
                        self.__playersBoards[id].populateFromState(boardState)

                    charJPos = player["charJPos"]
                    if charJPos is not None:
                        self.__playersCharacters[id].setJPos(charJPos)

        if self.__board.isBoardEmpty() and not self.__infinite:
            if self.__network is not None:
                if not self.__network.winSent():
                    self.__network.sendWin()
            else:
                self.__next_action = "go_to_title_scene"

        if self.__board.isBoardLost():
            self.__next_action = "go_to_retry_scene"

        self.__score = self.__board.getBlocksShot()

    def draw(self, screen):
        super().draw()

        self.__board.draw(
            self._surface, self._scale, self.__character.getJPos(), self._dt
        )
        self.__board.highlightBlock(
            self._surface, self._scale, self.__character.getJPos()
        )
        self.__character.draw(self._surface, self._scale)
        if self.__infinite:
            label = pygame.font.SysFont(None, self._scale).render(
                "Score : " + str(self.__score), 1, (0, 0, 0)
            )
            self._surface.blit(label, (7 * self._scale, 10 * self._scale))

            circlePos = (10, 13)
            pygame.draw.circle(
                self._surface,
                (0, 200, 0),
                tuple(np.array(circlePos) * self._scale),
                2 * self._scale,
            )

            angleValue = (
                min(
                    self.__board.getTimeoutLastShot(),
                    self.__board.getElapsedSinceLastShot(),
                )
                * (1 / self.__board.getTimeoutLastShot())
                * np.pi
                * 2
                + np.pi / 2
            )
            pygame.draw.arc(
                self._surface,
                (255, 0, 0),
                np.array([circlePos[0] - 2, circlePos[1] - 2, 4, 4]) * self._scale,
                np.pi / 2,
                angleValue,
                width=2 * self._scale,
            )

        if self.__network is not None:
            label = pygame.font.SysFont(None, self._scale).render(
                self.__network.getMyName(), 1, (0, 0, 0)
            )
            self._surface.blit(label, (self.__board.getPos()[1] * self._scale, 0))

            for id, board in self.__playersBoards.items():
                name = self.__playersNames[id]
                label = pygame.font.SysFont(None, self._scale).render(
                    name, 1, (0, 0, 0)
                )
                self._surface.blit(label, (board.getPos()[1] * self._scale, 0))
                if id != self.__network.getMyID():
                    board.draw(
                        self._surface,
                        self._scale,
                        self.__playersCharacters[id].getJPos(),
                        self._dt,
                    )
                    self.__playersCharacters[id].draw(self._surface, self._scale)

        screen.blit(self._surface, (0, 0))
