# type: ignore
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys

# Import the C++ module
sys.path.append('../src/build')
import gamelogic

app = FastAPI()

# Allow CORS for all domains (you can restrict this if you need to)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (use specific URLs in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Home page for welcoming the users
@app.get("/")
def home_page():
    return {"message": "Welcome to multiplayer tic tac toe game!"}

# Initialize the game
# [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
@app.post("/start")
def start_game():
    gamelogic.initializeBoard()
    return {"message": "Game started", "board": gamelogic.getBoard()}

# Make a move
@app.post("/move/{row}/{col}")
def make_move(row: int, col: int, player: str):
    if gamelogic.playerMakeMove(row, col, player):
      if gamelogic.hasWon():
        return {"message": f"Player {player} wins!", "win": True, "valid": True, "draw": False, "board": gamelogic.getBoard()}
      if gamelogic.isDraw():
        return {"message": "It's a draw!", "win": False, "valid": True, "draw": True, "board": gamelogic.getBoard()}
      return {"message": "Move successful", "valid": True, "win": False, "draw": False, "board": gamelogic.getBoard()}
  
    return {"message": "Invalid move", "valid": False, "win": False, "draw": False, "board": gamelogic.getBoard()}



# Get the current board state
@app.get("/board")
def get_board():
    return {"board": gamelogic.getBoard()}
