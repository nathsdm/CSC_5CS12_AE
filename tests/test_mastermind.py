# %%

import pytest

from mastermind.game import Mastermind, evaluate_guess, generate_code, validate_guess

# %%

def test_generate_code_default():

    code = generate_code()
    assert isinstance(code, tuple)
    assert len(code) == 4 
    assert all(0 <= x < 6 for x in code)

def test_generate_code_single_color():

    code = generate_code(n_colors=1, code_length=4)
    assert code == (0,0,0,0)

def test_generate_code_custom_param():

    code = generate_code(n_colors=4, code_length=8)
    assert len(code) == 8
    assert all(0 <= x < 4 for x in code)

def test_generate_code_invalid_params():

    with pytest.raises(ValueError):
        generate_code(n_colors=-1)

    with pytest.raises(ValueError):
        generate_code(code_length=-1)

# %%

def test_validate_guess():

    assert validate_guess(guess=(0,1,2,3), n_colors=4, code_length=4)
    assert not validate_guess(guess=(0,1,2,3,4), n_colors=4, code_length=4)
    assert not validate_guess(guess=(0,1,2,4), n_colors=4, code_length=4)
    assert not validate_guess(guess=(0,1,2,-3), n_colors=4, code_length=4)
    assert not validate_guess(guess=(0,1,2.5,3), n_colors=4, code_length=4)
    assert not validate_guess(guess=(0,1,2,"red"), n_colors=4, code_length=4)

def test_validate_guess_invalid_params():

    with pytest.raises(ValueError):
        validate_guess(guess=3, n_colors=1, code_length=1)

    with pytest.raises(ValueError):
        validate_guess(n_colors=-1, guess=(0,))

    with pytest.raises(ValueError):
        validate_guess(code_length=-1, guess=(0,))

# %%

def test_evaluate_guess():

    assert evaluate_guess(code=(0,1,0,2), guess=(1,2,3,3)) == (0,2)
    assert evaluate_guess(code=(0,1,0,2), guess=(0,1,0,2)) == (4,0)
    assert evaluate_guess(code=(0,1,0,2), guess=(2,0,1,0)) == (0,4)
    assert evaluate_guess(code=(0,1,0,2), guess=(0,4,1,3)) == (1,1)
    assert evaluate_guess(code=(0,1,0,2), guess=(3,3,3,3)) == (0,0)

def test_evaluate_guess_invalid_params():

    with pytest.raises(ValueError):
        evaluate_guess(code=[0,1], guess=(0,1))

    with pytest.raises(ValueError):
        evaluate_guess(code=(0,1), guess=[0,1])

    with pytest.raises(ValueError):
        evaluate_guess(code=[0,1], guess=[0,1])

    with pytest.raises(ValueError):
        evaluate_guess(code=(0,1,2,3), guess=(0,1,2))

# %%

def test_mastermind_init():

    game = Mastermind(n_colors=4, code_length=3, max_attempts=5)
    assert game.n_colors == 4
    assert game.code_length == 3
    assert game.max_attempts == 5
    assert len(game.code) == 3
    assert game.history == []
    assert game.status == "playing"

def test_mastermind_invalid_init():

    with pytest.raises(ValueError):
        Mastermind(max_attempts=0)

    with pytest.raises(ValueError):
        Mastermind(max_attempts=-1)

def test_mastermind_submit_guess():

    game = Mastermind()
    game.code = (0,1,2,3)

    result = game.submit_guess((0,2,1,4))

    assert result == (1,2)
    assert game.history == [((0,2,1,4), (1,2))]
    assert game.status == "playing"


def test_mastermind_invalid_guess():

    game = Mastermind()
    game.code = (0,1,2,3)

    with pytest.raises(ValueError):
        game.submit_guess((0,1,2,6))

    assert game.history == []
    assert game.status == "playing"

def test_mastermind_win():

    game = Mastermind(max_attempts=1)
    game.code = (0,1,2,3)

    result = game.submit_guess((0,1,2,3))

    assert result == (4,0)
    assert game.status == "won"
    assert len(game.history) == 1

    with pytest.raises(ValueError): 
        game.submit_guess((0,1,2,3))

def test_mastermind_loss():

    game = Mastermind(max_attempts=2)
    game.code = (0,1,2,3)

    game.submit_guess((4,4,4,4))

    assert game.status == "playing"
    assert len(game.history) == 1

    game.submit_guess((5,5,5,5))

    assert game.status == "lost"
    assert len(game.history) == 2

    with pytest.raises(ValueError):
        game.submit_guess((0,1,2,3))