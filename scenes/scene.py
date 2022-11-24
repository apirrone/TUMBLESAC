import pygame

class Scene:
    def __init__(self, w, h, scale):
        self._w                = w
        self._h                = h
        self._surface          = pygame.Surface((self._w, self._h))
        self._background_color = (255, 255, 255)
        self._scale            = scale
        self._font             = pygame.font.SysFont(None, self._scale)
        self._t                = 0
        self._dt               = 0

    def input(self):
        action = None
        events =  pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                action = "exit_game"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:            
                    action = "esc"

        return events, action

    def update(self, dt):
        self._dt = dt
        self._t += dt

    def draw(self):
        self._surface.fill(self._background_color)
