import pygame

class Character:
    def __init__(self, color, grid_size, board_pos):
        self.__color     = color
        self.__grid_w    = grid_size[0]
        self.__grid_h    = grid_size[1]
        self.__board_pos = board_pos
        self.__j_pos     = self.__grid_w//2

    def getJPos(self):
        return self.__j_pos

    def move(self, dir):
        self.__j_pos = min(max(0, self.__j_pos + dir), self.__grid_w-1)

    def draw(self, surface, scale):
        pygame.draw.rect(surface, self.__color, ((self.__board_pos[1]+self.__j_pos)*scale, (self.__grid_h+self.__board_pos[1])*scale,  scale, scale)) 
