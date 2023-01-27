from tumblesac.scenes.menuScene import MenuScene, Button
import numpy as np
import os
import pygame
from pygame import mixer
from tumblesac.animations import ExplisionAnimation


class Logo:
    def __init__(self, pos, size):
        self._pos = pos
        self._size = np.array(size)
        self._speed = 0.01

        self._currentSize = np.array([1.0, 1.0])
        package_root_dir = os.path.dirname(os.path.dirname(__file__))
        self._im_orig = pygame.image.load(
            os.path.join(package_root_dir, "assets", "dr_antoijne_shitty_games.png")
        )
        self._im = self._im_orig.copy()
        self._t = 0
        self._incomingDone = False

        mixer.init()
        mixer.music.load(os.path.join(package_root_dir, "assets", "crappyantoijne.wav"))
        mixer.music.play()

        self._explosionAnimation = ExplisionAnimation([0, 0])

    def update(self, dt):
        self._t += dt

        if self._currentSize[0] < self._size[0] and not self._incomingDone:
            self._currentSize += [self._speed, self._speed]
            # self._speed += 2 * dt
            self._speed += 0.28 * dt
        else:
            self._incomingDone = True
            self._currentSize = self._size + np.sin(2 * np.pi * 1 * self._t) * 60
            self._explosionAnimation.set_pos(self._pos + self._size // 2)
            self._explosionAnimation.update(dt)

        self._im = pygame.transform.scale(self._im_orig, self._currentSize)
        self._im = pygame.transform.rotate(
            self._im, np.sin(2 * np.pi * 0.2 * self._t) * 10
        )

    def draw(self, surface):

        surface.blit(self._im, self._pos)
        self._explosionAnimation.draw(surface)

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

        self.__logo = Logo((w // 2, 0), (400, 400))
        self.__last_background_update = 0.2

    def input(self):
        events, action = super().input()

        if action == "esc":
            action = "exit_game"

        return events, action

    def update(self, dt):
        super().update(dt)

        self.__last_background_update -= dt
        self.__logo.update(dt)

    def updateHighScores(self, scores):
        self.__highscores = scores

    def draw(self, screen):
        super().draw()

        label = self._font.render(self.__title, 1, (0, 0, 0))
        self._surface.blit(label, (10 * self._scale, 7 * self._scale))

        label = self._font.render("Infinite mode high scores : ", 1, (0, 0, 0))
        self._surface.blit(label, (7 * self._scale, 10 * self._scale))
        if self.__highscores is None:
            label = self._font.render("Could not fetch high scores", 1, (0, 0, 0))
            self._surface.blit(label, (7 * self._scale, (12) * self._scale))

        else:
            for i, score in enumerate(self.__highscores):
                label = self._font.render(
                    str(score[0]) + " : " + str(score[1]), 1, (0, 0, 0)
                )
                self._surface.blit(label, (7 * self._scale, (12 + i) * self._scale))

        self.__logo.draw(self._surface)

        screen.blit(self._surface, (0, 0))
