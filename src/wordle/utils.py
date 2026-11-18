from pathlib import Path
import random

N = 5

words_path = Path(__file__).parent / "words.txt"
with open(words_path, mode="r", encoding="utf-8") as f:
    VALID_WORDS = f.read().splitlines()

def choose_target() -> str:
    """At each game start, choose a target at random among the valid words."""
    return random.choice(list(VALID_WORDS))

def check_target(target: str) -> bool:
    """Check if the target is a 5-letter word and is in the list of valid words."""
    return (len(target) == N) & (target in VALID_WORDS)

def check_guess_len(guess: str) -> bool:
    """Check if the guess is a 5-letter word."""
    return(len(guess) == N)

def check_guess_list(guess: str) -> bool:
    """Check if guess is in the list of valid words."""
    return (guess in VALID_WORDS)