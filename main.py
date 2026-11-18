import uuid
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse

# Import des jeux
from src.game import Game
from src.mastermind.game import Mastermind, MastermindConfig, MastermindInput

app = FastAPI()

# ==========================================
# ROUTES HTML (Ton code)
# ==========================================

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

# Base de données temporaire pour stocker les parties en cours sur les différents jeux.
games_db: dict[str, Game] = {}

# ========================================== #
#                 MASTERMIND                 #
# ========================================== #

@app.post("/api/mastermind/create")
def create_game(config: MastermindConfig):
    game_id = str(uuid.uuid4())
    games_db[game_id] = Mastermind(config.n_colors, config.code_length, config.max_attempts)
    return {"game_id": game_id, "message": "Partie créée"}

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