import pytest
from src.sudoku.sudoku import DIFFICULTY, Sudoku, countSolutions


def testValidSolution():
    game = Sudoku()
    numbers = set(range(1, 10))

    for row in game.solution:
        assert set(row) == numbers

    for columns in range(9):
        assert {game.solution[row][columns] for row in range(9)} == numbers

    for row_start in range(0, 9, 3):
        for col_start in range(0, 9, 3):
            square = {
                game.solution[row][columns]
                for row in range(row_start, row_start + 3)
                for columns in range(col_start, col_start + 3)
            }
            assert square == numbers

    for row in range(9): 
        for col in range(9): 
            if game.sudoku[row][col] != 0:
                    assert game.sudoku[row][col] == game.solution[row][col]


def testUniqueSolution(): 
    game = Sudoku()
    nb_sol = countSolutions(game.sudoku)
    assert nb_sol == 1


def testDifficulty():
    for difficulty in DIFFICULTY.keys():
        game = Sudoku(difficulty)
        n_given_cells = sum(value != 0 for row in game.sudoku for value in row)
        assert DIFFICULTY[difficulty] == n_given_cells


def testFail():
    game = Sudoku()
    player_solution = [row[:] for row in game.solution]
    player_solution[1][1] = -1

    assert not game.checkPlayerSolution(player_solution)
    assert game.status == "playing"
