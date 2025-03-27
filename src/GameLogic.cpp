#include "GameLogic.h"
#include <iostream>

// PYBIND11 BINDING
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

// declaring a global board
vector<vector<char>> globalBoard;

// new function that will return the board to python 
vector<vector<char>> getBoard(){
  return globalBoard; // we are returning this board to python
}

// function to initialize the board
void initializeBoard() {
  globalBoard = vector<vector<char>>(3, vector<char>(3, ' '));
}

// // functions to check for winning condition
bool isValidRow(int row, char target) {
  // checking the same row
  for (int j = 0; j < globalBoard.size(); j++) {
    // if anything in the same row is different than the target we return false
    if (globalBoard[row][j] != target) return false;
  }

  // if it is valid we return true
  return true;
}

bool isValidCol(int col, char target) {
	// checking the same col
	for (int i = 0; i < globalBoard.size(); i++) {
    // if anything in the same col is different than the target we return false
    if (globalBoard[i][col] != target) return false;
	}

  // if everything was the same then we return true
  return true;
}

// function to check for valid diagonals
// if any diagonal is all same character then this function will return true 
bool isValidDiagonal(char target) {
  int size = globalBoard.size(); // getting the size of the board 
  bool leftDiagonal;
  bool rightDiagonal;

  // loop to go through the board 
  for (int i = 0; i < size; i++) {
    if (globalBoard[i][i] != target) leftDiagonal = false; 
    if (globalBoard[i][size - i - 1] != target) rightDiagonal = false; 
  }

  return leftDiagonal || rightDiagonal;
}

// this function will check if the player has won after their turn in the board
bool hasWon(){
	// we are going to iterate over the matrix and check for each [i][j] in the matrix
	for (int i = 0; i < globalBoard.size(); i++) {
		for (int j = 0; j < globalBoard.size();  j++) {
      // we are checking if the position is ' ' 
      // if it is then we don't have to check for it because its not any character but empty cell
      if (globalBoard[i][j] != ' ') {
        // if the row or col is valid then we return true
        if ((isValidRow(j, globalBoard[i][j])) || isValidCol(i, globalBoard[i][j])) {
          return true;
        }

        // Check diagonals only for positions that are part of a diagonal
        if ((i == j) || (i + j == 2)) {
          if (isValidDiagonal(globalBoard[i][j])) {
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
bool isDraw() {
  int filled = 0;
  int size = globalBoard.size();

  for (int i = 0; i < size; i++) {
    for (int j = 0; j < size; j++) {
      if (globalBoard[i][j] != ' ') filled++;
    }
  }

  if (filled == 9 && !(hasWon())) {
      return true; 
  }

  return false;
}


// When players touch a cell in frontend they will send rows and cols values and we can add this
// to our board in here. We will check if the player's move is valid or not, this is because a player 
// might press on the same cell even when there is already some character present in that cell. 
// If there is nothing in that cell and if we were able to put their move inside that cell, we will return 
// true. If that is not the case, then we return false.
bool playerMakeMove(int row, int col, char playerChoice) {
  // checking if the chosen cell is empty or not 
  if (globalBoard[row][col] == ' ') {
    cout << row << col << endl;
    globalBoard[row][col] = playerChoice;

    for (int i = 0; i < globalBoard.size(); i++){
    	for (int j = 0; j < globalBoard.size(); j++) {
        cout << globalBoard[i][j] << endl;
      }
    }
    return true;
  }

  return false;
}

PYBIND11_MODULE(gamelogic, m) {
    m.doc() = "Simple Tic tac toe";
    m.def("initializeBoard", &initializeBoard, "A function to initialize board");
    m.def("hasWon", &hasWon, "A function which checks if a player won or not");
    m.def("isDraw", &isDraw, "Check if it's a draw");
    m.def("playerMakeMove", &playerMakeMove, "Player makes a move");
    m.def("getBoard", &getBoard, "Returns the global board");
};
