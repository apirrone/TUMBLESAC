from tumblesac.scenes.menuScene import MenuScene, Button
import pickle
import os


class TitleMenuScene(MenuScene):
    def __init__(self, w, h, scale, title):
        super().__init__(w, h, scale)

        package_root_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), '../')

        self.__highscoreFilePath = os.path.join(package_root_dir, "config", "highscore.pckl")

        self.__title = title

        self._buttons.append(
            Button("Play", (1, 1), 5, 2, self._scale, "go_to_mode_select_scene")
        )
        self._buttons.append(
            Button("Online", (1, 6), 5, 2, self._scale, "go_to_online_scene")
        )
        self._buttons.append(Button("Exit", (1, 11), 5, 2, self._scale, "exit_game"))
        self._buttons[0].setHighlighted(True)

        if not os.path.exists(self.__highscoreFilePath):
            f = open(self.__highscoreFilePath, "wb")
            pickle.dump({"highscore": 0}, f)
            f.close()

        self.__highscore = pickle.load(open(self.__highscoreFilePath, "rb"))["highscore"]

    def input(self):
        events, action = super().input()

        if action == "esc":
            action = "exit_game"

        return events, action

    def update(self, dt):
        super().update(dt)

    def updateHighScore(self, score):
        if score > self.__highscore:
            self.__highscore = score
            f = open(self.__highscoreFilePath, "wb")
            pickle.dump({"highscore": score}, f)
            f.close()

    def draw(self, screen):
        super().draw()

        label = self._font.render(self.__title, 1, (0, 0, 0))
        self._surface.blit(label, (10 * self._scale, 7 * self._scale))

        label = self._font.render(
            "Infinite mode high score : " + str(self.__highscore), 1, (0, 0, 0)
        )
        self._surface.blit(label, (7 * self._scale, 10 * self._scale))

        screen.blit(self._surface, (0, 0))
