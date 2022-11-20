import pygame
from scenes.gameScene import GameScene
from scenes.titleMenuScene import TitleMenuScene
from scenes.onlineMenuScene import OnlineMenuScene
from scenes.lobbyScene import LobbyScene

window_size=(1600, 1000)
FULLSCREEN = False

pygame.init()
clock = pygame.time.Clock()

# fullscreen, resizing, resolutions https://www.youtube.com/watch?v=edJZOQwrMKw
if not FULLSCREEN:
    screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)
else:
    # https://stackoverflow.com/questions/51243222/how-can-i-change-the-resolution-of-my-screen-in-pygame
    screen = pygame.display.set_mode(window_size, pygame.FULLSCREEN)
    window_size = screen.get_size()

font = pygame.font.SysFont(None, 20)

titleMenuScene = TitleMenuScene(window_size[0], window_size[1], 55)
gameScene = GameScene(window_size[0], window_size[1], 55)
onlineMenuScene = OnlineMenuScene(window_size[0], window_size[1], 55)
lobbyScene = LobbyScene(window_size[0], window_size[1], 55)

# current_scene = titleMenuScene
current_scene = lobbyScene

dt = clock.tick() # is this really dt ?
running = True
while running:
    _, action = current_scene.input()

    if action == "exit_game" : 
        running = False
    elif action == "go_to_play_scene":
        current_scene = gameScene
    elif action == "go_to_title_scene":
        current_scene = titleMenuScene
    elif action == "go_to_online_scene":
        current_scene = onlineMenuScene
    elif action == "join_game":
        # TODO start server
        current_scene = lobbyScene
    elif action == "host_game":
        current_scene = lobbyScene

    current_scene.update(dt)
    current_scene.draw(screen)

    pygame.display.flip()
    dt = clock.tick()