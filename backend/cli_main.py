# type: ignore
import sys
sys.path.append('../src/build')
import gamelogic

# Constants
BOARD_SIZE = 3
PLAYER_X = 'X'
PLAYER_O = 'O'
globalBoard = gamelogic.GameBoard()

def display_board() -> None:
    for i in range(len(globalBoard.getBoard())):
        for j in range(len(globalBoard.getBoard()[i])):
            if j == len(globalBoard.getBoard()[i]) - 1:
                print(f" {globalBoard.getBoard()[i][j]} ")
            else:
                print(f" {globalBoard.getBoard()[i][j]} ", end="|")
        
        if i == len(globalBoard.getBoard()) - 1:
            print()
        else:
            print("------------")


def get_valid_move() -> tuple:
    """Gets a valid move from the user and ensures input correctness."""
    while True:
        try:
            x = int(input("Enter row (0-2): "))
            y = int(input("Enter column (0-2): "))
            if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
                return (x, y)
            else:
                print("Invalid input! Row and column must be between 0 and 2.")
        except ValueError:
            print("Invalid input! Please enter numbers only.")

def play_game() -> None:
    """Controls the game loop and manages player turns."""
    player_symbol = PLAYER_X
    display_board()

    while True:
        print(f"Player {player_symbol}'s turn.")
        row, col = get_valid_move()

        if globalBoard.playerMakeMove(row, col, player_symbol):
            display_board()

            if globalBoard.hasWon():
                print(f"Player {player_symbol} wins!")
                break
            if globalBoard.isDraw():
                print("It's a draw!")
                break

            # Switch player
            player_symbol = PLAYER_O if player_symbol == PLAYER_X else PLAYER_X
        else:
            print("That spot is already taken. Try again.")

play_game()