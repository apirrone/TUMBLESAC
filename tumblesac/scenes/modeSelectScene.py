from tumblesac.scenes.menuScene import MenuScene, Button


class ModeSelectScene(MenuScene):
    def __init__(self, w, h, scale):
        super().__init__(w, h, scale)

        self._buttons.append(
            Button("Normal", (1, 1), 5, 2, self._scale, "go_to_play_scene")
        )
        self._buttons.append(
            Button("Infinite", (1, 6), 5, 2, self._scale, "infinite_game")
        )
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
