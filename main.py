import pygame
from board import Board
from character import Character

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

b = Board((2, 1))
b.populateBoard(300)

c = Character((50, 50, 50), b.getGridSize(), b.getPos())

font = pygame.font.SysFont(None, 20)
background_color = (255, 255, 255)
running = True
while running:
    screen.fill(background_color)

    events =  pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:            
                running = False
            elif event.key == pygame.K_LEFT:
                c.move(-1)
            elif event.key == pygame.K_RIGHT:
                c.move(1)
            elif event.key == pygame.K_SPACE:
                b.shoot(c.getJPos())

    b.draw(screen, 55)
    c.draw(screen, 55)
    b.highlightBlock(screen, 55 , c.getJPos())



    pygame.display.flip()
    dt = clock.tick()