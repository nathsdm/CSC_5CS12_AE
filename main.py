import uuid
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse

# Import des jeux
from src.game import Game
from src.mastermind.game import Mastermind, MastermindConfig, MastermindInput
from src.wordle.game import Wordle, WordleConfig, WordleInput
from src.sudoku.sudoku import Sudoku, SudokuConfig, SudokuInput

app = FastAPI()

# ========================================== #
#                  ROUTES                    #
# ========================================== #

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    with open("./src/index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/mastermind", response_class=HTMLResponse)
async def read_mastermind(request: Request):
    with open("./src/mastermind/game.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/wordle", response_class=HTMLResponse)
async def read_wordle(request: Request):
    with open("./src/wordle/game.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/sudoku", response_class=HTMLResponse)
async def read_sudoku(request: Request):
    with open("./src/sudoku/game.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

# Base de données temporaire pour stocker les parties en cours sur les différents jeux
games_db: dict[str, Game] = {}

# ========================================== #
#                 MASTERMIND                 #
# ========================================== #

@app.post("/api/mastermind/create")
def create_game(config: MastermindConfig):
    game_id = str(uuid.uuid4())
    games_db[game_id] = Mastermind(config.n_colors, config.code_length, config.max_attempts)
    return {"game_id": game_id, "message": "Partie Mastermind créée"}

@app.post("/api/mastermind/{game_id}/guess")
def make_guess(game_id: str, guess_input: MastermindInput):
    if game_id not in games_db:
        raise HTTPException(status_code=404, detail="Partie introuvable")
    
    game = games_db[game_id]
    if not isinstance(game, Mastermind):
        raise HTTPException(status_code=400, detail="Ce jeu n'est pas un Mastermind")
    
    try:
        exact, misplaced = game.submit_guess(tuple(guess_input.guess))
        attempts_left = game.attempts_left
        status = game.status
        return {
            "exact_matches": exact,
            "misplaced_matches": misplaced,
            "attempts_left": attempts_left,
            "status": status
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# ========================================== #
#                  WORDLE                    #
# ========================================== #

@app.post("/api/wordle/create")
def create_wordle_game(config: WordleConfig):
    game_id = str(uuid.uuid4())
    games_db[game_id] = Wordle(config.target, config.mode)
    return {"game_id": game_id, "message": "Partie Wordle créée"}

@app.post("/api/wordle/{game_id}/guess")
def make_wordle_guess(game_id: str, guess_input: WordleInput):
    if game_id not in games_db:
        raise HTTPException(status_code=404, detail="Partie introuvable")
    
    game = games_db[game_id]
    if not isinstance(game, Wordle):
        raise HTTPException(status_code=400, detail="Ce jeu n'est pas un Wordle")
    
    try:
        guess = guess_input.guess.lower()

        if not game.is_admissible(guess):
            raise ValueError("Le mot proposé n'est pas valide.")

        wordle_result = game.assess_guess(guess)
        game.update_constraints(guess)
        game.attempts += 1
        
        # Update game status based on the guess
        if guess_input.guess == game.target:
            game.status = "won"
        elif game.attempts >= game.max_attempts:
            game.status = "lost"
        
        return {
            "wordle_result": wordle_result,
            "attempts": game.attempts,
            "status": game.status
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ========================================== #
#                  SUDOKU                    #
# ========================================== #

@app.post("/api/sudoku/create")
def create_sudoku_game(config: SudokuConfig):
    game_id = str(uuid.uuid4())
    game = Sudoku(config.difficulty)
    games_db[game_id] = game
    return {"game_id": game_id, "grid": game.sudoku, "message": "Partie Sudoku créée"}

@app.post("/api/sudoku/{game_id}/check")
def check_sudoku_solution(game_id: str, sudoku_input: SudokuInput):
    if game_id not in games_db:
        raise HTTPException(status_code=404, detail="Partie introuvable")

    game = games_db[game_id]
    if not isinstance(game, Sudoku):
        raise HTTPException(status_code=400, detail="Ce jeu n'est pas un Sudoku")

    board = sudoku_input.board
    solved = game.checkPlayerSolution(board)
    return {
        "solved": solved,
        "errors": game.findErrors(board),
        "status": game.status
    }