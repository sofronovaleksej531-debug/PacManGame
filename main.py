import pygame
import sys
from settings import *
from game.game_state import GameState

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Pac-Man')
    clock = pygame.time.Clock()
    game = GameState()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and (game.game_over or game.won):
                    game = GameState()
                else:
                    if not game.game_over and not game.won:
                        game.handle_input(event.key)
        
        if not game.game_over and not game.won:
            game.update()
        
        screen.fill(BLACK)
        game.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main()