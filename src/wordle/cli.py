from .wordle import Wordle
from .utils import choose_target


def launch_wordle():
    """Start a new game with a randomly chosen word."""

    while True:
        mode = input("Choose a mode (normal, hard or super-hard): ")
        mode = mode.strip().lower()

        if mode in {"normal", "hard", "super-hard"}:
            break

        print("Invalid mode.")
    
    game = Wordle(target=choose_target(), mode=mode)
    game.play()
