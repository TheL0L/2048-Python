import matplotlib.pyplot as plt
import os
import time

ROOT_EXPORT_PATH = './model_runs'

def plot_graph(scores, moves, forced, max_tiles):
    # Create subplots
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))

    # Plot Score(move) graph
    axs[0, 0].plot(range(len(scores)), scores, linestyle='-', color='C0')
    axs[0, 0].set_title('Graph A: Score(move)')
    # Adding red markers (X) for forced moves
    for move in forced:
        axs[0, 0].scatter(move + 1, scores[move + 1], color='C3', marker='X', zorder=10)

    # Plot MaxTile(move) graph
    axs[0, 1].plot(range(len(max_tiles)), max_tiles, linestyle='-', color='C1')
    axs[0, 1].set_title('Graph B: MaxTile(move)')

    # Prepare moves distribution data
    moves_dict = {'UP': 0, 'RIGHT': 0, 'DOWN': 0, 'LEFT': 0}
    for move in moves:
        moves_dict[move.name] += 1

    labels = list(moves_dict.keys())
    values = list(moves_dict.values())

    forced_dict = {'UP': 0, 'RIGHT': 0, 'DOWN': 0, 'LEFT': 0}
    for fmove in forced:
        forced_dict[moves[fmove].name] += 1
    forced_values = list(forced_dict.values())

    # Plot graph C moves distribution
    axs[1, 0].bar(labels, values)
    axs[1, 0].bar(labels, forced_values, color='red')
    axs[1, 0].set_title('Graph C: Distribution of moves')

    # Add custom legend in the bottom right corner
    legend_elements = [
        plt.Line2D([0], [0], marker='X', color='C0', markerfacecolor='C3', markersize=10, label='forced moves'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='C0', markersize=10, label='moves distribution'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='C3', markersize=10, label='forced moves distribution'),
    ]
    axs[1, 1].legend(handles=legend_elements, loc='center', title='Legend')
    axs[1, 1].axis('off')

    # Adjust layout
    plt.tight_layout()

    # Saving the graph
    if not os.path.exists(ROOT_EXPORT_PATH):
        os.makedirs(ROOT_EXPORT_PATH)

    figure_path = os.path.join(ROOT_EXPORT_PATH, f'run_{time.time()}.png')
    plt.savefig(figure_path)
    print(f'graph was saved at: {figure_path}')
    plt.close()

