import pygame
import numpy as np


class SmokeItem:
    def __init__(self, pos, speed, size, life_span):
        self._pos = np.array(pos)
        self._speed = np.array(speed)
        self._size = size
        self._life_span = life_span
        color = np.random.randint(100, 255)
        self._color = (color, color, color)

    def update(self, dt):
        self._pos = self._pos + self._speed * dt * 500
        self._life_span -= dt

    def draw(self, surface):
        if self._life_span > 0:
            pygame.draw.circle(surface, self._color, self._pos, self._size)
        # surface.blit(self._surface, (0, 0))


class ExplisionAnimation:
    def __init__(self, pos):
        self._pos = pos
        self._playing = False
        self._smoke = []
        self._done = False
        self._t = 0

    def update(self, dt):

        if self._done:
            return

        if not self._playing:
            self._playing = True
            for i in range(300):
                angle = np.random.random() * np.pi * 2

                self._smoke.append(
                    SmokeItem(
                        self._pos,
                        [
                            np.cos(angle) * np.random.random(),
                            np.sin(angle) * np.random.random(),
                        ],
                        np.random.uniform(20, 50),
                        np.random.random() * 2,
                    )
                )
        else:
            self._t += dt
            for smokeItem in self._smoke:
                smokeItem.update(dt)
            if self._t > 5:
                self._done = True

    def draw(self, surface):
        if self._done:
            return

        for smokeItem in self._smoke:
            smokeItem.draw(surface)

    # def play(self):
    #     self._playing = True

    def set_pos(self, pos):
        self._pos = pos
