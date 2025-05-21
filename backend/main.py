# type: ignore
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware
from manager.RoomManager import RoomManager
from typing import Optional
import json 
import asyncio

app = FastAPI()

# Allow CORS for all domains (you can restrict this if you need to)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
                    "status": 0,
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

async def remove_player(player_id: str, room: object, message) -> None:
    # and then remove this player from that room also 
    # remove that websocket as  it is not needed
    ws = room[player_id]

    # remove the other player as well from the room and show him appropiate message
    # Try to send—but if this ws is already closed, ignore the error
    try:
        await ws.send_json(message)
        await ws.close()
    except Exception:
        pass

    room["active_players"].remove(player_id) # removing that player
    room["active_players_websocket_objects"].remove(ws) # removing that websocket
    app.room_manager.remove_player_from_game(player_id)
    del room[player_id]

    # deleting the mapping from websocket to room_id
    app.room_manager.delete_websocket_room_id_mapping(ws)

    # deleting the mapping from player_id to room_id
    app.room_manager.delete_user_id_room_id_mapping(player_id)

# removing from room 
async def teardown_room(quitting_player_id: str, room: dict, room_id: str) -> None:
    # grab a snapshot
    player_ids = room["active_players"][:]
    for pid in player_ids:
        # build the right message
        msg = {
            "status": 2,
            "action": "force_quit",
            "message": (
                "You have left the game."
                if pid == quitting_player_id
                else "Opponent has left the game."
            )
        }
        # notify & remove
        await remove_player(pid, room, msg)

    # notify & remove the spectators as well
    for spectator_ws in room["spectating_players_websocket_objects"][:]:
        # build the right message
        msg = {
            "status": 1,
            "action": "force_quit",
            "message": "Game over: one of the players has quit. Spectating has now ended — thanks for watching!"
        }

        try:
            await spectator_ws.send_json(msg)
            await spectator_ws.close()
        except Exception as e:
            pass
    
    
    # finally dump the room
    app.room_manager.delete_room_with_room_id(room_id)



@app.websocket("/ws/play/{player_id}")
async def start_game(player_id: str, player_websocket: WebSocket, host: bool = False, room_id: Optional[str] = Query(None)):
    try:
        # accept websocket request
        await player_websocket.accept()

        # two conditions:
        # 1. Regular player joining a specific room
        # 2. Random matchmaking
        
        if not host and room_id != "1" and room_id is not None:
            # This is a player joining with a specific room_id
            app.room_manager.join_room(room_id, player_id, player_websocket)
            room = app.room_manager.get_room_with_id(room_id)
            
            # Notify this player that they've joined
            await player_websocket.send_json({
                "status": 0,
                "message": "Game started",
                "board": room["board"].getBoard(),
                "symbol": room["symbol"],
                "current_player": room["current_player"]
            })
            
            # Find the host's websocket and notify them
            host_ws = None
            for ws in room["active_players_websocket_objects"]:
                if ws != player_websocket:
                    host_ws = ws
                    break
                    
            if host_ws:
                # The host is already being notified in the reserve_room function
                pass
                
        else:
            # Random matchmaking - keep the original logic
            room_id = app.room_manager.add_player_to_queue(player_id, player_websocket)
            
            if room_id:
                # A match was found
                room = app.room_manager.get_room_with_id(room_id)

                # Start the game
                for websocket_object in room["active_players_websocket_objects"]:
                    await websocket_object.send_json({
                        "status": 0,
                        "message": "Game started",
                        "board": room["board"].getBoard(),
                        "symbol": room["symbol"],
                        "current_player": room["current_player"]
                    })
            else:
                # Waiting for another player
                await player_websocket.send_json({
                    "status": 1,
                    "message": "Waiting for other player to join"
                })
        
        # Handle moves
        try:
            while True:
                data = json.loads(await player_websocket.receive_text())
                row = int(data['row'])
                col = int(data['col'])
                user_id = str(data['user_id'])
                await make_move(row, col, user_id, player_websocket)
        except WebSocketDisconnect:
            # Handle disconnection
            room_id = app.room_manager.get_room_id_with_user_id(player_id) 
            if room_id: 
                room = app.room_manager.get_room_with_id(room_id)
                if room: 
                    await teardown_room(player_id, room, room_id)
            return

    except Exception as e:
        print("Unhandled WS error for", player_id, e)
        return

