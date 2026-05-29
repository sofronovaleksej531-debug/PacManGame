import pygame
import sys
from settings import *
from game.game_state import GameState

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('PacMan')
    clock = pygame.time.Clock()
    game = GameState()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and game.game_over:
                    game = GameState()
                else:
                    game.handle_input(event)
            
        if not game.game_over and not game.won:
            game.update()

        screen.fill(BLACK)
        game.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main()