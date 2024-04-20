import random
import constants
from constants import GRID_SIZE
from enum import Enum

GAME_RNG = random.Random(constants.SEED)

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Tile:
    def __init__(self, value = None, was_merged = False):
        self.__value = value if value is not None else (2 if GAME_RNG.random() < 0.9 else 4)
        self.__was_merged = was_merged and (value > 0)

    def getValue(self):
        return self.__value
    
    def wasMerged(self):
        return self.__was_merged

    def finalize(self):
        self.__was_merged = False


class Grid:
    def __init__(self, grid = None):
        if grid is not None:
            self.__grid = [[Tile(grid[row][col]) for col in range(GRID_SIZE)] for row in range(GRID_SIZE)]
        else:
            self.__grid = [[Tile(0) for col in range(GRID_SIZE)] for row in range(GRID_SIZE)]
    
    def insertTile(self, tile, position):
        row, col = position
        self.__grid[row][col] = tile

    def removeTile(self, position):
        row, col = position
        self.__grid[row][col] = Tile(0)
    
    def isCellWithinBounds(self, position):
        return (position[0] >= 0 and position[0] < GRID_SIZE) and (position[1] >= 0 and position[1] < GRID_SIZE)

    def getCell(self, position):
        row, col = position
        return self.__grid[row][col]

    def getGrid(self):
        return [[self.__grid[row][col].getValue() for col in range(GRID_SIZE)] for row in range(GRID_SIZE)]

    def isCellEmpty(self, position):
        return self.getCell(position).getValue() == 0

    def getEmptyCells(self):
        empty = []
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                position = (row, col)
                if self.isCellEmpty(position):
                    empty.append(position)
        return empty

    def finalizeGrid(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                position = (row, col)
                self.getCell(position).finalize()


class Game:
    def __init__(self, grid = None, score = 0):
        if grid is not None:
            self.__grid = Grid(grid)
        else:
            self.__grid = Grid()
            self.__addStartingTiles()
        
        self.__score = max(0, score)
        self.__moves = []
        self.__hasEnded = False

    def getGrid(self):
        return self.__grid.getGrid()
    
    def __insertRandomTile(self):
        empty = self.__grid.getEmptyCells()
        if len(empty) > 0:
            self.__grid.insertTile(Tile(), GAME_RNG.choice(empty))

    def __addStartingTiles(self):
        for _ in range(constants.STARTING_TILES):
            self.__insertRandomTile()

    def restartGame(self):
        if constants.RESET_RNG_ON_GAME_RESTART:
            GAME_RNG.seed(constants.SEED)  # reset the RNG
        self.__grid = Grid()
        self.__addStartingTiles()
        self.__score = 0
        self.__moves = []
        self.__hasEnded = False

    def hasEnded(self):
        return self.__hasEnded

    def hasValidMoves(self):
        return len(self.__grid.getEmptyCells()) > 0 or self.__mergePossible()
    
    def __mergePossible(self):
        # iterate over all cells
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                position = (row, col)
                
                # check in all directions
                for d in Direction:
                    vector = self.__getDirectionVector(d)
                    farthest = self.__findFarthestEmptyPosition(position, vector)
                    # what is the first obstacle in a given direction
                    obstacle = (farthest[0] + vector[0], farthest[1] + vector[1])
                    if self.__grid.isCellWithinBounds(obstacle):
                        # can the current tile and the obstacle be merged?
                        if self.__grid.getCell(position).getValue() == self.__grid.getCell(obstacle).getValue():
                            # if so, return true
                            return True
                    # otherwise keep checking other directions
        return False

    def __findFarthestEmptyPosition(self, position, vector):
        farthest = position

        while True:
            next_pos = (farthest[0] + vector[0], farthest[1] + vector[1])
            if self.__grid.isCellWithinBounds(next_pos) and self.__grid.isCellEmpty(next_pos):
                farthest = next_pos
            else:
                break

        return farthest
    
    def __getDirectionVector(self, direction):
        vectors = {
            Direction.UP:       (   -1,   0    ),
            Direction.RIGHT:    (   0,    1    ),
            Direction.DOWN:     (   1,    0    ),
            Direction.LEFT:     (   0,    -1   ),
        }
        return vectors[direction]
    
    def insertTile(self, value, position):
        # this method is explicitly used for the expectimax algorithm, just to make things quicker
        self.__grid.insertTile(Tile(value), position)

    def attempt_move(self, direction):
        valid_move = self.move(direction)
        if valid_move:
            # insert a new random tile
            self.__insertRandomTile()
            # finalize the tile states
            self.__grid.finalizeGrid()
            # save the move
            self.__moves.append(direction)
            # check if the game has ended this turn
            if not self.hasValidMoves():
                self.__hasEnded = True
        return valid_move

    def move(self, direction):
        valid_move = False

        # setup the move steps
        vector = self.__getDirectionVector(direction)
        traversals = self.__buildTraversals(vector)

        # perform the moves on the tiles
        for position in traversals:
            # if current tile is empty, skip the iteration
            if self.__grid.getCell(position).getValue() == 0:
                continue

            # get the farthest empty tile, and the first obstacle in the move direction
            farthest = self.__findFarthestEmptyPosition(position, vector)
            obstacle = (farthest[0] + vector[0], farthest[1] + vector[1])

            # check if the obstacle is a valid tile
            is_obstacle_valid = self.__grid.isCellWithinBounds(obstacle)
            if is_obstacle_valid:
                # check if merging is possible, same value and neither was merged this move
                current_tile = self.__grid.getCell(position)
                obstacle_tile = self.__grid.getCell(obstacle)
                if (current_tile.getValue() == obstacle_tile.getValue()
                    and not current_tile.wasMerged() and not obstacle_tile.wasMerged()):
                    # merge is possible, merge into a new tile at the obstacle position
                    merged = Tile(current_tile.getValue() + obstacle_tile.getValue(), True)
                    self.__grid.insertTile(merged, obstacle)
                    # remove the current position tile
                    self.__grid.removeTile(position)
                    # indicate that the move is valid
                    valid_move = True
                    # increase the score
                    self.__score += merged.getValue()
                else:
                    is_obstacle_valid = False
            # if could not merge, check if the farthest empty tile position, is not the current position
            if is_obstacle_valid == False and position != farthest:
                # farthest empty tile is valid, move the current tile there
                current_tile = self.__grid.getCell(position)
                self.__grid.insertTile(current_tile, farthest)
                self.__grid.removeTile(position)
                # indicate that the move is valid
                valid_move = True
            # otherwise currently can not do anything with this tile

        return valid_move
    
    def __buildTraversals(self, vector):
        # build a list of position to follow during the Move operation
        t_row = [step for step in range(GRID_SIZE)]
        t_col = [step for step in range(GRID_SIZE)]

        # start moving from the farthest cell opposite to the given direction
        if vector[0] == 1:
            t_row.reverse()
        if vector[1] == 1:
            t_col.reverse()
        
        traversals = []
        for r in t_row:
            for c in t_col:
                traversals.append( (r, c) )
        return traversals

    def getScore(self):
        return self.__score

    def getMoves(self):
        return self.__moves
