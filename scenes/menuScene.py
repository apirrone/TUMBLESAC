import pygame
from scenes.scene import Scene

class Button:
    def __init__(self, text, pos, w, h, scale, action):
        self._text        = text
        self._pos         = pos
        self._w           = w
        self._h           = h
        self._scale       = scale
        self._font        = pygame.font.SysFont(None, self._scale)
        self._highlighted = False
        self._action      = action

    def draw(self, surface):
        if self._highlighted:
            pygame.draw.rect(surface, (255, 0, 0), (self._pos[0]*self._scale, self._pos[1]*self._scale, self._w*self._scale, self._h*self._scale))
        else:
            pygame.draw.rect(surface, (0, 0, 0), (self._pos[0]*self._scale, self._pos[1]*self._scale, self._w*self._scale, self._h*self._scale), 3)

        label = self._font.render(self._text, 1, (0, 0, 0))

        surface.blit(label, (self._pos[0]*self._scale, self._pos[1]*self._scale))

    def setHighlighted(self, highlighted):
        self._highlighted = highlighted

    def getHighlighted(self):
        return self._highlighted

    def getAction(self):
        return self._action

    def toggle(self):
        pass

class ToggleButton(Button):
    def __init__(self, text, pos, w, h, scale, action_state_true, action_state_false, state=False):
        super().__init__(text, pos, w, h, scale, action_state_true)

        self.__state = state
        self.__action_state_true = action_state_true
        self.__action_state_false = action_state_false

    def draw(self, surface):
        super().draw(surface)

        if self.__state:
            pygame.draw.rect(surface, (0, 0, 255), (self._pos[0]*self._scale, self._pos[1]*self._scale, self._w*self._scale, self._h*self._scale), 3)

    def setHighlighted(self, highlighted):
        super().setHighlighted(highlighted)

    def getHighlighted(self):
        super().getHighlighted()

    def getAction(self):
        if self.__state:
            return self.__action_state_true
        else:
            return self.__action_state_false

    def toggle(self):
        self.__state = not self.__state


class MenuScene(Scene):
    def __init__(self, w, h, scale):
        super().__init__(w, h, scale)

        self._buttons = []
        self._currentButton = 0

    def input(self):
        events, action = super().input()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self._currentButton = min(self._currentButton+1, len(self._buttons)-1)
                elif event.key == pygame.K_UP:
                    self._currentButton = max(self._currentButton-1, 0)
                elif event.key == pygame.K_RETURN:
                    self._buttons[self._currentButton].toggle()
                    action = self._buttons[self._currentButton].getAction()


        return events, action

    def update(self, dt):
        super().update(dt)

        for i, button in enumerate(self._buttons):
            if self._currentButton == i:
                button.setHighlighted(True)
            else:
                button.setHighlighted(False)


    def draw(self, screen):
        super().draw(screen)
        for button in self._buttons:
            button.draw(self._surface)

        screen.blit(self._surface, (0, 0))


