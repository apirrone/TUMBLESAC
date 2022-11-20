import pygame
from scenes.scene import Scene

class Item:
    def __init__(self, text, pos, w, h, scale, action):
        self.__text        = text
        self.__pos         = pos
        self.__w           = w
        self.__h           = h
        self.__scale       = scale
        self.__font        = pygame.font.SysFont(None, self.__scale)
        self.__highlighted = False
        self.__action      = action

    def draw(self, surface):
        if self.__highlighted:
            pygame.draw.rect(surface, (255, 0, 0), (self.__pos[0]*self.__scale, self.__pos[1]*self.__scale, self.__w*self.__scale, self.__h*self.__scale))
        else:
            pygame.draw.rect(surface, (0, 0, 0), (self.__pos[0]*self.__scale, self.__pos[1]*self.__scale, self.__w*self.__scale, self.__h*self.__scale), 3)

        label = self.__font.render(self.__text, 1, (0, 0, 0))

        surface.blit(label, (self.__pos[0]*self.__scale, self.__pos[1]*self.__scale))

    def setHighlighted(self, highlighted):
        self.__highlighted = highlighted

    def getAction(self):
        return self.__action

class MenuScene(Scene):
    def __init__(self, w, h, scale):
        super().__init__(w, h, scale)

        self._items = []
        self._currentItem = 0

    def input(self):
        events, action = super().input()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self._currentItem = min(self._currentItem+1, len(self._items)-1)
                elif event.key == pygame.K_UP:
                    self._currentItem = max(self._currentItem-1, 0)
                elif event.key == pygame.K_RETURN:
                    action = self._items[self._currentItem].getAction()

        return events, action

    def update(self, dt):
        super().update(dt)

        for i, item in enumerate(self._items):
            if self._currentItem == i:
                item.setHighlighted(True)
            else:
                item.setHighlighted(False)


    def draw(self, screen):
        super().draw(screen)
        for item in self._items:
            item.draw(self._surface)

        screen.blit(self._surface, (0, 0))


