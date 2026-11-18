# %%

import random
from src.game import Game
from pydantic import BaseModel

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

    if not all(type(x) is int for x in guess):
        return False

    return all(0 <= x < n_colors for x in guess)

# %%

def evaluate_guess(
        code : tuple[int, ...],
        guess : tuple[int, ...]) -> tuple[int, int]:

    """
    Function that returns the number of colors present in the code that are correctly placed and the number 
    of colors present in the code that are misplaced
    
    Inputs : 
        - code (tuple) : true secret sequence 
        - guess (tuple) : sequence proposed by the player 

    Output : 
        - (exact_matches, misplaced_matches) : first element = number of colors correctly placed
                                               second element = number of colors misplaced 
    
    """

    if not isinstance(code, tuple) or not isinstance(guess, tuple):
        raise ValueError("code and guess must be tuples") 

    if len(code) != len(guess):
        raise ValueError("code and guess must be the same length")

    exact_matches = 0
    misplaced_matches = 0

    remaining_colors_code = []
    remaining_colors_guess = []

    for color_code, color_guess in zip(code, guess):
        if color_code == color_guess:
            exact_matches += 1
        else:
            remaining_colors_code.append(color_code)
            remaining_colors_guess.append(color_guess)

    for color in remaining_colors_guess:
        if color in remaining_colors_code:
            misplaced_matches += 1 
            remaining_colors_code.remove(color)

    return (exact_matches, misplaced_matches)


# %%

class Mastermind(Game):

    def __init__(
            self, 
            n_colors : int = 6,
            code_length : int = 4,
            max_attempts : int = 10
    ) -> None :
        super().__init__()

        if max_attempts < 1:
            raise ValueError("max_attempts must be positive")

        self.n_colors = n_colors 
        self.code_length = code_length 
        self.max_attempts = max_attempts
        self.attempts_left = max_attempts
        self.code : tuple[int, ...] = generate_code(n_colors, code_length)
        self.history : list[tuple[tuple[int, ...], tuple[int, int]]] = [] # stores (guess, (exact_matches, misplaced_matches))


    def submit_guess(
            self,
            guess : tuple[int, ...]
    ) -> tuple[int, int]:

        if self.status != "playing":
            raise ValueError("The game is over")

        if not validate_guess(guess, self.n_colors, self.code_length):
            raise ValueError("The guess is not valid")

        result = evaluate_guess(self.code, guess)
        self.history.append((guess, result))
        self.attempts_left -= 1

        if result[0] == self.code_length: # nb of exact_matches = length of code
            self.status = "won"

        elif len(self.history) >= self.max_attempts:
            self.status = "lost"

        return result

class MastermindConfig(BaseModel):
    n_colors: int = 6
    code_length: int = 4
    max_attempts: int = 10
    
class MastermindInput(BaseModel):
    guess: list[int]
    

    