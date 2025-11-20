import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.game import Game

if __name__ == "__main__":
    game = Game()
    game.run()
