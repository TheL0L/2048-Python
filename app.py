import game as Game
import ai_agent as Agent
import matplotlib.pyplot as plt

def displayScoreGraph(data_points):
    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.title('Score as a function of Steps')
    plt.xlabel('Step')
    plt.ylabel('Score')
    plt.grid(True)
    plt.plot(data_points, color='blue')


if __name__ == '__main__':
    game = Game(seed=47368211)

    agent = Agent.model()

    history = {}
    step = 0
    while not game.isOver():
        current_move = agent.getMove(state=game.getBoard())
        game.forwardInput(move=current_move)
        history[step] = game.getScore()
        step += 1
    
    displayScoreGraph(history.items())
    