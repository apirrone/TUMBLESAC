import pygame
from tumblesac.scenes.scene import Scene


class Button:
    def __init__(self, text, pos, w, h, scale, action, enabled=True):
        self._text = text
        self._pos = pos
        self._w = w
        self._h = h
        self._scale = scale
        self._font = pygame.font.SysFont(None, self._scale)
        self._highlighted = False
        self._action = action
        self._enabled = enabled

    def draw(self, surface):
        if self._highlighted:
            pygame.draw.rect(
                surface,
                (255, 0, 0),
                (
                    self._pos[0] * self._scale,
                    self._pos[1] * self._scale,
                    self._w * self._scale,
                    self._h * self._scale,
                ),
            )
        else:
            pygame.draw.rect(
                surface,
                (0, 0, 0),
                (
                    self._pos[0] * self._scale,
                    self._pos[1] * self._scale,
                    self._w * self._scale,
                    self._h * self._scale,
                ),
                3,
            )

        label = self._font.render(
            self._text, 1, (0, 0, 0) if self._enabled else (128, 128, 128)
        )

        surface.blit(label, (self._pos[0] * self._scale, self._pos[1] * self._scale))

    def setHighlighted(self, highlighted):
        self._highlighted = highlighted

    def getHighlighted(self):
        return self._highlighted

    def getAction(self):
        if self._enabled:
            return self._action
        else:
            return None

    def getState(self):
        return True

    def disable(self):
        self._enabled = False

    def enable(self):
        self._enabled = True

    def isEnabled(self):
        return self._enabled

    def toggle(self):
        pass


class ToggleButton(Button):
    def __init__(
        self,
        textTrue,
        textFalse,
        pos,
        w,
        h,
        scale,
        action_state_true,
        action_state_false,
        state=False,
        enabled=True,
    ):
        super().__init__(
            textTrue if state else textFalse,
            pos,
            w,
            h,
            scale,
            action_state_true,
            enabled=enabled,
        )
        self.__textTrue = textTrue
        self.__textFalse = textFalse
        self.__state = state
        self.__action_state_true = action_state_true
        self.__action_state_false = action_state_false

    def draw(self, surface):
        super().draw(surface)

        if self.__state:
            pygame.draw.rect(
                surface,
                (0, 0, 255),
                (
                    self._pos[0] * self._scale,
                    self._pos[1] * self._scale,
                    self._w * self._scale,
                    self._h * self._scale,
                ),
                3,
            )

    def setHighlighted(self, highlighted):
        super().setHighlighted(highlighted)

    def getHighlighted(self):
        super().getHighlighted()

    def getAction(self):
        if self._enabled:
            return (
                self.__action_state_true if self.__state else self.__action_state_false
            )
        else:
            return None

    def getState(self):
        return self.__state

    def toggle(self):
        if self._enabled:
            self.__state = not self.__state
            self._text = self.__textTrue if self.__state else self.__textFalse


class MenuScene(Scene):
    def __init__(self, w, h, scale):
        super().__init__(w, h, scale)

        self._buttons = []
        self._currentButton = 0
        self._mutuallyExclusiveToggleButtons = []

    def input(self):
        events, action = super().input()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self._currentButton = min(
                        self._currentButton + 1, len(self._buttons) - 1
                    )
                elif event.key == pygame.K_UP:
                    self._currentButton = max(self._currentButton - 1, 0)
                elif event.key == pygame.K_RETURN:
                    self._buttons[self._currentButton].toggle()
                    action = self._buttons[self._currentButton].getAction()
                    self.applyMutuallyExclusiveness()

        return events, action

    def update(self, dt):
        super().update(dt)

        for i, button in enumerate(self._buttons):
            if self._currentButton == i:
                button.setHighlighted(True)
            else:
                button.setHighlighted(False)

    def draw(self):
        super().draw()
        for button in self._buttons:
            button.draw(self._surface)

        self._surface.blit(self._surface, (0, 0))

    # ids of buttons in list
    # for example, if ids 0 and 1 are mutually exclusive, if 0 is toggled,
    #   1 will be disabled and vice versa
    # if both are untoggled, both are enabled
    def addMutuallyExclusiveToggleButtonsPair(self, pair):
        if pair[0] < len(self._buttons) and pair[1] < len(self._buttons):
            self._mutuallyExclusiveToggleButtons.append(pair)
        else:
            print(
                "ERROR: invalid button id(s) for mutually exclusive toggle buttons pair"
            )

    def applyMutuallyExclusiveness(self):
        for pair in self._mutuallyExclusiveToggleButtons:
            b1 = self._buttons[pair[0]]
            b2 = self._buttons[pair[1]]

            if not b1.getState() and not b2.getState():
                b1.enable()
                b2.enable()
            elif b1.getState():
                b1.enable()
                b2.disable()
            else:
                b1.disable()
                b2.enable()
