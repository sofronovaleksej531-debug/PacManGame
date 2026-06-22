import pygame
import random
from settings import *

class Ghost:
    def __init__(self, x, y, color, scatter_target, spawn_order):
        self.x = x * CELL_SIZE + CELL_SIZE // 2
        self.y = y * CELL_SIZE + CELL_SIZE // 2
        self.start_x = self.x
        self.start_y = self.y
        self.color = color
        self.direction = random.choice([0, 90, 180, 270])
        self.speed = GHOST_SPEED
        self.scatter_target = scatter_target
        self.mode = 'scatter'
        self.mode_timer = 700
        self.frightened = False
        self.frightened_timer = 0
        self.spawn_order = spawn_order
        self.in_house = True
        self.spawn_timer = spawn_order * 300
        self.radius = CELL_SIZE // 2 - 2
        self.moving = True
        self.speed = GHOST_SPEED
    
    def update(self, maze, pacman_pos):
        if self.in_house:
            self.spawn_timer -= 1
            if self.spawn_timer <= 0:
                self.in_house = False
                self.x = 9 * CELL_SIZE + CELL_SIZE // 2
                self.y = 9 * CELL_SIZE + CELL_SIZE // 2
                self.direction = 0
        
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
        grid_x = round((self.x - CELL_SIZE // 2) / CELL_SIZE)
        grid_y = round((self.y - CELL_SIZE // 2) / CELL_SIZE)

        is_intersection = (self.x % CELL_SIZE == CELL_SIZE // 2 and 
                          self.y % CELL_SIZE == CELL_SIZE // 2)
        
        if is_intersection:
            possible_dirs = []
            for direction in [0, 180, 90, 270]:
                if direction == (self.direction + 180) % 360:
                    continue
                
                can_move = self.can_move_in_direction(maze, direction, grid_x, grid_y)
                if can_move:
                    possible_dirs.append(direction)
            
            if possible_dirs:
                if self.frightened:
                    self.direction = random.choice(possible_dirs)
                else:
                    if self.in_house:
                        target = (10, 9)
                    elif self.mode == 'scatter':
                        target = self.scatter_target
                    else:
                        target = pacman_pos
                    
                    self.direction = self.get_best_direction(possible_dirs, grid_x, grid_y, target)
        new_x = self.x
        new_y = self.y
        
        if self.direction == 0:
            new_x = self.x + self.speed
        elif self.direction == 180:
            new_x = self.x - self.speed
        elif self.direction == 90:
            new_y = self.y - self.speed
        elif self.direction == 270:
            new_y = self.y + self.speed
        
        if not self.check_collision(maze, new_x, new_y):
            self.x = new_x
            self.y = new_y
    
    def can_move_in_direction(self, maze, direction, grid_x, grid_y):
        if direction == 0:
            return maze.can_ghost_pass((grid_x + 1) * CELL_SIZE + CELL_SIZE // 2, 
                                      grid_y * CELL_SIZE + CELL_SIZE // 2)
        elif direction == 180:
            return maze.can_ghost_pass((grid_x - 1) * CELL_SIZE + CELL_SIZE // 2, 
                                      grid_y * CELL_SIZE + CELL_SIZE // 2)
        elif direction == 90:
            return maze.can_ghost_pass(grid_x * CELL_SIZE + CELL_SIZE // 2, 
                                      (grid_y - 1) * CELL_SIZE + CELL_SIZE // 2)
        elif direction == 270:
            return maze.can_ghost_pass(grid_x * CELL_SIZE + CELL_SIZE // 2, 
                                      (grid_y + 1) * CELL_SIZE + CELL_SIZE // 2)
        return False
    
    def check_collision(self, maze, x, y):
        points = [
            (x - self.radius + 2, y - self.radius + 2),
            (x + self.radius - 2, y - self.radius + 2),
            (x - self.radius + 2, y + self.radius - 2),
            (x + self.radius - 2, y + self.radius - 2)
        ]
        
        for px, py in points:
            if maze.is_wall(px, py):
                return True
        return False
    
    def get_best_direction(self, directions, grid_x, grid_y, target):
        best_dir = directions[0]
        best_dist = float('inf')
        
        for dir in directions:
            new_x = grid_x
            new_y = grid_y
            if dir == 0:
                new_x = grid_x + self.speed
            elif dir == 180:
                new_x = grid_x - self.speed
            elif dir == 90:
                new_y = grid_y - self.speed
            elif dir == 270:
                new_y = grid_y + self.speed
            
            if self.frightened:
                dist = abs(new_x - target[0]) + abs(new_y - target[1])
            else:
                dist = abs(new_x - target[0]) + abs(new_y - target[1])
            
            if dist < best_dist:
                best_dist = dist
                best_dir = dir
        
        return best_dir
    
    def reset_position(self):
        self.x = self.start_x
        self.y = self.start_y
        self.direction = random.choice([0, 90, 180, 270])
        self.frightened = False
        self.in_house = True
        self.spawn_timer = self.spawn_order * 300
    
    def make_frightened(self):
        self.frightened = True
        self.frightened_timer = FRIGHTENED_DURATION
    
    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)
    
    def draw(self, screen):
        center = (int(self.x), int(self.y))
        radius = self.radius
        
        if self.frightened:
            if self.frightened_timer < 150 and self.frightened_timer % 20 < 10:
                color = WHITE
            else:
                color = FRIGHTENED_BLUE
        else:
            color = self.color
        
        pygame.draw.circle(screen, color, center, radius)
        pygame.draw.rect(screen, color, 
                        (center[0] - radius, center[1], radius * 2, radius))
        
        for i in range(3):
            x = center[0] - radius + i * (radius * 2 // 3) + radius // 3
            y = center[1] + radius
            if i % 2 == 0:
                pygame.draw.circle(screen, color, (x, y + 2), radius // 3)
            else:
                pygame.draw.circle(screen, color, (x + 2, y - 2), radius // 3)

        eye_radius = 4
        pupil_radius = 2
        
        if self.direction == 0:
            eye1 = (center[0] - 3, center[1] - 4)
            eye2 = (center[0] + 3, center[1] - 4)
            pupil1 = (eye1[0] + 2, eye1[1])
            pupil2 = (eye2[0] + 2, eye2[1])
        elif self.direction == 180:
            eye1 = (center[0] - 3, center[1] - 4)
            eye2 = (center[0] + 3, center[1] - 4)
            pupil1 = (eye1[0] - 2, eye1[1])
            pupil2 = (eye2[0] - 2, eye2[1])
        else:
            eye1 = (center[0] - 4, center[1] - 4)
            eye2 = (center[0] + 4, center[1] - 4)
            pupil1 = (eye1[0], eye1[1] - 2)
            pupil2 = (eye2[0], eye2[1] - 2)
        
        if not self.frightened:
            pygame.draw.circle(screen, WHITE, eye1, eye_radius)
            pygame.draw.circle(screen, WHITE, eye2, eye_radius)
            pygame.draw.circle(screen, BLACK, pupil1, pupil_radius)
            pygame.draw.circle(screen, BLACK, pupil2, pupil_radius)
        else:
            for eye in [eye1, eye2]:
                pygame.draw.line(screen, WHITE, 
                               (eye[0] - 3, eye[1] - 3),
                               (eye[0] + 3, eye[1] + 3), 2)
                pygame.draw.line(screen, WHITE,
                               (eye[0] + 3, eye[1] - 3),
                               (eye[0] - 3, eye[1] + 3), 2)