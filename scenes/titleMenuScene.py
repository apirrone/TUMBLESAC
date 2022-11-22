import pygame
from scenes.menuScene import MenuScene, Button

class TitleMenuScene(MenuScene):
    def __init__(self, w, h, scale):
        super().__init__(w, h, scale)

        self._buttons.append(Button("Play", (1, 1), 5, 2, self._scale, "go_to_play_scene"))
        self._buttons.append(Button("Online", (1, 6), 5, 2, self._scale, "go_to_online_scene"))
        self._buttons.append(Button("Exit", (1, 11), 5, 2, self._scale, "exit_game"))
        self._buttons[0].setHighlighted(True)

    def input(self):
        events, action = super().input()

        if action == "esc":
            action = "exit_game"

        return events, action

    def update(self, dt):
        super().update(dt)

    def draw(self, screen):
        super().draw(screen)