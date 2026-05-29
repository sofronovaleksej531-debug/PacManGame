import pygame
from settings import *

class Maze:
    def __init__(self):
        self.layout = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,1],
            [1,2,1,1,1,2,1,1,2,1,1,2,1,1,2,1,1,1,2,1],
            [1,2,1,1,1,2,1,1,2,1,1,2,1,1,2,1,1,1,2,1],
            [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
            [1,2,1,1,1,2,1,2,1,1,1,1,2,1,2,1,1,1,2,1],
            [1,2,2,2,2,2,1,2,2,1,1,2,2,1,2,2,2,2,2,1],
            [1,1,1,1,1,2,1,1,1,1,1,1,1,1,2,1,1,1,1,1],
            [0,0,0,0,1,2,1,1,1,1,1,1,1,1,2,1,0,0,0,0],
            [1,1,1,1,1,2,1,1,1,1,1,1,1,1,2,1,1,1,1,1],
            [1,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,1],
            [1,2,1,1,1,2,1,1,2,1,1,2,1,1,2,1,1,1,2,1],
            [1,2,2,2,1,2,2,2,2,2,2,2,2,2,2,1,2,2,2,1],
            [1,1,2,2,1,2,1,2,1,1,1,1,2,1,2,1,2,2,1,1],
            [0,0,2,2,1,2,1,2,1,1,1,1,2,1,2,1,2,2,0,0],
            [1,1,2,2,1,2,1,2,2,2,2,2,2,1,2,1,2,2,1,1],
            [1,2,2,2,2,2,1,1,1,1,1,1,1,1,2,2,2,2,2,1],
            [1,2,1,1,1,2,1,1,1,1,1,1,1,1,2,1,1,1,2,1],
            [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ]
        self.width = MAZE_WIDTH
        self.height = MAZE_HEIGHT
        self.dots = []
        self.power_pellets = []
        self.load_dots()

    def load_dots(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.layout[y][x] == 2:
                    self.dots.append((x, y))
                elif self.layout[y][x] == 3:
                    self.power_pellets.append((x, y))
    
    def draw(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                if self.layout[y][x] == 1:
                    pygame.draw.rect(screen, BLUE, 
                                     (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                elif self.layout[y][x] == 2:
                    pygame.draw.circle(screen, WHITE, 
                                     (x * CELL_SIZE + CELL_SIZE//2, y * CELL_SIZE + CELL_SIZE//2), 3)
                elif self.layout[y][x] == 3:
                    pygame.draw.circle(screen, WHITE,
                                       (x * CELL_SIZE + CELL_SIZE//2, y * CELL_SIZE + CELL_SIZE//2), 10)
    def is_wall(self, x, y):
        grid_x = int(x // CELL_SIZE)
        grid_y = int(y // CELL_SIZE)
        if 0 <= grid_x < self.width and 0 <= grid_y < self.height:
            return self.layout[grid_y][grid_x] == 1
        return True
    
    def eat_dot(self, x, y):
        grid_x = int(x // CELL_SIZE)
        grid_y = int(y // CELL_SIZE)
        pos = (grid_x, grid_y)
        if pos in self.dots:
            self.dots.remove(pos)
            self.layout[grid_y][grid_x] = 0
            return 50
        return 0
    
    def get_remaining_dots(self):
        return len(self.dots) + len(self.power_pellets)