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
        self.mouth_angle = 0
        self.mouth_direction = 1
    
    def handle_input(self, key):
        if key == pygame.K_LEFT:
            self.next_direction = 180
        elif key == pygame.K_RIGHT:
            self.next_direction = 0
        elif key == pygame.K_UP:
            self.next_direction = 90
        elif key == pygame.K_DOWN:
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
        new_x, new_y = self.x, self.y
        
        if self.next_direction != self.direction:
            dx = 0
            dy = 0
            if self.next_direction == 0:
                dx = self.speed
            elif self.next_direction == 180:
                dx = -self.speed
            elif self.next_direction == 90:
                dy = -self.speed
            elif self.next_direction == 270:
                dy = self.speed
            
            test_x = new_x + dx
            test_y = new_y + dy
            
            if not maze.is_wall(test_x + 10, test_y + 10) and not maze.is_wall(test_x - 10, test_y + 10) and not maze.is_wall(test_x + 10, test_y - 10) and not maze.is_wall(test_x - 10, test_y - 10):
                self.direction = self.next_direction
                self.x = test_x
                self.y = test_y
        
        dx = 0
        dy = 0
        if self.direction == 0:
            dx = self.speed
        elif self.direction == 180:
            dx = -self.speed
        elif self.direction == 90:
            dy = -self.speed
        elif self.direction == 270:
            dy = self.speed
        
        test_x = self.x + dx
        test_y = self.y + dy
        
        if not maze.is_wall(test_x + 10, test_y + 10) and not maze.is_wall(test_x - 10, test_y + 10) and not maze.is_wall(test_x + 10, test_y - 10) and not maze.is_wall(test_x - 10, test_y - 10):
            self.x = test_x
            self.y = test_y
        else:
            if self.direction == 0 or self.direction == 180:
                self.x = round(self.x / CELL_SIZE) * CELL_SIZE
            else:
                self.y = round(self.y / CELL_SIZE) * CELL_SIZE
    
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
        
        eye_radius = 3
        eye_offset = 8
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