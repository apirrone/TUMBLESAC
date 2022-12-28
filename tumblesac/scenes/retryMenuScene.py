from tumblesac.scenes.menuScene import MenuScene, Button


class RetryMenuScene(MenuScene):
    def __init__(self, w, h, scale, title, network):
        super().__init__(w, h, scale)

        self.__title = title
        self._buttons.append(
            Button("Retry", (1, 1), 5, 2, self._scale, "retry_infinite_mode")
        )
        self._buttons.append(
            Button("Exit", (1, 6), 5, 2, self._scale, "go_to_title_scene")
        )

        self.__network = network

    def input(self):
        events, action = super().input()

        if action == "esc":
            action = "go_to_title_scene"

        return events, action

    def update(self, dt):
        super().update(dt)

    def draw(self, screen):
        super().draw()

        label = self._font.render(self.__title, 1, (0, 0, 0))
        self._surface.blit(label, (8 * self._scale, 7 * self._scale))

        label = self._font.render(
            "Score : " + str(self.__network.getLastScore()), 1, (0, 0, 0)
        )
        self._surface.blit(label, (8 * self._scale, 8 * self._scale))
        if self.__network.isUpdating():
            label = self._font.render("Updating highscores ...", 1, (0, 0, 0))
            self._surface.blit(label, (8 * self._scale, 10 * self._scale))
        else:
            label = self._font.render("Done updating !", 1, (0, 0, 0))
            self._surface.blit(label, (8 * self._scale, 10 * self._scale))

        screen.blit(self._surface, (0, 0))
