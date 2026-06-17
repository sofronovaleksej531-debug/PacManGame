import pygame
from settings import *
from .maze import Maze
from .pacman import PacMan
from .ghost import Ghost

class GameState:
    def __init__(self):
        self.maze = Maze()
        self.pacman = PacMan()
        spawn_points = self.maze.get_ghost_spawn_points()
        self.ghosts = [
            Ghost(spawn_points[0][0], spawn_points[0][1], RED, (0, 0), 0),
            Ghost(spawn_points[1][0], spawn_points[1][1], PINK, (MAZE_WIDTH-1, 0), 1),
            Ghost(spawn_points[2][0], spawn_points[2][1], CYAN, (MAZE_WIDTH-1, MAZE_HEIGHT-1), 2),
            Ghost(spawn_points[3][0], spawn_points[3][1], ORANGE, (0, MAZE_HEIGHT-1), 3)
        ]
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.won = False
    
    def handle_input(self, key):
        self.pacman.handle_input(key)
    
    def update(self):
        if self.game_over or self.won:
            return
        
        self.pacman.update(self.maze)
        
        pacman_pos = self.pacman.get_position()
        
        for ghost in self.ghosts:
            ghost.update(self.maze, pacman_pos)
        
        points = self.maze.eat_dot(self.pacman.x, self.pacman.y)
        if points > 0:
            self.score += points
            if points == 50:
                for ghost in self.ghosts:
                    ghost.make_frightened()
        
        if self.maze.get_remaining_dots() == 0:
            self.won = True
            self.game_over = True
        
        for ghost in self.ghosts:
            ghost_rect = ghost.get_rect()
            pacman_rect = pygame.Rect(self.pacman.x, self.pacman.y, CELL_SIZE, CELL_SIZE)
            
            if ghost_rect.colliderect(pacman_rect):
                if ghost.frightened:
                    self.score += 200
                    ghost.reset_position()
                else:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_over = True
                    else:
                        self.reset_positions()
    
    def reset_positions(self):
        self.pacman = PacMan()
        for ghost in self.ghosts:
            ghost.reset_position()
    
    def draw(self, screen):
        self.maze.draw(screen)
        self.pacman.draw(screen)
        for ghost in self.ghosts:
            ghost.draw(screen)
        
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        screen.blit(score_text, (10, SCREEN_HEIGHT - 40))
        
        for i in range(self.lives):
            pygame.draw.circle(screen, YELLOW, 
                             (SCREEN_WIDTH - 50 - i * 30, SCREEN_HEIGHT - 25), 10)
        
        if self.game_over:
            font_big = pygame.font.Font(None, 74)
            if self.won:
                text = font_big.render('YOU WIN!', True, WHITE)
            else:
                text = font_big.render('GAME OVER', True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(text, text_rect)
            
            font_small = pygame.font.Font(None, 36)
            restart_text = font_small.render('Press SPACE to restart', True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
            screen.blit(restart_text, restart_rect)
    def reset_positions(self):
        self.pacman = PacMan()
        for ghost in self.ghosts:
            ghost.reset_position()