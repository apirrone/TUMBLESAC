import pygame
from scenes.menuScene import MenuScene, Item
import json
class PlayersTable():
    def __init__(self, pos, scale):
        self.__pos     = pos
        self.__scale   = scale
        self.__players = []
        self.__font    = pygame.font.SysFont(None, self.__scale)

    def addPlayer(self, name):
        self.__players.append(name)

    def draw(self, surface):
        for i, player in enumerate(self.__players):
            pygame.draw.rect(surface, (0, 0, 0), (self.__pos[0]*self.__scale, (i+self.__pos[1])*self.__scale, 10*self.__scale, self.__scale), 3)
            label = self.__font.render(player, 1, (0, 0, 0))

            surface.blit(label, (self.__pos[0]*self.__scale, (i+self.__pos[1])*self.__scale))


class LobbyScene(MenuScene):
    def __init__(self, w, h, scale):
        super().__init__(w, h, scale)

        self._items.append(Item("Start", (1, 12), 5, 2, self._scale, "start_game"))
        self._items[0].setHighlighted(True)

        self.__cfg = json.load(open("online.cfg"))
        self.__myName = self.__cfg["name"]

        self.__playersTable = PlayersTable((1, 1), self._scale)
        self.__playersTable.addPlayer(self.__myName)

    def input(self):
        events, action = super().input()

        if action == "esc":
            action = "go_to_online_scene"

        return events, action

    def update(self, dt):
        super().update(dt)


    def draw(self, screen):
        super().draw(screen)

        self.__playersTable.draw(self._surface)

        screen.blit(self._surface, (0, 0))