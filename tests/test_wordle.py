# %%

import pytest
from copy import deepcopy

from wordle.game import Wordle
from src.wordle.utils import (
    N,
    VALID_WORDS,
    choose_target,
    check_guess_len,
    check_guess_list,
)

# %%

def test_choose_target():
    for _ in range(20): # Choose a target 20 times at random
        target = choose_target()

        assert isinstance(target, str)
        assert len(target) == N
        assert target.isalpha()
        assert target in VALID_WORDS

def test_invalid_mode():

    with pytest.raises(ValueError):
        Wordle(target="hello", mode="easy") # Not in admissible modes

    with pytest.raises(ValueError):
        Wordle(target="hello", mode="hard ") # Unexpected space

    with pytest.raises(ValueError):
        Wordle(target="hello", mode="super hard") # "-" missing

def test_normal_mode():
    assert not check_guess_len(guess="please") # Does not have 5 letters
    assert not check_guess_list(guess="hjloa") # Does not exist / not in list
    assert check_guess_list(guess="arise")


def test_invalid_target():
    with pytest.raises(ValueError, match="Invalid target"):
        Wordle(target="please", mode="normal")

    with pytest.raises(ValueError, match="Invalid target"):
        Wordle(target="hjloa", mode="normal")


def test_invalid_guess_preserves_state():
    game = Wordle(target="hello", mode="normal")
    game.play_turn("arise")
    before = deepcopy(game.constraints)

    for guess in ["", "please", "hjloa"]:
        game.play_turn(guess)
        assert game.attempts == 1
        assert game.status == "playing"
        assert game.constraints == before


def test_normal_mode_ignores_hints():
    game = Wordle(target="hello", mode="normal")
    game.play_turn("arise")
    game.play_turn("mount")  # Accepted even though the revealed e is missing.

    assert game.attempts == 2
    assert game.status == "playing"


def test_no_turn_after_win():
    game = Wordle(target="hello", mode="normal")
    game.play_turn("hello")
    before = deepcopy(game.constraints)

    game.play_turn("mount")

    assert game.attempts == 1
    assert game.status == "won"
    assert game.constraints == before


def test_no_turn_after_loss():
    game = Wordle(target="hello", mode="normal")
    for _ in range(game.max_attempts):
        game.play_turn("arise")
    before = deepcopy(game.constraints)

    game.play_turn("hello")

    assert game.attempts == game.max_attempts
    assert game.status == "lost"
    assert game.constraints == before

# %%

def test_hard_mode():
    game = Wordle(target="hello", mode="hard")

    # Round 1: guess finds that "e" is present
    game.play_turn(guess="arise")
    assert game.attempts == 1
    assert game.constraints["🟧"]["e"] == {4}

    # A future guess without "e" should be turned down
    before = deepcopy(game.constraints)
    game.play_turn(guess="mount")
    assert game.attempts == 1
    assert game.constraints == before

    # Round 2: "level" contains "e" so it's accepted
    game.play_turn("level")
    assert game.attempts == 2
    assert game.constraints["🟩"]["e"] == 1
    assert game.constraints["🟧"]["l"] == {0, 4}

    # Future guesses must now contain "e" and "l"
    assert not game.is_admissible("erase")
    assert game.is_admissible("slope")

    # "hello" must finish the game
    game.play_turn("hello")
    assert game.attempts == 3
    assert game.status == "won"

def test_super_hard_mode():
    game = Wordle(target="hello", mode="super-hard")
    
    # Round 1: guess finds that "e" is present
    game.play_turn(guess="arise")
    assert game.attempts == 1
    assert game.constraints["🟧"]["e"] == {4}
    assert game.constraints["⬛"] == {"a", "r", "i", "s"}

    # A future guess without "e" or with "e" at position 4 should be turned down
    # Same with a word that reuses grey letters
    before = deepcopy(game.constraints)
    game.play_turn(guess="mount") # "e" is not present
    game.play_turn(guess="elope") # "e" is at position 4
    game.play_turn(guess="fiery") # "r" is reused
    assert game.attempts == 1
    assert game.constraints == before

    # Round 2: "level" contains "e" at a different position so it's accepted
    game.play_turn("level")
    assert game.attempts == 2
    assert game.constraints["🟩"]["e"] == 1
    assert game.constraints["🟧"]["l"] == {0, 4}
    assert game.constraints["⬛"] == {"a", "r", "i", "s", "v"}

    # Future guesses must now contain "e" and "l" but careful with their positions
    assert not game.is_admissible("erase")
    assert game.is_admissible("helly")

    # "hello" must finish the game
    game.play_turn("hello")
    assert game.attempts == 3
    assert game.status == "won"

def test_repeated_letters():
    game = Wordle(target="hello", mode="normal")

    assert game.assess_guess("level") == {
        0: {"l": "🟧"},
        1: {"e": "🟩"},
        2: {"v": "⬛"},
        3: {"e": "⬛"},
        4: {"l": "🟧"},
    }

def test_super_hard_green_position_and_orange_hints():
    game = Wordle(target="hello", mode="super-hard")
    game.play_turn("arise")
    game.play_turn("level")

    assert not game.is_admissible("holly")  # Required green e is missing.
    assert not game.is_admissible("olleh")  # Green e is misplaced.
    assert not game.is_admissible("lemon")  # Orange l is at a forbidden position.
    assert not game.is_admissible("helle")  # Green e must still respect orange hints.
    assert game.is_admissible("hello")

def test_win_on_last_attempt():
    game = Wordle(target="hello", mode="normal")

    for _ in range(game.max_attempts - 1):
        game.play_turn("arise")

    assert game.status == "playing"

    game.play_turn("hello")

    assert game.attempts == game.max_attempts
    assert game.status == "won"

def test_lose_game():
    game = Wordle(target="hello", mode="normal")
    
    for _ in range(game.max_attempts - 1):
        game.play_turn("arise")

    assert game.status == "playing"

    game.play_turn("arise")

    assert game.attempts == game.max_attempts
    assert game.status == "lost"
