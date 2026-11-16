# %%

import random

# %%

def generate_code(
        n_colors : int = 6, 
        code_length : int = 4) -> tuple[int, ...]:
    """
    Function that generates a secret combination

    Inputs : 
        - n_colors (int) : number of available colors for the code
        - code_length (int) : length of the code 
    Output : 
        - code (tuple) : combination of random colors
    """

    if n_colors <= 0:
        raise ValueError("n_colors must be positive")

    if code_length <= 0:
        raise ValueError("code_length must be positive")

    code = []
    for _ in range(code_length):
        code.append(random.randint(0, n_colors-1))
    return tuple(code)

# %%

def validate_guess(
        guess : tuple[int, ...],
        n_colors : int = 6,
        code_length : int = 4) -> bool : 

    """
    Function that checks if a combination is valid or not
    A combination is valid if :
        - It has code_length colors in it 
        - All element in the guess are integers greater than or equal to 0 and strictly lower than n_colors

    Inputs : 
        - guess (tuple) : guess of the player 
        - n_colors (int) : number of available colors for the code
        - code_length (int) : length of the code 

    Output : 
        - bool : true if valid, else False
    """

    if n_colors <= 0:
            raise ValueError("n_colors must be positive")
    
    if code_length <= 0:
        raise ValueError("code_length must be positive")

    if not isinstance(guess, tuple):
        raise ValueError("guess must a tuple")

    if len(guess) != code_length:
        return False

    if not all(isinstance(x, int) for x in guess):
        return False

    return all(0 <= x < n_colors for x in guess)

# %%

