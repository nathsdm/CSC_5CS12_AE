from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    with open("./src/index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/game_example", response_class=HTMLResponse)
async def read_game_example(request: Request):
    with open("./src/game_example/game.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)
    