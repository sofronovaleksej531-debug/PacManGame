import pygame
import random
from settings import *

class Ghost:
    def __init__(self, x, y, color, scatter_target):
        self.x = x * CELL_SIZE
        self.y = y * CELL_SIZE
        self.start_x = x * CELL_SIZE
        self.start_y = y * CELL_SIZE
        self.color = color
        self.direction = 0
        self.speed = GHOST_SPEED
        self.scatter_target = scatter_target
        self.mode = 'scatter'
        self.mode_timer = 0
        self.frightened = False
        self.frightened_timer = 0
    
    def update(self, maze, pacman_pos):
        if self.frightened:
            self.frightened_timer -= 1
            if self.frightened_timer <= 0:
                self.frightened = False
        
        self.mode_timer -= 1
        if self.mode_timer <= 0:
            if self.mode == 'scatter':
                self.mode = 'chase'
                self.mode_timer = 2000
            else:
                self.mode = 'scatter'
                self.mode_timer = 700
        
        self.move(maze, pacman_pos)
    
    def move(self, maze, pacman_pos):
        grid_x = int(self.x // CELL_SIZE)
        grid_y = int(self.y // CELL_SIZE)
        
        directions = [0, 90, 180, 270]
        opposite = {0: 180, 180: 0, 90: 270, 270: 90}
        
        if self.direction in directions:
            directions.remove(opposite[self.direction])
        
        if self.frightened:
            random.shuffle(directions)
            best_dir = directions[0]
        else:
            if self.mode == 'scatter':
                best_dir = self.get_best_direction(directions, maze, grid_x, grid_y, self.scatter_target)
            else:
                best_dir = self.get_best_direction(directions, maze, grid_x, grid_y, pacman_pos)
        
        self.direction = best_dir
        self.update_position()
    
    def get_best_direction(self, directions, maze, grid_x, grid_y, target):
        best_dir = directions[0]
        best_dist = float('inf')
        
        for dir in directions:
            new_x = grid_x
            new_y = grid_y
            if dir == 0:
                new_x += 1
            elif dir == 180:
                new_x -= 1
            elif dir == 90:
                new_y -= 1
            elif dir == 270:
                new_y += 1
            
            if not maze.is_wall(new_x * CELL_SIZE + 15, new_y * CELL_SIZE + 15):
                dist = abs(new_x - target[0]) + abs(new_y - target[1])
                if dist < best_dist:
                    best_dist = dist
                    best_dir = dir
        
        return best_dir
    
    def update_position(self):
        if self.direction == 0:
            self.x += self.speed
        elif self.direction == 180:
            self.x -= self.speed
        elif self.direction == 90:
            self.y -= self.speed
        elif self.direction == 270:
            self.y += self.speed
        
        self.x = max(CELL_SIZE, min(self.x, (MAZE_WIDTH - 1) * CELL_SIZE))
        self.y = max(CELL_SIZE, min(self.y, (MAZE_HEIGHT - 1) * CELL_SIZE))
    
    def reset_position(self):
        self.x = self.start_x
        self.y = self.start_y
        self.direction = 0
        self.frightened = False
    
    def make_frightened(self):
        self.frightened = True
        self.frightened_timer = FRIGHTENED_DURATION
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, CELL_SIZE, CELL_SIZE)
    
    def draw(self, screen):
        center = (int(self.x + CELL_SIZE // 2), int(self.y + CELL_SIZE // 2))
        radius = CELL_SIZE // 2 - 2
        
        if self.frightened:
            color = BLUE
        else:
            color = self.color
        
        pygame.draw.circle(screen, color, center, radius)
        
        eye_radius = 3
        eye_offset = 6
        eye1 = (center[0] - 4, center[1] - 3)
        eye2 = (center[0] + 4, center[1] - 3)
        
        pygame.draw.circle(screen, WHITE, eye1, eye_radius)
        pygame.draw.circle(screen, WHITE, eye2, eye_radius)
        pygame.draw.circle(screen, BLACK, (eye1[0] - 1, eye1[1] - 1), 2)
        pygame.draw.circle(screen, BLACK, (eye2[0] - 1, eye2[1] - 1), 2)
        
        if self.direction == 0:
            pygame.draw.rect(screen, color, (center[0] - 10, center[1] + 5, 20, 8))
        elif self.direction == 180:
            pygame.draw.rect(screen, color, (center[0] - 10, center[1] + 5, 20, 8))
        elif self.direction == 90:
            pygame.draw.rect(screen, color, (center[0] - 8, center[1] + 2, 16, 12))
        else:
            pygame.draw.rect(screen, color, (center[0] - 8, center[1] + 2, 16, 12))