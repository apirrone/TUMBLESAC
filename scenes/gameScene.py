import pygame
from scenes.scene import Scene
from board import Board
from character import Character

class GameScene(Scene):
    def __init__(self, w, h, scale):
        super().__init__(w, h, scale)

        self.__board     = Board((2, 1))
        self.__board.populateBoard(30)
        self.__character = Character((50, 50, 50), self.__board.getGridSize(), self.__board.getPos())

    def input(self):
        events, action = super().input()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.__character.move(-1)
                elif event.key == pygame.K_RIGHT:
                    self.__character.move(1)
                elif event.key == pygame.K_SPACE:
                    self.__board.shoot(self.__character.getJPos())
                elif event.key == pygame.K_DOWN:
                    self.__board.reset()

        if action == "esc":
            action = "go_to_title_scene"

        return events, action

    def update(self, dt):
        super().update(dt)

    def draw(self, screen):
        super().draw(screen)

        self.__board.draw(self._surface, self._scale)
        self.__board.highlightBlock(self._surface, self._scale, self.__character.getJPos())
        self.__character.draw(self._surface, self._scale)


        if self.__board.isBoardEmpty():
            print("WIN")
            exit()

        screen.blit(self._surface, (0, 0))
        # self._surface.blit(screen)




