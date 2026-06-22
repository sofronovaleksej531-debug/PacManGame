import pygame
from settings import *

class Maze:
    def __init__(self):
        self.layout = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,3,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,3,1],
            [1,2,1,1,1,2,1,1,2,1,1,2,1,1,2,1,1,1,2,1],
            [1,2,1,1,1,2,1,1,2,1,1,2,1,1,2,1,1,1,2,1],
            [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
            [1,2,1,1,1,2,1,2,1,1,1,1,2,1,2,1,1,1,2,1],
            [1,2,2,2,2,2,1,2,2,2,2,2,2,1,2,2,2,2,2,1],
            [1,1,1,1,1,2,1,1,1,1,1,1,1,1,2,1,1,1,1,1],
            [0,0,0,0,1,2,1,1,1,1,1,1,1,1,2,1,0,0,0,0],
            [1,1,1,1,1,2,4,4,4,4,4,4,4,4,2,1,1,1,1,1],
            [1,2,2,2,2,2,1,1,4,1,1,4,1,1,2,2,2,2,2,1],
            [1,2,1,1,1,2,1,1,4,1,1,4,1,1,2,1,1,1,2,1],
            [1,2,2,2,1,2,2,2,4,4,4,4,2,2,2,1,2,2,2,1],
            [1,2,2,2,1,2,1,2,1,1,1,1,2,1,2,1,2,2,2,1],
            [1,2,2,2,1,2,1,2,1,1,1,1,2,1,2,1,2,2,2,1],
            [1,2,2,2,1,2,1,2,2,2,2,2,2,1,2,1,2,2,2,1],
            [1,2,2,2,2,2,1,1,1,1,1,1,1,1,2,2,2,2,2,1],
            [1,2,1,1,1,2,1,1,1,1,1,1,1,1,2,1,1,1,2,1],
            [1,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ]
        
        for y in range(len(self.layout)):
            for x in range(len(self.layout[y])):
                if self.layout[y][x] == 0:
                    if (x == 8 or x == 11) and (y == 8 or y == 14):
                        self.layout[y][x] = 3
        
        self.width = MAZE_WIDTH
        self.height = MAZE_HEIGHT
        self.dots = []
        self.power_pellets = []
        self.ghost_door = (9, 9)
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
                                     (x * CELL_SIZE + CELL_SIZE//2, y * CELL_SIZE + CELL_SIZE//2),
                                     3)
                elif self.layout[y][x] == 3:
                    pygame.draw.circle(screen, WHITE,
                                     (x * CELL_SIZE + CELL_SIZE//2, y * CELL_SIZE + CELL_SIZE//2),
                                     7)
                elif self.layout[y][x] == 4:
                    pygame.draw.rect(screen, BLACK,
                                   (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    def is_wall(self, x, y):
        grid_x = int(x // CELL_SIZE)
        grid_y = int(y // CELL_SIZE)
        if 0 <= grid_y < self.height and 0 <= grid_x < self.width:
            return self.layout[grid_y][grid_x] == 1
        return True
    
    def is_ghost_door(self, x, y):
        grid_x = int(x // CELL_SIZE)
        grid_y = int(y // CELL_SIZE)
        return self.layout[grid_y][grid_x] == 4
    
    def can_ghost_pass(self, x, y):
        grid_x = int(x // CELL_SIZE)
        grid_y = int(y // CELL_SIZE)
        if 0 <= grid_y < self.height and 0 <= grid_x < self.width:
            return self.layout[grid_y][grid_x] != 1
        return False
    
    def eat_dot(self, x, y):
        grid_x = int(x // CELL_SIZE)
        grid_y = int(y // CELL_SIZE)
        if grid_y >= self.height or grid_x >= self.width:
            return 0
        pos = (grid_x, grid_y)
        if pos in self.dots:
            self.dots.remove(pos)
            self.layout[grid_y][grid_x] = 0
            return 10
        elif pos in self.power_pellets:
            self.power_pellets.remove(pos)
            self.layout[grid_y][grid_x] = 0
            return 50
        return 0
    
    def get_remaining_dots(self):
        return len(self.dots) + len(self.power_pellets)
    
    def get_ghost_spawn_points(self):
        return [(10, 9), (10, 10), (9, 10), (11, 10)]
    def is_wall(self, x, y):
        grid_x = int(x // CELL_SIZE)
        grid_y = int(y // CELL_SIZE)

        if grid_x < 0 or grid_x >= self.width or grid_y < 0 or grid_y >= self.height:
            return True
        if self.layout[grid_y][grid_x] == 4:
            return False
        
        return self.layout[grid_y][grid_x] == 1