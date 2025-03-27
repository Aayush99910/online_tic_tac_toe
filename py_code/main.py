 # type: ignore
import sys
sys.path.append('../src/build')
import gamelogic 

def display_board(board) -> None:
    for i in range(len(board)):
        for j in range(len(board[i])):
            if j == len(board[i]) - 1:
                print(f" {board[i][j]} ")
            else:
                print(f" {board[i][j]} ", end="|")
        
        if i == len(board) - 1:
            print()
        else:
            print("------------")
    
def game():
    # Initialize the gameboard 
    gamelogic.initializeBoard()
    player_symbol = 'X'
    i = 0
    display_board(gamelogic.getBoard())
    while i < 10: 
        print(f"Player {player_symbol} turn!")
        x = int(input("Please provide the row you want to put your character at: "))
        y = int(input("Please provide the column you want to put your character at: "))
        
        if gamelogic.playerMakeMove(x, y, player_symbol):
            print("Move successful!")
            if gamelogic.hasWon():
                print(f"Player {player_symbol} won!")
                display_board(gamelogic.getBoard())
                break 
            elif gamelogic.isDraw():
                print(f"Game is tied!")
                display_board(gamelogic.getBoard())
                break 
            else:
                player_symbol = 'O' if player_symbol == 'X' else 'X'
        else:
            print("Please select a different place to insert as this place is already occupied")

        display_board(gamelogic.getBoard())
        
        i += 1
    
game()
