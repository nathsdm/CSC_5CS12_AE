from collections import Counter
from typing import Union, Literal
from pydantic import BaseModel

from ..game import Game
from .utils import N, check_target, check_guess_list, check_guess_len

# Class
class Wordle(Game):

    def __init__(self, target: str, mode: str) -> None:
        super().__init__()

        if not check_target(target):
            raise ValueError(f"Invalid target {target!r}: expected a valid {N}-letter word from the list.")
        
        self.target: str = target
        self.attempts = 0
        self.max_attempts = 6

        if mode not in {"normal", "hard", "super-hard"}:
            raise ValueError("Invalid mode: expected 'normal', 'hard' or 'super-hard'")
        
        self.mode: str = mode

        # For hard and super-hard mode only
        self.constraints = {
            "🟩": {}, 
            "🟧": {}, 
            "⬛": set() 
        }

    def assess_guess(self, guess: str) -> dict[int, dict[str, str]]:
        """
        Take a 5-letter word and assess if:
            - its letters feature in the target word;
            - the positions of its letters correspond to the ones in the target word.

        Args:
            - guess: str -> player's input

        Return:
        A dictionary of the type {0: {"h": "🟩"}, 1: {"e": "🟧"}, etc.}.
        """
        response = {i: {letter: "⬛"} for i, letter in enumerate(guess)}
        target_count = Counter(self.target)

        # Reserve exact matches before assigning orange letters
        for i, guess_letter in enumerate(guess):
            
            if guess_letter == self.target[i]:
                response[i] = {guess_letter: "🟩"}
                target_count[guess_letter] -= 1

        # Only remaining occurrences can be orange; extras stay grey
        for i, guess_letter in enumerate(guess):
            
            if response[i][guess_letter] == "🟩":
                continue
            
            if target_count[guess_letter] > 0:
                response[i] = {guess_letter: "🟧"}
                target_count[guess_letter] -= 1

        return response

    def display_response(self, guess: str) -> None:
        """
        Display the answer nicely.
        
        Print example:  A  R  I  S  E
                        🟩 🟧 ⬛ ⬛ 🟩
        """
        response = self.assess_guess(guess)

        guess_letters = list(guess.upper())
        display_letters = "  ".join(guess_letters)
        colors = " ".join(next(iter(response[i].values())) for i in sorted(response))

        print(display_letters)
        print(colors)
        print("\n")

    def update_constraints(self, guess: str) -> dict[str, Union[dict[str, set], set]]:
        """
        Store orange and green letters for the player to reuse them in next guesses.
        For hard and super-hard mode only.

        Args:
            - response: list[dict[str, str]], guess assessment returned by assess_guess.

        Return: 
            - a dictionary returning the updated constraints.
        """
        response = self.assess_guess(guess)

        present_letters = {
            letter for i, letter in enumerate(guess)
            if response[i][letter] != "⬛"
        }
        self.constraints["⬛"].difference_update(present_letters)

        for i, guess_letter in enumerate(guess):

            color = response[i][guess_letter]

            # The i associated with a green letter indicates that the same letter should be used at the same position i
            if color == "🟩":
                self.constraints["🟩"][guess_letter] = i

            # The i associated with an orange letter indicates that the same letter sould not be used at position i
            elif color == "🟧":
                if guess_letter not in self.constraints["🟧"]:
                    self.constraints["🟧"][guess_letter] = set()

                self.constraints["🟧"][guess_letter].add(i)

            elif guess_letter not in present_letters:
                self.constraints["⬛"].add(guess_letter)

        return self.constraints

    def is_admissible(self, guess: str) -> bool:
        """
        Check if the guess is admissible ie satisfies the potential constraints.
        
        Return:
            - True if it does ;
            - False if it does not.
        """

        green = self.constraints["🟩"]
        orange = self.constraints["🟧"]
        grey = self.constraints["⬛"]

        # Normal mode, no constraints
        if self.mode == "normal":
            return True

        # Hard mode: any revealed hints must be used in subsequent guesses
        if self.mode in {"hard", "super-hard"}:
            green_letters = list(green.keys())
            orange_letters = list(orange.keys())

            if any(letter not in guess for letter in green_letters + orange_letters):
                print(f"Revealed hints must be used in your guess.")
                return False

        # Super hard mode:
        # - green letters must be reused at the same position
        # - orange letters must be reused at a different position
        # - grey letters must not be reused
        if self.mode == "super-hard":

            # Check required positions, even when the letter is missing.
            for letter, position in green.items():
                if position >= len(guess) or guess[position] != letter:
                    print(f"The letter {letter} must be in position {position}.")
                    return False

            for i, letter in enumerate(guess):
                # A letter can have both green and orange hints.
                if letter in orange and i in orange[letter]:
                    print(f"The letter {letter} is misplaced.")
                    return False

                if letter in grey:
                    print(f"You cannot use {letter} anymore.")
                    return False

        return True

    def play_turn(self, guess: str) -> None:
        """
        Simulate one round of the game:
            - Check if the guess is admissible ;
            - Assess the guess compared to target ;
            - Update the constraints accordingly ;
            - Add 1 to the number of attempts.
        """
        if self.status != "playing":
            return

        if not check_guess_len(guess):
            print(f"Your guess does not have {N} letters.")
            return

        if not check_guess_list(guess):
            print(f"Guess not in list.")
            return
        
        if not self.is_admissible(guess):
            print("Your guess does not comply with constraints.")
            return

        response = self.assess_guess(guess)
        self.display_response(guess)
        self.update_constraints(guess)
        self.attempts += 1

        if guess == self.target:
            self.status = "won"
        elif self.attempts >= self.max_attempts:
            self.status = "lost"

    def play(self):
        """Simulate all the rounds in the game."""

        while self.attempts < self.max_attempts:

            print(f"Guess {self.attempts + 1}")
            guess = input(f"Enter your guess: ").lower()

            if not guess:
                print("Game stopped.")
                return
            
            self.play_turn(guess)

            if guess == self.target:
                print("Congratulations, you've won!")
                self.status = "won"
                return
        
        print(f"Game over! The word was {self.target}")
        self.status = "lost"

class WordleConfig(BaseModel):
    mode: Literal["normal", "hard", "super-hard"] = "normal"

class WordleInput(BaseModel):
    guess: str