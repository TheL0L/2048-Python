import constants
from game import Game, Grid, Direction
import math

def evaluate(game):
    if constants.GRID_SIZE != 4:
        return game.getScore()

    if not game.hasValidMoves() or game.hasEnded():
        return 0

    if constants.EVAL_FUNC == 'score':
        return game.getScore()
    elif constants.EVAL_FUNC == 'weighted':
        grid = game.getGrid()
        score = 0
        for i in range(constants.GRID_SIZE):
            for j in range(constants.GRID_SIZE):
                score += grid[i][j] * constants.WEIGHT_MATRIX[i][j]
        return score


def expectimax(game, depth, max_player):
    if depth == 0 or not game.hasValidMoves():
        return evaluate(game)
    
    if max_player:
        # simulate a move in each direction
        # and search for max expected state evaluation
        max_utility = -math.inf
        for move in range(4):
            game_copy = Game(game.getGrid(), game.getScore())

            # skip invalid moves
            if not game_copy.move(Direction(move)):
                continue

            utility = expectimax(game_copy, depth - 1, False)
            max_utility = max(max_utility, utility)
        return max_utility
    else:
        # simulate insertions of new tiles after a move
        # in every possible spot, with either 2 or 4 tiles
        # and average the evaluation of all possible states
        sum_utility = 0
        empty_cells = Grid(game.getGrid()).getEmptyCells()
        for position in empty_cells:
            game_copy_2 = Game(game.getGrid(), game.getScore())
            game_copy_4 = Game(game.getGrid(), game.getScore())
            game_copy_2.insertTile(2, position)
            game_copy_4.insertTile(4, position)
            sum_utility += 0.9 * expectimax(game_copy_2, depth - 1, True) + 0.1 * expectimax(game_copy_4, depth - 1, True)
        return sum_utility / max(1, len(empty_cells))


def getBestMove(game, depth):
    best_move = None
    best_utility = -math.inf
    for move in range(4):
        game_copy = Game(game.getGrid(), game.getScore())

        # skip invalid moves
        if not game_copy.move(Direction(move)):
            continue

        utility = expectimax(game_copy, depth, max_player=False)
        if utility > best_utility:
            best_move = Direction(move)
            best_utility = utility
    return best_move

