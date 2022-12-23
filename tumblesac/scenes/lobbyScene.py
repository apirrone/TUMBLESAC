import pygame
from tumblesac.scenes.menuScene import MenuScene, Button, ToggleButton
import json
import os
import numpy as np


class PlayersTable:
    def __init__(self, pos, scale):
        self.__pos = pos
        self.__scale = scale
        self.__players = {}
        self.__font = pygame.font.SysFont(None, self.__scale)

    def clear(self):
        self.__players = {}

    def addPlayer(self, id, name, score, ready):
        self.__players[id] = {
            "name": name,
            "score": score,
            "ready": " - ready" if ready else "",
        }

    def draw(self, surface):
        for i, id in enumerate(self.__players.keys()):
            name = self.__players[id]["name"]
            score = self.__players[id]["score"]
            ready = self.__players[id]["ready"]
            pygame.draw.rect(
                surface,
                (0, 0, 0),
                (
                    self.__pos[0] * self.__scale,
                    (i + self.__pos[1]) * self.__scale,
                    10 * self.__scale,
                    self.__scale,
                ),
                3,
            )
            txt = name + " - " + str(score) + ready
            label = self.__font.render(txt, 1, (0, 0, 0))

            surface.blit(
                label,
                (self.__pos[0] * self.__scale, (i + self.__pos[1]) * self.__scale + 10),
            )


class LobbyScene(MenuScene):
    def __init__(self, w, h, scale, network):
        super().__init__(w, h, scale)

        package_root_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), '../')

        self.__onlineFilePath = os.path.join(package_root_dir, "config", "online.cfg")

        self._buttons.append(
            ToggleButton("Ready", (1, 12), 5, 2, self._scale, "ready", "not_ready")
        )
        self._buttons.append(Button("Start", (1, 15), 5, 2, self._scale, "start_game"))
        self._buttons[0].setHighlighted(True)

        self.__cfg = json.load(open(self.__onlineFilePath))

        self.__playersTable = PlayersTable((1, 1), self._scale)

        self.__network = network

        self.__connexion_status = self.__network.start()

        self.__last_winner = ""

        self.__taunts = [
            "Quel énorme sac à merde !",
            "Le plus gros des sacs !",
            "Jamais vu un tas de merde aussi haut",
            "rEgaRDez mOI j'Ai GAgNé GneuGneu",
            "Sac un jour, sac toujours",
            "Au SACours ...",
            "Il a triché ce gros sac",
        ]
        self.__current_taunt = np.random.choice(self.__taunts)

    def input(self):
        events, action = super().input()

        if action == "esc":
            action = "go_to_online_scene"

        if self.__connexion_status:
            if action == "ready":
                self.__network.sendReady(True)
            if action == "not_ready":
                self.__network.sendReady(False)

            if action == "start_game":
                self.__network.sendStartGame()
                action = ""

            if self.__network.isGameStarted():
                action = "start_game"

        return events, action

    def reset(self, winner=""):
        self._buttons[0].toggle()
        self.__last_winner = winner
        self.__current_taunt = np.random.choice(self.__taunts)

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
            # id = player["id"]
            name = player["name"]
            score = player["score"]
            ready = player["ready"]
            self.__playersTable.addPlayer(id, name, score, ready)

    def draw(self, screen):
        super().draw()

        self.__playersTable.draw(self._surface)
        if self.__connexion_status:
            msg = "connected"
        else:
            msg = "not connected"

        label = pygame.font.SysFont(None, self._scale).render(msg, 1, (0, 0, 0))

        self._surface.blit(label, (0, 0))

        if self.__last_winner != "":
            label = pygame.font.SysFont(None, self._scale).render(
                "Last winner : " + str(self.__last_winner), 1, (0, 0, 0)
            )
            self._surface.blit(label, (6.5 * self._scale, 16 * self._scale))

            label = pygame.font.SysFont(None, self._scale // 2).render(
                self.__current_taunt, 1, (0, 0, 0)
            )
            self._surface.blit(label, (6.5 * self._scale, 17 * self._scale))

        screen.blit(self._surface, (0, 0))
