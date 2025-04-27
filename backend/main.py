# type: ignore
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sys
import json
import random 

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

# global variable 
room = {
    "current_player": 'X'
}
first_player = True

# make move function 
async def make_move(row: int, col: int, websocket: WebSocket):
    current_player = room["current_player"]

    if gamelogic.playerMakeMove(row, col, current_player):
        if gamelogic.hasWon():
            response1 = {
                "message": f"Player {current_player} wins!",
                "valid": True,
                "win": True,
                "draw": False, 
                "board": gamelogic.getBoard()
            }

        elif gamelogic.isDraw():
            response1 = {
                "message": "It a tie!",
                "valid": True,
                "win": False,
                "draw": True, 
                "board": gamelogic.getBoard()
            }
        else:
            room["current_player"] = 'O' if current_player == 'X' else 'X'
            response1 = {
                "message": f"Player {current_player} made a move!",
                "valid": True,
                "win": False,
                "draw": False, 
                "board": gamelogic.getBoard(),
                "current_player": room["current_player"]
            }

        # Broadcast to all players in the room
        for player in room["players_array"]:
            await player.send_json(response1)
    else:
        response1 = {
            "message": "Invalid Move! Please try again!",
            "valid": False,
            "win": False,
            "draw": False, 
            "board": gamelogic.getBoard(),
            "current_player": room["current_player"]
        }
        await websocket.send_json(response1)


# adding the websocket connection so that two people can see the board in real time
@app.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    global room 
    await websocket.accept()
    
    if len(room) == 1:
        room = {
            "current_player": 'X',
            "player_X": websocket,
            "player_O": None, 
            "players_array": [websocket]
        }
    else:
        room["players_array"].append(websocket)
        room["player_O"] = websocket

    while True:
        data = json.loads(await websocket.receive_text())
        row = int(data["row"])
        col = int(data["col"])
        await make_move(row, col, websocket)


# Home page for welcoming the users
@app.get("/")
def home_page():
    return {"message": "Welcome to multiplayer tic tac toe game!"}


# Initialize the game
# [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
@app.post("/start")
def start_game():
    try:
        global first_player, room
        
        if first_player:
            symbol = "X"
            first_player = False 
        else:
            symbol = "O"

        gamelogic.initializeBoard()
        return {
            "message": "Game started", 
            "board": gamelogic.getBoard(), 
            "you_are": symbol, 
            "current_player": room["current_player"]
        }
    
    except AttributeError as e:
        raise HTTPException(status_code=500, detail=f"Function missing: {str(e)}")
    except NameError as e:
        raise HTTPException(status_code=500, detail=f"Game logic module issue: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")
    

# Get the current board state
@app.get("/board")
def get_board():
    return {"board": gamelogic.getBoard()}
