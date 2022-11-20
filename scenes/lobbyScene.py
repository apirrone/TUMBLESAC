import pygame
from scenes.menuScene import MenuScene, Item
import json
import sys
sys.path.append("../")
from network import Network
class PlayersTable():
    def __init__(self, pos, scale):
        self.__pos     = pos
        self.__scale   = scale
        self.__players = []
        self.__font    = pygame.font.SysFont(None, self.__scale)

    def clear(self):
        self.__players = []

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

        self.__network = Network(self.__cfg["ip"], self.__cfg["port"], self.__myName)

        self.__connexion_status = self.__network.start()
        self.__game_started = False

    def input(self):
        events, action = super().input()

        if action == "esc":
            action = "go_to_online_scene"

        if action == "start_game":
            print("STARTING")
            self.__network.sendStartGame()

        if self.__game_started:
            action = "start_game"

        return events, action

    def getNetwork(self):
        return self.__network

    def update(self, dt):
        super().update(dt)
        if not self.__connexion_status:
            self.__connexion_status = self.__network.start()
            return

        self.__network.getUpdate()

        # TODO do better, this is so bad
        self.__playersTable.clear()
        for id, player in self.__network.getPlayers().items():
            name = player["name"]
            self.__playersTable.addPlayer(name)

        self.__game_started = self.__network.isGameStarted()


    def draw(self, screen):
        super().draw(screen)

        self.__playersTable.draw(self._surface)
        if self.__connexion_status:
            msg = "connected"
        else:
            msg = "not connected"

        label = pygame.font.SysFont(None, self._scale).render(msg, 1, (0, 0, 0))

        self._surface.blit(label, (0, 0))

        screen.blit(self._surface, (0, 0))