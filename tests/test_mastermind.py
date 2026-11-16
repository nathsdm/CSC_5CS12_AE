# %%

import pytest

from mastermind.game import generate_code, validate_guess

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