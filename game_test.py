from game import Game, Direction
import pygame
import constants
from grid_window import draw_grid

def main():
    pygame.init()
    screen = pygame.display.set_mode((constants.WINDOW_SIZE, constants.WINDOW_SIZE))
    engine_clock = pygame.time.Clock()

    game = Game()

    while True:
        pygame.display.set_caption(f"2048-Python   |   [R]estart   |   Moves = {len(game.getMoves())}   |   Score = {game.getScore()}")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYUP:
                # reset
                if event.key == pygame.K_r:
                    game.restartGame()
                # moves
                if event.key == pygame.K_UP:
                    game.move(Direction.UP)
                if event.key == pygame.K_DOWN:
                    game.move(Direction.DOWN)
                if event.key == pygame.K_LEFT:
                    game.move(Direction.LEFT)
                if event.key == pygame.K_RIGHT:
                    game.move(Direction.RIGHT)
        
        # Draw the game grid
        draw_grid(screen, constants.GRID_SIZE, constants.GAP_SIZE, constants.WINDOW_SIZE, game.getGrid())
        engine_clock.tick(constants.FPS_CAP)
        pygame.display.flip()


if __name__ == "__main__":
    main()
