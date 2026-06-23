import pygame
import math
from settings import *

class PacMan:
    def __init__(self):
        self.x = 14 * CELL_SIZE + CELL_SIZE // 2
        self.y = 15 * CELL_SIZE + CELL_SIZE // 2
        self.direction = 0
        self.next_direction = 0
        self.radius = (CELL_SIZE // 2) - 2
        self.speed = PACMAN_SPEED
        self.width = MAZE_WIDTH
        self.height = MAZE_HEIGHT
        self.mouth_angle = 0
        self.mouth_direction = 1
        self.start_x = self.x
        self.start_y = self.y
    
    def handle_input(self, key):
        if key == pygame.K_LEFT or key == pygame.K_a:
            self.next_direction = 180
        elif key == pygame.K_RIGHT or key == pygame.K_d:
            self.next_direction = 0
        elif key == pygame.K_UP or key == pygame.K_w:
            self.next_direction = 90
        elif key == pygame.K_DOWN or key == pygame.K_s:
            self.next_direction = 270
    
    def update(self, maze):
        self.mouth_angle += 4 * self.mouth_direction
        if self.mouth_angle >= 30:
            self.mouth_angle = 30
            self.mouth_direction = -1
        elif self.mouth_angle <= 0:
            self.mouth_angle = 0
            self.mouth_direction = 1
        
        self.try_move(maze)
    
    def try_move(self, maze):
        grid_x = round((self.x - CELL_SIZE // 2) / CELL_SIZE)
        grid_y = round((self.y - CELL_SIZE // 2) / CELL_SIZE)

        if self.next_direction != self.direction:
            can_change = self.can_move_in_direction(maze, self.next_direction, grid_x, grid_y)
            if can_change:
                self.x = grid_x * CELL_SIZE + CELL_SIZE // 2
                self.y = grid_y * CELL_SIZE + CELL_SIZE // 2
                self.direction = self.next_direction
        
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
        else:
            self.x = grid_x * CELL_SIZE + CELL_SIZE // 2
            self.y = grid_y * CELL_SIZE + CELL_SIZE // 2
    
    def can_move_in_direction(self, maze, direction, grid_x, grid_y):
        if direction == 0:
            return not maze.is_wall((grid_x + 1) * CELL_SIZE + CELL_SIZE // 2, 
                                   grid_y * CELL_SIZE + CELL_SIZE // 2)
        elif direction == 180:
            return not maze.is_wall((grid_x - 1) * CELL_SIZE + CELL_SIZE // 2, 
                                   grid_y * CELL_SIZE + CELL_SIZE // 2)
        elif direction == 90:
            return not maze.is_wall(grid_x * CELL_SIZE + CELL_SIZE // 2, 
                                   (grid_y - 1) * CELL_SIZE + CELL_SIZE // 2)
        elif direction == 270:
            return not maze.is_wall(grid_x * CELL_SIZE + CELL_SIZE // 2, 
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
    
    def get_position(self):
        return (int(self.x // CELL_SIZE), int(self.y // CELL_SIZE))
    
    def reset_position(self):
        self.x = self.start_x
        self.y = self.start_y
        self.direction = 0
        self.next_direction = 0
    
    def draw(self, screen):
        center = (int(self.x), int(self.y))
        mouth_angle_rad = math.radians(self.mouth_angle)

        pygame.draw.circle(screen, YELLOW, center, self.radius)

        if self.direction == 0:
            start_angle = -mouth_angle_rad
            end_angle = mouth_angle_rad
        elif self.direction == 180:
            start_angle = math.pi - mouth_angle_rad
            end_angle = math.pi + mouth_angle_rad
        elif self.direction == 90:
            start_angle = -math.pi/2 - mouth_angle_rad
            end_angle = -math.pi/2 + mouth_angle_rad
        elif self.direction == 270:
            start_angle = math.pi/2 - mouth_angle_rad
            end_angle = math.pi/2 + mouth_angle_rad
        else:
            start_angle = -mouth_angle_rad
            end_angle = mouth_angle_rad
        points = [center]
        num_points = 20
        
        if start_angle <= end_angle:
            for i in range(num_points + 1):
                t = i / num_points
                angle = start_angle + (end_angle - start_angle) * t
                x = center[0] + self.radius * math.cos(angle)
                y = center[1] + self.radius * math.sin(angle)
                points.append((x, y))
        else:
            for i in range(num_points + 1):
                t = i / num_points
                angle = start_angle + (end_angle - start_angle) * t
                x = center[0] + self.radius * math.cos(angle)
                y = center[1] + self.radius * math.sin(angle)
                points.append((x, y))
        if len(points) > 2:
            pygame.draw.polygon(screen, BLACK, points)
        eye_radius = 2
        if self.direction == 0:
            eye_pos = (center[0] + 5, center[1] - 5)
        elif self.direction == 180:
            eye_pos = (center[0] - 5, center[1] - 5)
        elif self.direction == 90:
            eye_pos = (center[0] - 5, center[1] - 5)
        elif self.direction == 270:
            eye_pos = (center[0] - 5, center[1] + 5)
        
        pygame.draw.circle(screen, BLACK, eye_pos, eye_radius)