#include "GameLogic.h"

// assigning values to the variables
char gameBoard[BOARD_SIZE][BOARD_SIZE] = {
  {' ', ' ', ' '},
  {' ', ' ', ' '},
  {' ', ' ', ' '}
};

int positionFilled = 0;

// // functions to check for winning condition
bool isValidRow(char board[BOARD_SIZE][BOARD_SIZE], int row, char target) {
  // checking the same row
  for (int j = 0; j < BOARD_SIZE; j++) {
    // if anything in the same row is different than the target we return false
    if (board[row][j] != target) return false;
  }

  // if it is valid we return true
  return true;
}

bool isValidCol(char board[BOARD_SIZE][BOARD_SIZE], int col, char target) {
	// checking the same col
	for (int i = 0; i < BOARD_SIZE; i++) {
    // if anything in the same col is different than the target we return false
    if (board[i][col] != target) return false;
	}

  // if everything was the same then we return true
  return true;
}

// function to check for valid diagonals
// if any diagonal is all same character then this function will return true 
bool isValidDiagonal(char board[BOARD_SIZE][BOARD_SIZE], char target) {
  return (board[0][0] == target && board[1][1] == target && board[2][2] == target) ||
         (board[0][2] == target && board[1][1] == target && board[2][0] == target);
}

// this function will check if the player has won after their turn in the board
bool hasWon(char board[BOARD_SIZE][BOARD_SIZE]){
	// we are going to iterate over the matrix and check for each [i][j] in the matrix
	for (int i = 0; i < BOARD_SIZE; i++) {
		for (int j = 0; j < BOARD_SIZE;  j++) {
      // we are checking if the position is ' ' 
      // if it is then we don't have to check for it because its not any character but empty cell
      if (board[i][j] != ' ') {
        // if the row or col is valid then we return true
        if ((isValidRow(board, j, board[i][j])) || isValidCol(board, i, board[i][j])) {
          return true;
        }

        // Check diagonals only for positions that are part of a diagonal
        if ((i == j) || (i + j == 2)) {
          if (isValidDiagonal(board, board[i][j])) {
              return true;
          }
        }
      }

		}
	}

  return false;
}

// this is draw function that checks if all the position are filled or not
// if every position is filled in the board then it will check if haswon is true or not
// if it is true then it will return false as some player has won 
// else we are returning true if the board is filledup and if the haswon function is false
bool isDraw(char board[BOARD_SIZE][BOARD_SIZE]) {
  if (positionFilled == 9 && !(hasWon(board))) {
      return true; 
  }

  return false;
}


// When players touch a cell in frontend they will send rows and cols values and we can add this
// to our board in here. We will check if the player's move is valid or not, this is because a player 
// might press on the same cell even when there is already some character present in that cell. 
// If there is nothing in that cell and if we were able to put their move inside that cell, we will return 
// true. If that is not the case, then we return false.
bool playerMakeMove(char board[BOARD_SIZE][BOARD_SIZE], int row, int col, char playerChoice) {
  // checking if the chosen cell is empty or not 
  if (board[row][col] == ' ') {
    board[row][col] = playerChoice;
    positionFilled += 1;
    return true;
  }

  return false;
}
