# type: ignore
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sys
import json

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

# adding the websocket connection so that two people can see the board in real time
@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int):
    await websocket.accept()

    while True:
        data = json.loads(await websocket.receive_text())
        row = int(data["row"])
        col = int(data["col"])
        print(row, col)
        await websocket.send_json({"message": "Works"})

# Home page for welcoming the users
@app.get("/")
def home_page():
    return {"message": "Welcome to multiplayer tic tac toe game!"}

# Initialize the game
# [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
@app.post("/start")
def start_game():
    try:    
        gamelogic.initializeBoard()
        return {"message": "Game started", "board": gamelogic.getBoard()}
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
