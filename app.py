from game import Game, Direction
import pygame
import constants
from grid_window import draw_grid, draw_popup
import numpy as np
from graph_exporter import plot_graph
import expectimax
from neural_net import NeuralNetwork, load_weights, preprocess_state
import torch, random

AGENT = ['USER', 'EXPECTIMAX', 'NEURALNET'][2]
SEARCH_DEPTH = 3
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


def get_max_tile(grid):
    return np.array(grid).flatten().max()

def create_nn_agent():
    model = NeuralNetwork().to(DEVICE)
    load_weights(model, 'model_weights_plain_relu_120ep.pth')
    return model


def get_user_decision():
    # iterate over captured events, and process the first matching user action
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return 'EXIT'
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_r:
                return 'RESTART'
            elif event.key == pygame.K_UP:
                return Direction.UP
            elif event.key == pygame.K_DOWN:
                return Direction.DOWN
            elif event.key == pygame.K_LEFT:
                return Direction.LEFT
            elif event.key == pygame.K_RIGHT:
                return Direction.RIGHT
    return None

def get_expecti_decision(game):
    return expectimax.getBestMove(game, SEARCH_DEPTH)

def get_nn_decision(game, model):
    # prepare a copy of the game object for move validation
    grid = game.getGrid()
    game_copy = Game(grid)

    # let the model predict a move based on current game grid
    state_tensor = preprocess_state(grid).to(DEVICE)
    outputs = model(state_tensor)
    predicted_move = Direction(torch.argmax(outputs).item())

    is_forced = False
    forced_move = None

    # validate move, and randomly select a forced move incase move was invalid
    if not game_copy.attempt_move(predicted_move):
        moves = [0, 1, 2, 3]
        moves.remove(predicted_move.value)
        is_forced = True

        for _ in range(3):
            forced_move = Direction(random.choice(moves))
            if not game_copy.attempt_move(forced_move):
                moves.remove(forced_move.value)
            else:
                break
    
    return (predicted_move, is_forced, forced_move)


def game_loop(game, screen, engine_clock, tile_font, gameover_font, model):
    # check if given game instance awaits restart
    if game.hasEnded():
        action = get_user_decision()
        return action if (action == 'EXIT' or action == 'RESTART') else None

    # prepare variables for game data tracking
    forced_moves, scores, max_tiles = [], [0], [get_max_tile(game.getGrid())]

    while not game.hasEnded():
        # update window title
        pygame.display.set_caption(f"2048-Python   |   [R]estart   |   Moves = {len(game.getMoves())}   |   Score = {game.getScore()}")

        # write screen data into draw buffer
        grid_surface = draw_grid(tile_font, game.getGrid())
        screen.blit(grid_surface, (0, 0))

        # draw buffer onto sreen
        engine_clock.tick(constants.FPS_CAP)
        pygame.display.flip()

        # prepare variables for decision break down
        move, is_forced, forced_move = None, False, None

        # get agent decision
        if AGENT == 'USER':
            decision = get_user_decision()
            if decision is None:
                continue
            elif decision == 'EXIT' or decision == 'RESTART':
                return decision
            else:
                move = decision

        elif AGENT == 'EXPECTIMAX':
            move = get_expecti_decision(game)

        else:
            move, is_forced, forced_move = get_nn_decision(game, model)
        
        # enact agent decision
        is_valid = game.attempt_move(forced_move if is_forced else move)
        if not is_valid:
            continue

        # track agent decision
        if is_forced:
            forced_moves.append(len(game.getMoves()) - 1)
        scores.append(game.getScore())
        max_tiles.append(get_max_tile(game.getGrid()))

        # allow user input, for any active agent
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'EXIT'
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    return 'RESTART'
        
    # write final screen data into draw buffer
    grid_surface = draw_grid(tile_font, game.getGrid())
    screen.blit(grid_surface, (0, 0))

    # write gameover screen data into draw buffer
    popup, x, y = draw_popup(gameover_font)
    screen.blit(popup, (x ,y))

    # draw buffer onto sreen
    engine_clock.tick(constants.FPS_CAP)
    pygame.display.flip()

    # return game tracking data
    return (scores, game.getMoves(), forced_moves, max_tiles)


if __name__ == '__main__':
    # initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((constants.WINDOW_SIZE, constants.WINDOW_SIZE))
    engine_clock = pygame.time.Clock()

    # initialize fonts
    tile_font = pygame.font.SysFont('Consolas', 30)
    gameover_font = pygame.font.SysFont('Consolas', 36)

    # initialize neuralnet agent if necessary
    model = create_nn_agent() if AGENT == 'NEURALNET' else None

    # initialize the 2048 game instance
    game = Game()

    # main app loop, allows multiple sequential games
    while True:
        # complete a game, and get game tracking data
        result = game_loop(game, screen, engine_clock, tile_font, gameover_font, model)

        # check if there was a specific request by the user
        if result == 'EXIT':
            pygame.quit()
            break
        elif result == 'RESTART':
            game.restartGame()
        elif result is not None:
            # if not, then save tracked game data as an organized graph
            scores, moves, forced_moves, max_tiles = result
            plot_graph(scores, moves, forced_moves, max_tiles)
        
