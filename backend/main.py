# type: ignore
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from manager.RoomManager import RoomManager
import json 
import asyncio

app = FastAPI()

# Allow CORS for all domains (you can restrict this if you need to)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Explicitly allow your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
                
            # boardcast to all active players in that room
            for websocket_object in room["active_players_websocket_objects"]:    
                await websocket_object.send_json(res)

            for websocket_object in room["spectating_players_websocket_objects"]:
                await websocket_object.send_json({
                    "message": res["message"],
                    "board": res["board"]
                })
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
@app.websocket("/ws/play/{player_id}")
async def start_game(player_id: str, player_websocket: WebSocket):
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
            for websocket_object in room["active_players_websocket_objects"]:
                await websocket_object.send_json({
                    "status": 0,
                    "message": "Game started",
                    "board": room["board"].getBoard(),
                    "symbol": room["symbol"],
                    "current_player": room["current_player"],
                    "room_id": room_id # Testing purpose will be sending only when they create a room and not everytime
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

@app.websocket("/ws/watch/{player_id}")
async def watch_game(player_id: str, player_websocket: WebSocket, room_id: str = Query(...)):
    try:
        # accept websocket request
        await player_websocket.accept()
        
        if room_id:
            # adding this player to that room 
            app.room_manager.add_player_to_room(player_id, room_id, player_websocket)
            
            # getting that current room
            room = app.room_manager.get_room_with_id(room_id)
            await player_websocket.send_json({
                "message": f"Watching room: {room_id}",
                "board": room["board"].getBoard()  
            })

        else:
            # there is no such room available right now
            await player_websocket.send_json({
                "status": 1,
                "message": "Invalid room id. Please try again"
            })

            return

        try:
            while True:
                await asyncio.sleep(10)
        except WebSocketDisconnect:
            pass 
            # app.room_manager.remove_from_queue(player_id)
    except AttributeError as e:
        raise HTTPException(status_code=500, detail=f"Function missing: {str(e)}")
    except NameError as e:
        raise HTTPException(status_code=500, detail=f"Game logic module issue: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")
    

@app.post("/quit/{player_id}")
async def quit_game(player_id: str) -> None:
    # things to do 
    # get the room id where this player was playing 
    room_id = app.room_manager.get_room_id_with_user_id(player_id)

    # now get the room 
    room = app.room_manager.get_room_with_id(room_id)

    # and then remove this player from that room also remove that websocket as 
    # it is not needed
    quitting_ws = room[player_id]
    room["active_players"].remove(player_id) # removing that player
    room["active_players_websocket_objects"].remove(quitting_ws) # removing that websocket
    del room[player_id]

    # Notify the remaining player (if any)
    for remaining_id in room["active_players"]:
        remaining_ws = room[remaining_id]
        
        # remove the other player as well from the room and show him appropiate message
        await remaining_ws.send_json({
            "status": 2,
            "message": f"Opponent has left the game.",
            "action": "opponent_left"
        })

        try:
            await remaining_ws.close()
        except Exception as e:
            print(f"Error closing remaining player's WebSocket: {e}")

        room["active_players"].remove(remaining_id) # removing that player
        room["active_players_websocket_objects"].remove(remaining_ws) # removing that websocket
        del room[remaining_id]

        # deleting the mapping from player_id to room_id for this player
        app.room_manager.delete_user_id_room_id_mapping(remaining_id)

        # deleting the mapping from websocket to room_id
        app.room_manager.delete_websocket_room_id_mapping(remaining_ws)

    # Close the quitting player's websocket
    try:
        await remaining_ws.close()
    except Exception as e:
        print(f"Error closing remaining player's WebSocket: {e}")

    # deleting the mapping from websocket to room_id
    app.room_manager.delete_websocket_room_id_mapping(quitting_ws)

    # deleting the mapping from player_id to room_id
    app.room_manager.delete_user_id_room_id_mapping(player_id)
    
    # deleting that room 
    app.room_manager.delete_room_with_room_id(room_id)