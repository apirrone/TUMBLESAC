from tumblesac.scenes.menuScene import MenuScene, Button, ToggleButton
from requests import get
import threading

class OnlineMenuScene(MenuScene):
    def __init__(self, w, h, scale, port):
        super().__init__(w, h, scale)

        self._buttons.append(Button("Join", (1, 1), 5, 2, self._scale, "join_game"))

        self._buttons.append(
            ToggleButton(
                "Stop hosting",
                "Start hosting",
                (1, 6),
                5,
                2,
                self._scale,
                "hosting",
                "not_hosting",
            )
        )
        self._buttons[0].setHighlighted(True)

        self.__port = port
        t = threading.Thread(target=self.acquireIp)
        t.start()
        # self.__ip = get("https://api.ipify.org").content.decode("utf8")

    def acquireIp(self):
        self.__ip = get("https://api.ipify.org").content.decode("utf8")

    def input(self):
        events, action = super().input()

        if action == "esc":
            action = "go_to_title_scene"

        return events, action

    def update(self, dt):
        super().update(dt)

    def draw(self, screen):
        super().draw()

        label = self._font.render(
            "Your ip : " + str(self.__ip) + ":" + str(self.__port), 1, (0, 0, 0)
        )
        self._surface.blit(label, (7 * self._scale, 7 * self._scale))

        screen.blit(self._surface, (0, 0))
