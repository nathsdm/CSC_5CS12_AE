import random
from typing import Literal
from pydantic import BaseModel
from src.game import Game


#################### PARAMETERS ######################

DIFFICULTY = {
    "easy": 45,
    "normal": 35,
    "hard": 30,
}

######################################################


def isValid(board, row, col, num):
    for i in range(9):
        # Check row
        if board[row][i] == num:
            return False

        # Check column
        if board[i][col] == num:
            return False

        # Check 3 x 3 box
        boxRow = 3 * (row // 3) + i // 3
        boxCol = 3 * (col // 3) + i % 3

        if board[boxRow][boxCol] == num:
            return False

    return True


def countSolutions(board):

    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                nb_sol = 0

                for val in range(1, 10):
                    if isValid(board, row, col, val):
                        board[row][col] = val
                        nb_sol += countSolutions(board)
                        board[row][col] = 0

                        if nb_sol > 1:
                            return nb_sol

                return nb_sol

    return 1


def hasUniqueSolution(board):
    return countSolutions(board) == 1


def fillBoard(board):

    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                values = list(range(1, 10))
                random.shuffle(values)

                for num in values:
                    if isValid(board, row, col, num):
                        board[row][col] = num

                        if fillBoard(board):
                            return True

                        board[row][col] = 0

                return False

    return True


def generateCompleteBoard():
    board = [[0] * 9 for _ in range(9)]
    fillBoard(board)
    return board


def generateSudoku(difficulty):
    n_given_cells = DIFFICULTY[difficulty]

    for _ in range(50):
        solution = generateCompleteBoard()
        sudoku = [row[:] for row in solution]

        cells = [(row, column) for row in range(9) for column in range(9)]
        random.shuffle(cells)
        filled_cells = 9 * 9

        for row, column in cells:
            value = sudoku[row][column]
            sudoku[row][column] = 0

            if hasUniqueSolution(sudoku):
                filled_cells -= 1
                if filled_cells == n_given_cells:
                    return sudoku, solution

            else:
                sudoku[row][column] = value

    raise RuntimeError(f"Runtime Error")


class Sudoku(Game):
    def __init__(self, difficulty="easy"):
        super().__init__()
        self.difficulty = difficulty
        self.status = "playing"
        self.sudoku, self.solution = generateSudoku(difficulty)

    def checkPlayerSolution(self, player_solution):
        if self.solution == player_solution:
            self.status = "won"
            return True
        else:
            return False

    def findErrors(self, player_solution):
        errors = []

        for row in range(9):
            for col in range(9):
                value = player_solution[row][col]
                if value != self.solution[row][col]:
                    errors.append([row, col])
        return errors


class SudokuConfig(BaseModel):
    difficulty: Literal["easy", "normal", "hard"] = "easy"


class SudokuInput(BaseModel):
    board: list[list[int]]
