import pygame
import constants
from constants import GET_TILE_COLOR


# Function to draw the grid
def draw_grid(pygame_screen, grid_size, gap_size, window_size, grid):
    cell_size = (window_size - (grid_size + 1) * gap_size) // grid_size

    # Initialize the font
    FONT = pygame.font.SysFont('Consolas', 30)

    # Draw background
    pygame_screen.fill((255, 255, 255))

    for i in range(grid_size):
        for j in range(grid_size):
            # Calculate cell position
            x = gap_size + j * (cell_size + gap_size)
            y = gap_size + i * (cell_size + gap_size)

            # Draw cell border
            pygame.draw.rect(pygame_screen, (0, 0, 0), (x, y, cell_size, cell_size), 2)

            # Get cell color based on value
            cell_color = GET_TILE_COLOR(grid[i][j])

            # Draw cell background with dynamic color
            pygame.draw.rect(pygame_screen, cell_color, (x + 2, y + 2, cell_size - 4, cell_size - 4))

            # Print value inside the cell
            value_string = str(grid[i][j]) if grid[i][j]>0 else None
            text = FONT.render(value_string, True, (0, 0, 0))
            text_rect = text.get_rect(center=(x + cell_size // 2, y + cell_size // 2))
            pygame_screen.blit(text, text_rect)


def draw_test_grid():
    # Set parameters
    N = constants.GRID_SIZE
    GAP_SIZE = 5  # gap size
    WINDOW_SIZE = 500

    # Define a test grid
    grid = [[2**(i * N + j + 1) for j in range(N)] for i in range(N)]

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Grid with Pygame")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_g:  # cycle through 20 gap sizes
                    GAP_SIZE = (GAP_SIZE + 1) % 20
                    print(f'{GAP_SIZE=}')

        # Draw the grid
        draw_grid(screen, N, GAP_SIZE, WINDOW_SIZE, grid)

        pygame.display.flip()

if __name__ == "__main__":
    draw_test_grid()
