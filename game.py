import random
import constants
from constants import GRID_SIZE

GAME_RNG = random.Random(constants.SEED)


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
    def __init__(self, grid = None):
        if grid is not None:
            self.__grid = Grid(grid)
        else:
            self.__grid = Grid()
            self.__addStartingTiles()
        
        self.__score = 0
        self.__moves = 0

    def getGrid(self):
        return self.__grid.getGrid()
    
    def __insertRandomTile(self):
        empty = self.__grid.getEmptyCells()
        if len(empty) > 0:
            self.__grid.insertTile(Tile(), GAME_RNG.choice(empty))

    def __addStartingTiles(self):
        for _ in range(constants.STARTING_TILES):
            self.__insertRandomTile()

    def __moveTile(self, position_old, position_new):
        tile = self.__grid.getCell(position_old)
        self.__grid.removeTile(position_old)
        self.__grid.insertTile(tile, position_new)

    def __finalizeTiles(self):
        self.__grid.finalizeGrid()

    def restartGame(self):
        if constants.RESET_RNG_ON_GAME_RESTART:
            GAME_RNG.seed(constants.SEED)  # reset the RNG
        self.__grid = Grid()
        self.__addStartingTiles()
        self.__score = 0
        self.__moves = 0

    # implement moving logic
