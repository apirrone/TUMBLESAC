import pygame
from scenes.menuScene import MenuScene, Button

class OnlineMenuScene(MenuScene):
    def __init__(self, w, h, scale):
        super().__init__(w, h, scale)

        self._buttons.append(Button("Join", (1, 1), 5, 2, self._scale, "join_game"))
        self._buttons.append(Button("Host", (1, 6), 5, 2, self._scale, "host_game"))
        self._buttons[0].setHighlighted(True)

    def input(self):
        events, action = super().input()

        if action == "esc":
            action = "go_to_title_scene"

        return events, action

    def update(self, dt):
        super().update(dt)

    def draw(self, screen):
        super().draw()
        screen.blit(self._surface, (0, 0))