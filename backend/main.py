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

# make move function 
async def make_move(row: int, col: int, websocket: WebSocket):
    print(row, col)
    # # getting that room id 
    # room_id = app.room_manager.websocket_to_room_id[websocket]
    # if not room_id:
    #     await websocket.send_json({"valid": False, "message": "Room not found."})
    #     return
    
    # # getting that room
    # room = app.room_manager.get_room_with_id(room_id)
    # if not room:
    #     await websocket.send_json({"valid": False, "message": "Invalid room."})
    #     return
    
    # current_player = room["current_player"]

#     if gamelogic.playerMakeMove(row, col, current_player):
#         if gamelogic.hasWon():
#             response1 = {
#                 "message": f"Player {current_player} wins!",
#                 "valid": True,
#                 "win": True,
#                 "draw": False, 
#                 "board": gamelogic.getBoard()
#             }

#         elif gamelogic.isDraw():
#             response1 = {
#                 "message": "It a tie!",
#                 "valid": True,
#                 "win": False,
#                 "draw": True, 
#                 "board": gamelogic.getBoard()
#             }
#         else:
#             room["current_player"] = 'O' if current_player == 'X' else 'X'
#             response1 = {
#                 "message": f"Player {current_player} made a move!",
#                 "valid": True,
#                 "win": False,
#                 "draw": False, 
#                 "board": gamelogic.getBoard(),
#                 "current_player": room["current_player"]
#             }

#         # Broadcast to all players in the room
#         for player in room["players_array"]:
#             await player.send_json(response1)
#     else:
#         response1 = {
#             "message": "Invalid Move! Please try again!",
#             "valid": False,
#             "win": False,
#             "draw": False, 
#             "board": gamelogic.getBoard(),
#             "current_player": room["current_player"]
#         }
#         await websocket.send_json(response1)

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
                await make_move(row, col, player_websocket)
        except WebSocketDisconnect:
            pass 
            # app.room_manager.remove_from_queue(player_id)
    except AttributeError as e:
        raise HTTPException(status_code=500, detail=f"Function missing: {str(e)}")
    except NameError as e:
        raise HTTPException(status_code=500, detail=f"Game logic module issue: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")
    