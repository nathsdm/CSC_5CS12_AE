from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Le serveur Docker tourne parfaitement !"}

@app.get("/home")
def read_home():
    return {"message": "Test"}