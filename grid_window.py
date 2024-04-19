import pygame
import constants
from constants import GET_TILE_COLOR


# Function to draw a gameover popup
def draw_popup(FONT):
    # setup constants
    BLACK = (0, 0, 0)
    LIGHT_RED = (255, 70, 70, 200)
    w, h = 275, 100
    x, y = (constants.WINDOW_SIZE - w)//2, (constants.WINDOW_SIZE - h)//3

    # create a surface for the popup
    popup_surface = pygame.Surface((w, h), pygame.SRCALPHA)
    
    # draw the background rectangle and border
    pygame.draw.rect(popup_surface, LIGHT_RED, (0, 0, w, h))
    pygame.draw.rect(popup_surface, BLACK, (0, 0, w, h), 1)
    
    # render the text
    text_surface = FONT.render('Game Over!', True, BLACK)
    # calculate text position
    text_rect = text_surface.get_rect(center=(w//2, h//2))
    # draw the text and textbox
    popup_surface.blit(text_surface, text_rect)

    return popup_surface, x, y


# Function to draw the grid
def draw_grid(FONT, grid):
    # Calculate cell size
    cell_size = (constants.WINDOW_SIZE - (constants.GRID_SIZE + 1) * constants.GAP_SIZE) // constants.GRID_SIZE

    # Create a surface for the game screen
    game_surface = pygame.Surface((constants.WINDOW_SIZE, constants.WINDOW_SIZE))
    game_surface.fill((255, 255, 255))

    for i in range(constants.GRID_SIZE):
        for j in range(constants.GRID_SIZE):
            # Calculate cell position
            x = constants.GAP_SIZE + j * (cell_size + constants.GAP_SIZE)
            y = constants.GAP_SIZE + i * (cell_size + constants.GAP_SIZE)

            # Draw cell border
            pygame.draw.rect(game_surface, (0, 0, 0), (x, y, cell_size, cell_size), 2)

            # Get cell color based on value
            cell_color = GET_TILE_COLOR(grid[i][j])

            # Draw cell background with dynamic color
            pygame.draw.rect(game_surface, cell_color, (x + 2, y + 2, cell_size - 4, cell_size - 4))

            # Print value inside the cell
            value_string = str(grid[i][j]) if grid[i][j]>0 else None
            text = FONT.render(value_string, True, (0, 0, 0))
            text_rect = text.get_rect(center=(x + cell_size // 2, y + cell_size // 2))
            game_surface.blit(text, text_rect)
    return game_surface

