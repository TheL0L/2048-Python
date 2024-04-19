from game import Game, Direction
import pygame
import constants
from grid_window import draw_grid, draw_popup


def main():
    pygame.init()
    screen = pygame.display.set_mode((constants.WINDOW_SIZE, constants.WINDOW_SIZE))
    engine_clock = pygame.time.Clock()

    # initialize fonts
    FONT_30 = pygame.font.SysFont('Consolas', 30)
    FONT_36 = pygame.font.SysFont('Consolas', 36)

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
                if not game.hasEnded():
                    if event.key == pygame.K_UP:
                        game.move(Direction.UP)
                    if event.key == pygame.K_DOWN:
                        game.move(Direction.DOWN)
                    if event.key == pygame.K_LEFT:
                        game.move(Direction.LEFT)
                    if event.key == pygame.K_RIGHT:
                        game.move(Direction.RIGHT)
        
        # Draw the game grid
        grid_surface = draw_grid(FONT_30, game.getGrid())
        screen.blit(grid_surface, (0, 0))

        # draw game over screen if game is over
        if game.hasEnded():
            popup, x, y = draw_popup(FONT_36)
            screen.blit(popup, (x ,y))

        engine_clock.tick(constants.FPS_CAP)
        pygame.display.flip()


if __name__ == "__main__":
    main()
