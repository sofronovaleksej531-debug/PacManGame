import pygame
from settings import *

class PacMan:
    def __init__(self):
        self.x = 14 * CELL_SIZE
        self.y = 15 * CELL_SIZE
        self.direction = 0
        self.next_direction = 0
        self.radius = CELL_SIZE // 2 - 2
        self.speed = PACMAN_SPEED
        self.width = MAZE_WIDTH
        self.height = MAZE_HEIGHT
        self.mouth_angle = 0
        self.mouth_direction = 1
    
    def handle_input(self, key):
        if key == pygame.K_a:
            self.next_direction = 180
        elif key == pygame.K_d:
            self.next_direction = 0
        elif key == pygame.K_w:
            self.next_direction = 90
        elif key == pygame.K_s:
            self.next_direction = 270
    
    def update(self, maze):
        self.mouth_angle += 10 * self.mouth_direction
        if self.mouth_angle >= 50:
            self.mouth_angle = 50
            self.mouth_direction = -1
        elif self.mouth_angle <= 0:
            self.mouth_angle = 0
            self.mouth_direction = 1
        
        self.try_move(maze)
    
    def try_move(self, maze):
        grid_x = int(self.x // CELL_SIZE)
        grid_y = int(self.y // CELL_SIZE)
        
        if self.x % CELL_SIZE == 0 and self.y % CELL_SIZE == 0:
            if self.next_direction != self.direction:
                can_change = False
                if self.next_direction == 0:
                    if not maze.is_wall((grid_x + 1) * CELL_SIZE, grid_y * CELL_SIZE):
                        can_change = True
                elif self.next_direction == 180:
                    if not maze.is_wall((grid_x - 1) * CELL_SIZE, grid_y * CELL_SIZE):
                        can_change = True
                elif self.next_direction == 90:
                    if not maze.is_wall(grid_x * CELL_SIZE, (grid_y - 1) * CELL_SIZE):
                        can_change = True
                elif self.next_direction == 270:
                    if not maze.is_wall(grid_x * CELL_SIZE, (grid_y + 1) * CELL_SIZE):
                        can_change = True
                
                if can_change:
                    self.direction = self.next_direction
        
        if self.direction == 0:
            next_x = self.x + self.speed
            next_grid_x = int((next_x + CELL_SIZE // 2) // CELL_SIZE)
            next_grid_y = int((self.y + CELL_SIZE // 2) // CELL_SIZE)
            
            if not maze.is_wall(next_grid_x * CELL_SIZE, next_grid_y * CELL_SIZE):
                self.x = next_x
        
        elif self.direction == 180:
            next_x = self.x - self.speed
            next_grid_x = int((next_x + CELL_SIZE // 2) // CELL_SIZE)
            next_grid_y = int((self.y + CELL_SIZE // 2) // CELL_SIZE)
            
            if not maze.is_wall(next_grid_x * CELL_SIZE, next_grid_y * CELL_SIZE):
                self.x = next_x
        
        elif self.direction == 90:
            next_y = self.y - self.speed
            next_grid_x = int((self.x + CELL_SIZE // 2) // CELL_SIZE)
            next_grid_y = int((next_y + CELL_SIZE // 2) // CELL_SIZE)
            
            if not maze.is_wall(next_grid_x * CELL_SIZE, next_grid_y * CELL_SIZE):
                self.y = next_y
        
        elif self.direction == 270:
            next_y = self.y + self.speed
            next_grid_x = int((self.x + CELL_SIZE // 2) // CELL_SIZE)
            next_grid_y = int((next_y + CELL_SIZE // 2) // CELL_SIZE)
            
            if not maze.is_wall(next_grid_x * CELL_SIZE, next_grid_y * CELL_SIZE):
                self.y = next_y
    
    def get_position(self):
        return (int(self.x // CELL_SIZE), int(self.y // CELL_SIZE))
    
    def draw(self, screen):
        center = (int(self.x + CELL_SIZE // 2), int(self.y + CELL_SIZE // 2))
        
        angle = self.mouth_angle
        start_angle = self.direction + angle
        end_angle = self.direction - angle
        
        pygame.draw.arc(screen, YELLOW, 
                       (center[0] - self.radius, center[1] - self.radius,
                        self.radius * 2, self.radius * 2),
                       start_angle * 3.14159 / 180,
                       end_angle * 3.14159 / 180,
                       self.radius)
        
        pygame.draw.line(screen, YELLOW, center, 
                        (center[0] + self.radius * 0.7, center[1]), self.radius)
        
        eye_radius = 3
        if self.direction == 0:
            eye1 = (center[0] + 5, center[1] - 6)
            eye2 = (center[0] + 5, center[1] + 6)
        elif self.direction == 180:
            eye1 = (center[0] - 5, center[1] - 6)
            eye2 = (center[0] - 5, center[1] + 6)
        elif self.direction == 90:
            eye1 = (center[0] - 6, center[1] - 5)
            eye2 = (center[0] + 6, center[1] - 5)
        else:
            eye1 = (center[0] - 6, center[1] + 5)
            eye2 = (center[0] + 6, center[1] + 5)
        
        pygame.draw.circle(screen, BLACK, eye1, eye_radius)
        pygame.draw.circle(screen, BLACK, eye2, eye_radius)