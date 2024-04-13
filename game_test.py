from game import Game
import pygame
import constants
from grid_window import draw_grid

def main():
    # Set parameters
    GAP_SIZE = 5
    WINDOW_SIZE = 500

    grid = [[0, 4, 0, 0],
            [0, 2, 0, 0],
            [0, 2, 0, 0],
            [0, 4, 0, 0]]
    game = Game(grid)

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("2048-Python")

    updated = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYUP:
                # reset
                if event.key == pygame.K_r:
                    game.restartGame()
                    updated = True
                # moves
                # if event.key == pygame.K_UP:
                #     updated += game.move(GameBoard.Direction.UP)
                # if event.key == pygame.K_DOWN:
                #     updated += game.move(GameBoard.Direction.DOWN)
                # if event.key == pygame.K_LEFT:
                #     updated += game.move(GameBoard.Direction.LEFT)
                # if event.key == pygame.K_RIGHT:
                #     updated += game.move(GameBoard.Direction.RIGHT)
        
        if bool(updated):
            # Draw the game grid
            draw_grid(screen, constants.GRID_SIZE, GAP_SIZE, WINDOW_SIZE, game.getGrid())
            updated = False
        
        pygame.display.flip()


if __name__ == "__main__":
    main()
