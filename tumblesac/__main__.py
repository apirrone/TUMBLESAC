import pygame
from tumblesac.scenes.gameScene import GameScene
from tumblesac.scenes.titleMenuScene import TitleMenuScene
from tumblesac.scenes.onlineMenuScene import OnlineMenuScene
from tumblesac.scenes.lobbyScene import LobbyScene
from tumblesac.scenes.modeSelectScene import ModeSelectScene
from tumblesac.scenes.retryMenuScene import RetryMenuScene
from tumblesac.network import Network
import json
import os
import subprocess
import signal


def main():
    window_size = (1000, 1000)
    FULLSCREEN = False

    pygame.init()
    pygame.display.set_caption("TUMBLESAC")

    clock = pygame.time.Clock()

    # fullscreen, resizing, resolutions https://www.youtube.com/watch?v=edJZOQwrMKw
    if not FULLSCREEN:
        screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)
    else:
        # https://stackoverflow.com/questions/51243222/how-can-i-change-the-resolution-of-my-screen-in-pygame
        screen = pygame.display.set_mode(window_size, pygame.FULLSCREEN)
        window_size = screen.get_size()

    package_root_dir = os.path.dirname(os.path.dirname(__file__))
    cfg = json.load(open(os.path.join(package_root_dir, "config", "online.cfg")))
    network = Network(cfg["ip"], cfg["port"], cfg["name"])

    titleMenuScene = TitleMenuScene(window_size[0], window_size[1], 55, "TUMBLESAC")
    titleMenuScene.updateHighScores(network.getNHighestScores())
    onlineMenuScene = OnlineMenuScene(window_size[0], window_size[1], 55, cfg["port"])
    retryMenuScene = RetryMenuScene(
        window_size[0], window_size[1], 55, "Infinite mode", network
    )
    gameScene = None  # GameScene(window_size[0], window_size[1], 55)
    lobbyScene = None

    current_scene = titleMenuScene

    host_subprocess = None

    dt = clock.tick(165)/1000.  # is this really dt ?
    running = True
    while running:
        _, action = current_scene.input()

        if action == "exit_game":
            running = False
        elif action == "go_to_mode_select_scene":
            modeSelectScene = ModeSelectScene(window_size[0], window_size[1], 55)
            current_scene = modeSelectScene
        elif action == "go_to_play_scene":
            gameScene = GameScene(window_size[0], window_size[1], 55)
            current_scene = gameScene
        elif action == "infinite_game":
            gameScene = GameScene(window_size[0], window_size[1], 55, infinite=True)
            current_scene = gameScene
        elif action == "go_to_retry_scene":
            network.updateHighScores(gameScene.getScore())
            titleMenuScene.updateHighScores(network.getNHighestScores())
            current_scene = retryMenuScene
        elif action == "retry_infinite_mode":
            gameScene = GameScene(window_size[0], window_size[1], 55, infinite=True)
            current_scene = gameScene
        elif action == "go_to_title_scene":
            current_scene = titleMenuScene
        elif action == "go_to_online_scene":
            current_scene = onlineMenuScene
            network.disconnect()
        elif action == "join_game":
            lobbyScene = LobbyScene(window_size[0], window_size[1], 55, network)
            current_scene = lobbyScene
        elif action == "hosting":
            print("START HOSTING")
            print("Running server in background ...")
            host_subprocess = subprocess.Popen(["tumblesac_server"])
        elif action == "not_hosting":
            os.kill(host_subprocess.pid, signal.SIGTERM)
            host_subprocess = None
            print("STOP NOT_HOSTING")
        elif action == "start_game":
            print("start game")
            gameScene = GameScene(window_size[0], window_size[1], 55, network)
            current_scene = gameScene

        current_scene.update(dt)
        if gameScene is not None:
            game_over, winner = network.isGameOver()

            if game_over:
                print("WINNER : ", winner)
                lobbyScene.reset(winner)
                gameScene = None
                network.reset()
                current_scene = lobbyScene

        current_scene.draw(screen)

        pygame.display.flip()
        dt = clock.tick(165)/1000.

    network.disconnect()
    if host_subprocess is not None:
        os.kill(host_subprocess.pid, signal.SIGTERM)


if __name__ == "__main__":
    main()
