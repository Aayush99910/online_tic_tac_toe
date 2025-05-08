# type: ignore
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from manager.RoomManager import RoomManager
import json 

app = FastAPI()

# Allow CORS for all domains (you can restrict this if you need to)
app.add_middleware(
   CORSMiddleware,
   allow_origins=["*"],  # Allows all origins (use specific URLs in production)
   allow_credentials=True,
   allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
   allow_headers=["*"],  # Allows all headers
)

# global room manager object
app.room_manager = RoomManager()

# builing a response to avoid repitition
def build_response(message: str, room: object, win: bool, draw: bool, valid: bool) -> dict:
    return {
        "symbol": room["symbol"],
        "status": 0,
        "valid": valid,
        "message": message,
        "win": win,
        "draw": draw,
        "board": room["board"].getBoard(),
        "current_player": room["current_player"]
    }


# make move function 
async def make_move(row: int, col: int, user_id: str, websocket: WebSocket):
    # getting that room id 
    room_id = app.room_manager.get_room_id_with_websocket(websocket)
    if not room_id:
        await websocket.send_json({"valid": False, "message": "Room not found."})
        return
    
    # getting that room
    room = app.room_manager.get_room_with_id(room_id)
    if not room:
        await websocket.send_json({"valid": False, "message": "Invalid room."})
        return
    
    # current player 
    current_player = room["current_player"]
    symbol = room["symbol"]
    symbol_to_move = symbol[user_id]

    if current_player == symbol_to_move:
        # get the gameboard
        board = room["board"]

        # making a move
        if board.playerMakeMove(row, col, symbol_to_move):
            # need to change the current_player to another player 
            room["current_player"] = 'O' if room["current_player"] == 'X' else 'X'

            # three condition 
            # win
            if board.hasWon():
                res = build_response(f"Player {symbol_to_move} won!", room, True, False, True) 
            # draw
            elif board.isDraw():
                res =  build_response("It is a tie game!", room, False, True, True)
            else:
                # normal move
                res =  build_response(f"Player {symbol_to_move} made a move!", room, False, False, True)
                
            # boardcast to all players in that room
            for websocket_object in room["websocket_objects"]:
                await websocket_object.send_json(res)
        else:
            res = build_response("Invalid move. Please try again!", room, False, False, False)
            await websocket.send_json(res)
    else:
        res = build_response("It's not your turn.", room, False, False, False)
        await websocket.send_json(res)


# Home page for welcoming the users
@app.get("/")
def home_page():
    unique_user_id = app.room_manager.generate_user_id() 
    return {
        "user_id": unique_user_id,
        "message": "Welcome to multiplayer tic tac toe game!"
    }


# Initialize the game
# [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
@app.websocket("/ws/{player_id}")
async def websocket_endpoint(player_id: str, player_websocket: WebSocket):
    try:
        # accept websocket request
        await player_websocket.accept()

        # add the player to a players queue 
        # if a room is created then start the game or else send a waiting message
        room_id = app.room_manager.add_player_to_queue(player_id, player_websocket)
        
        if room_id:
            # getting the room information 
            room = app.room_manager.get_room_with_id(room_id)

            # start the game
            for websocket_object in room["websocket_objects"]:
                await websocket_object.send_json({
                    "status": 0,
                    "message": "Game started",
                    "board": room["board"].getBoard(),
                    "symbol": room["symbol"],
                    "current_player": room["current_player"]
                })

        else:
            # waiting there is no match 
            await player_websocket.send_json({
                "status": 1,
                "message": "Waiting for other player to join"
            })

        try:
            while True:
                data = json.loads(await player_websocket.receive_text())
                row = int(data['row'])
                col = int(data['col'])
                user_id = str(data['user_id'])
                await make_move(row, col, user_id, player_websocket)
        except WebSocketDisconnect:
            pass 
            # app.room_manager.remove_from_queue(player_id)
    except AttributeError as e:
        raise HTTPException(status_code=500, detail=f"Function missing: {str(e)}")
    except NameError as e:
        raise HTTPException(status_code=500, detail=f"Game logic module issue: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")
    