import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from game import Game, Direction
from tqdm import tqdm
import data_generator
import random
import os

ROOT_MODELS_PATH = './model_weights'

# Save the trained model weights
def save_weights(model, filename):
    if not os.path.exists(ROOT_MODELS_PATH):
        os.makedirs(ROOT_MODELS_PATH)
    model_path = os.path.join(ROOT_MODELS_PATH, filename)
    torch.save(model.state_dict(), model_path)
# Load pretrained weights
def load_weights(model, filename):
    model_path = os.path.join(ROOT_MODELS_PATH, filename)
    if not os.path.exists(model_path):
        return
    model.load_state_dict(torch.load(model_path))

# Define the neural network architecture
class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer1 = nn.Linear(16, 64)
        self.layer2 = nn.Linear(64, 16)
        self.layer3 = nn.Linear(16, 4)

    def forward(self, x):
        x = torch.relu(self.layer1(x))
        x = torch.relu(self.layer2(x))
        x = self.layer3(x)
        return x

# Define a function to preprocess the game state
def preprocess_state(grid):
    # Convert the grid to a flattened numpy array
    flattened_grid = np.array(grid).flatten()
    # Normalize the values to be between 0 and 1
    # normalize against the max tile, since we don't really care about previous states, or some max_tile goal
    normalized_grid = flattened_grid / flattened_grid.max()
    # Convert to tensor and reshape to match the input size of the neural network
    tensor_grid = torch.tensor(normalized_grid, dtype=torch.float).unsqueeze(0)
    return tensor_grid


if __name__ == '__main__':
    # decide which device should be used
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # Initialize the neural network
    model = NeuralNetwork().to(device)
    # Define loss function and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # load weights
    load_weights(model, 'model_weights_plain_relu_120ep.pth')

    # generate some training data
    #data_generator.generate_data(20)

    data_files = data_generator.get_data_files()
    # Training loop
    for epoch in range(80):
        print(f'Epoch {epoch + 1}:')
        epoch_bar = tqdm(total=len(data_files), desc="Batches")
        for batch in range(len(data_files)):
            # Play the game and collect training data
            #training_data = play_game_and_collect_data(model, max_moves=300)
            training_data = data_generator.load_training_data(data_files[batch])
            if training_data is None:
                continue
            # Train the model using collected data
            for state, action in training_data:
                state_tensor = preprocess_state(state).to(device)
                action_tensor = torch.tensor([action]).to(device)
                optimizer.zero_grad()
                outputs = model(state_tensor)
                loss = criterion(outputs, action_tensor)
                loss.backward()
                optimizer.step()
            epoch_bar.update()
        epoch_bar.close()
    save_weights(model, 'model_weights_plain_relu_200ep.pth')


    # Use the trained model to play the game
    game = Game()
    forced_moves, scores, max_tiles = [], [0], [np.array(game.getGrid()).flatten().max()]
    while not game.hasEnded():
        # print the grid
        grid = game.getGrid()
        for row in grid:
            print(' '.join([f'{col:^4}' for col in row]))

        # let the model predict the move
        state_tensor = preprocess_state(grid).to(device)
        outputs = model(state_tensor)
        predicted_move = Direction(torch.argmax(outputs).item())
        
        # display prediction
        print(f'step={len(game.getMoves())}  descisions={torch.Tensor.tolist(outputs)}  move={predicted_move}')

        # if the model fails to pick a valid move, force a random move on it
        if not game.attempt_move(predicted_move):
            moves = [0, 1, 2, 3]
            moves.remove(predicted_move.value)

            for _ in range(3):
                forced_move = Direction(random.choice(moves))
                if not game.attempt_move(forced_move):
                    moves.remove(forced_move.value)
                else:
                    # if managed to pick a valid move, print it as forced move
                    print(f'step={len(game.getMoves()) - 1}  forced={forced_move}')
                    break
            # append the index of the forced move, within the moves list
            forced_moves.append(len(game.getMoves()) - 1)
        # append the score after the move
        scores.append(game.getScore())
        # append the max tile after the move
        max_tiles.append(np.array(grid).flatten().max())
        #input()

    # game has ended by now, print the last grid state
    grid = game.getGrid()
    for row in grid:
        print(' '.join([f'{col:^4}' for col in row]))
    # print gameover message, and some stats
    print(f'GAME OVER.  score = {game.getScore()}')
    print(f'    max tile = {max_tiles[-1]}')
    print(f'    forced = {len(forced_moves):<4}  moves = {len(game.getMoves()):<4}  % = {len(forced_moves)/len(game.getMoves()):.3}')

    # plot game stats and save as image file 
    import graph_exporter
    graph_exporter.plot_graph(scores, game.getMoves(), forced_moves, max_tiles)
