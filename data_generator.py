from game import Game
import expectimax
from tqdm import tqdm
import os
import time

DATASET_PATH = './expecti_runs/'

# Function to save training data to a file
def save_training_data(training_data):
    if not os.path.exists(DATASET_PATH):
        os.makedirs(DATASET_PATH)
    with open(os.path.join(DATASET_PATH, f'run_{time.time()}.txt'), 'w') as file:
        for step in training_data:
            file.write(f'{repr(step)}\n')

# Function to load training data from a file
def load_training_data(filename):
    file_path = os.path.join(DATASET_PATH, filename)
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r') as file:
        return [eval(line) for line in file]


def get_data_files(folder_path = './expecti_runs/'):
    if not os.path.exists(folder_path):
        return []
    return [file for file in os.listdir(folder_path) if file.endswith('.txt')]


# Function to play the game and collect training data
def play_game_and_collect_data(max_moves=3000):
    game = Game()  # Initialize the game
    training_data = []  # List to store (state, action) pairs

    game_bar = tqdm(total=max_moves, desc="Game Progress")

    made_moves = 0
    while not game.hasEnded() and made_moves < max_moves:
        grid = game.getGrid()
        best_move = expectimax.getBestMove(game, depth=3)
        training_data.append((grid, best_move.value))
        game.attempt_move(best_move)
        made_moves += 1
        game_bar.update()

    game_bar.close()
    return training_data

def generate_data(count = 10):
    for _ in tqdm(range(count), desc="Generating data", unit="game"):
        training_data = play_game_and_collect_data(max_moves=3000)
        save_training_data(training_data)
