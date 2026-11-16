# %%

import pytest

from mastermind.game import generate_code

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