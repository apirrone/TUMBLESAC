from tumblesac.scenes.menuScene import MenuScene, Button
import pickle
import os


class TitleMenuScene(MenuScene):
    def __init__(self, w, h, scale, title):
        super().__init__(w, h, scale)

        self.__title = title

        self._buttons.append(
            Button("Play", (1, 1), 5, 2, self._scale, "go_to_mode_select_scene")
        )
        self._buttons.append(
            Button("Online", (1, 6), 5, 2, self._scale, "go_to_online_scene")
        )
        self._buttons.append(Button("Exit", (1, 11), 5, 2, self._scale, "exit_game"))
        self._buttons[0].setHighlighted(True)

        self.__highscores = None

    def input(self):
        events, action = super().input()

        if action == "esc":
            action = "exit_game"

        return events, action

    def update(self, dt):
        super().update(dt)

    def updateHighScores(self, scores):
        self.__highscores = scores

    def draw(self, screen):
        super().draw()

        label = self._font.render(self.__title, 1, (0, 0, 0))
        self._surface.blit(label, (10 * self._scale, 7 * self._scale))

        label = self._font.render("Infinite mode high scores : ", 1, (0, 0, 0))
        self._surface.blit(label, (7 * self._scale, 10 * self._scale))

        for i, score in enumerate(self.__highscores):
            label = self._font.render(str(score[0]) + " : " + str(score[1]), 1, (0, 0, 0))
            self._surface.blit(label, (7 * self._scale, (12 + i) * self._scale))

        screen.blit(self._surface, (0, 0))
