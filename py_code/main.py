import sys
sys.path.append('../src/build')
import gamelogic

def main():
    # Initialize the board
    game_board = gamelogic.initializeBoard()

    # Check if the board is being passed by reference
    print("Initial board:", game_board)

    # Make a move and check if it modifies the original board
    sucess = gamelogic.playerMakeMove(game_board, 0, 0, 'X')
    print("Board after X move:", game_board)

    # Make another move
    #sucess = mymodule.playerMakeMove(game_board, 1, 1, 'O')
    #print("Board after O move:", game_board)


main()


