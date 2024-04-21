# 2048-Python

A python clone of the game [2048](https://github.com/gabrielecirulli/2048) by [Gabriele Cirulli](https://github.com/gabrielecirulli),
written to compare the expectimax algorithm agaist a custom neural network.

## How to Use

To use this repository, follow these steps:

1. **Clone the Repository**: Clone this repository to your local machine using `git clone https://github.com/TheL0L/2048-Python.git`.

2. **Optional: Create a Virtual Environment**: Make sure you have Python installed on your machine. It's recommended to use a virtual environment to manage dependencies.
    - Navigating to the project directory.
    - Create a virtual environment using `python -m venv env`.

3. **Install Dependencies**: Install the project dependencies by running `pip install -r requirements.txt`.
    - In case you're planning on training models, consider installing a version of `torch` that supports GPU usage, you can find more details [here](https://pytorch.org/get-started/locally/).

4. **Optional: Modify Constants**: If desired, you can modify the constants in `constants.py` to customize the game settings according to your preferences.

5. **Optional: Modify Agent**: You can choose the AI agent to play the game by modifying the `AGENT` variable in `app.py`.

6. **Run the Application**: Start the game by running `app.py`.


## License

This project is licensed under the [MIT License](LICENSE).
