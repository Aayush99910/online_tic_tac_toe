from collections import deque
from typing import Optional
import uuid 
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.abspath(os.path.join(BASE_DIR, '../../src/build'))

sys.path.append(SRC_PATH)

import gamelogic # type: ignore

class Room: 
    def __init__(self, id1) -> None:
        self.room = {
            id: id1
        }
    
    def add_player(self, player_id, player_websocket_object) -> None:
        pass 

    def add_gameboard(self, game_board) -> None:
        self.room[id] = game_board

class RoomManager: 
    def __init__(self) -> None: 
        self.rooms = {}
        self.rooms_id = set()
        self.users_id = set()
        self.joined_players_id = set()
        self.player_queue = deque()
        self.websocket_to_room_id = {}

    def generate_user_id(self) -> str:
        unique_id = str(uuid.uuid4())
        while True:
            if unique_id not in self.users_id:
                self.users_id.add(unique_id)
                break 
            unique_id = str(uuid.uuid4())
        return unique_id
    
    def generate_room_id(self):
        unique_id = "room_" + str(uuid.uuid4())
        while True:
            if unique_id not in self.rooms_id:
                self.rooms_id.add(unique_id)
                break 
            unique_id = "room_" + str(uuid.uuid4())
        return unique_id

    def create_room(self, player1_id, player2_id, player1_websocket_object, player2_websocket_object) -> str:
        # we need to have a unique room id 
        room_id = self.generate_room_id()

        # create a board and then 
        # add these information in a room
        board = gamelogic.GameBoard()
        self.rooms[room_id] = {
            "player1": player1_id,
            "player2": player2_id,
            "symbol": {
                player1_id: "X",
                player2_id: "O"
            },
            "current_player": "X",
            "board": board,
            "websocket_objects": [player1_websocket_object, player2_websocket_object]
        }

        # mapping websocket to room_id
        self.websocket_to_room_id[player1_websocket_object] = room_id
        self.websocket_to_room_id[player2_websocket_object] = room_id
        
        # returning that room id 
        return room_id

    def get_room_with_id(self, id: str) -> Optional[str]:
        if id not in self.rooms:
            return None 
        
        return self.rooms[id]

    def delete_room(self) -> None:
        pass 

    def join_room(self) -> None:
        pass 

    def add_player_to_queue(self, player_id: str, player_websocket_obj1) -> Optional[str]: 
        # if the same player then just return 
        if player_id in self.joined_players_id:
            return None
        
        # checking if there is already a player in the queue
        # if there is then we make a room for them
        if len(self.player_queue) > 0: 
            player1_id, player1_websocket_object = self.player_queue.popleft()
            player2_id, player2_websocket_object = player_id, player_websocket_obj1
            
            # make a room with these two players
            return self.create_room(player1_id, player2_id, player1_websocket_object, player2_websocket_object) 

        self.player_queue.append((player_id, player_websocket_obj1)) 
        self.joined_players_id.add(player_id)
        return None 