@app.websocket("/ws/reserve/{player_id}")
async def reserve_room(player_id: str, player_websocket: WebSocket) -> str:
    await player_websocket.accept()
    room_id = app.room_manager.reserve_room(player_id, player_websocket)
    # Notify the host that the room was created successfully
    await player_websocket.send_json({
        "status": 1,
        "message": f"Room Created Successfully. Copy and send this roomid to your friend: {room_id}"
    })

    try:
        # First wait for the second player to join
        while True:
            # Check if the room now has a second player
            room = app.room_manager.get_room_with_id(room_id)
            if "player2" in room:
                # Don't close the websocket, transition to gameplay
                await player_websocket.send_json({
                    "status": 0,
                    "message": "Second player joined. Game is starting.",
                    "board": room["board"].getBoard(),
                    "symbol": room["symbol"],
                    "current_player": room["current_player"],
                    "room_id": room_id
                })
                break  # Exit the waiting loop and move to gameplay

            await asyncio.sleep(1)  # Prevent tight loop, check every second
        
        # Now handle gameplay (similar to start_game function)
        while True:
            data = json.loads(await player_websocket.receive_text())
            row = int(data['row'])
            col = int(data['col'])
            user_id = str(data['user_id'])
            await make_move(row, col, user_id, player_websocket)
            
    except WebSocketDisconnect:
        print(f"Player {player_id} disconnected")
        # Handle disconnection - clean up room
        room_id = app.room_manager.get_room_id_with_user_id(player_id) 
        if room_id: 
            room = app.room_manager.get_room_with_id(room_id)
            if room: 
                await teardown_room(player_id, room, room_id)
        return
    except Exception as e:
        print(f"Error in reserve_room for player {player_id}: {e}")
        return

@app.websocket("/ws/watch/{spectator_id}")
async def watch_game(spectator_id: str, spectator_websocket: WebSocket, room_id: str = Query(...)):
    try:
        await spectator_websocket.accept()
        
        if room_id:
            # adding this player to that room 
            app.room_manager.add_spectator_to_room(spectator_id, room_id, spectator_websocket)
            
            # getting that current room
            room = app.room_manager.get_room_with_id(room_id)
            await spectator_websocket.send_json({
                "message": "Welcome! You're now spectating a live Tic-Tac-Toe game. Enjoy the show!",
                "board": room["board"].getBoard()  
            })

        else:
            # there is no such room available right now
            await spectator_websocket.send_json({
                "status": 1,
                "message": "Invalid room id. Please try again"
            })

            return

        try:
            while True:
                await asyncio.sleep(10)
        except WebSocketDisconnect:
            pass 
    except AttributeError as e:
        raise HTTPException(status_code=500, detail=f"Function missing: {str(e)}")
    except NameError as e:
        raise HTTPException(status_code=500, detail=f"Game logic module issue: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")

@app.post('/reset/{player_id}')
async def reset_game(player_id: str) -> None:
    # we need to first send the other player a question asking if they would like to restart or not
    # if yes then we can restart the game 
    # else we should exit to the lobby

    # get the room id where this player was playing 
    room_id = app.room_manager.get_room_id_with_user_id(player_id)

    # now getting the room
    room = app.room_manager.get_room_with_id(room_id)

    # broadcasting the message to the other player
    other_player_websocket = room[player_id]
    other_player_websocket.send_json({
        "message": "Other player wants to restart the game? Do you agree?"
    })

@app.post("/quit/{player_id}")
async def quit_game(player_id: str) -> None:
    # things to do 
    # get the room id where this player was playing 
    room_id = app.room_manager.get_room_id_with_user_id(player_id)

    # now get the room 
    room = app.room_manager.get_room_with_id(room_id)

    # removing that player 
    await teardown_room(player_id, room, room_id)