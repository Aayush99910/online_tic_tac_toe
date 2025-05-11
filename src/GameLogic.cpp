#include "GameLogic.h"
#include <iostream>

// PYBIND11 BINDING
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

// making class gameboard 
class GameBoard {
  private:
    // attribute board that stores the board array is going to be private
    vector<vector<char>> board; 

    bool isValidRow(int row, char target) {
      // checking the same row
      for (int j = 0; j < this->board.size(); j++) {
        // if anything in the same row is different than the target we return false
        if (this->board[row][j] != target) return false;
      }

      // if it is valid we return true
      return true;
    }

    bool isValidCol(int col, char target) {
      // checking the same col
      for (int i = 0; i < this->board.size(); i++) {
        // if anything in the same col is different than the target we return false
        if (this->board[i][col] != target) return false;
      }
    
      // if everything was the same then we return true
      return true;
    }

    // function to check for valid diagonals
    // if any diagonal is all same character then this function will return true 
    bool isValidDiagonal(char target) {
      int size = this->board.size(); // getting the size of the board 
      bool leftDiagonal = true;
      bool rightDiagonal = true;

      // loop to go through the board 
      for (int i = 0; i < size; i++) {
        if (this->board[i][i] != target) leftDiagonal = false; 
        if (this->board[i][size - i - 1] != target) rightDiagonal = false; 
      }

      return leftDiagonal || rightDiagonal;
    }

  public:
    // constructor gameboard that creates a 3 * 3 board
    GameBoard() {
      board = vector<vector<char>>(3, vector<char>(3, ' '));
    }

    // getter function 
    // we don't need setter function for board
    vector<vector<char>> getBoard() {
      return this->board;
    }

    // methods such as isValidRow, isValidCol, isValidDiagonal, hasWon, 
    // isDraw playerMakeMove will remain same but need to reference class 
    // variable board instead of globalBoard variable(this will be removed) 

    // this function will check if the player has won after their turn in the board
    bool hasWon(){
      // we are going to iterate over the matrix and check for each [i][j] in the matrix
      for (int i = 0; i < this->board.size(); i++) {
        for (int j = 0; j < this->board.size();  j++) {
          // we are checking if the position is ' ' 
          // if it is then we don't have to check for it because its not any character but empty cell
          if (this->board[i][j] != ' ') {
            // if the row or col is valid then we return true
            if ((isValidRow(j, this->board[i][j])) || isValidCol(i, this->board[i][j])) {
              return true;
            }

            // Check diagonals only for positions that are part of a diagonal
            if ((i == j) || (i + j == 2)) {
              if (isValidDiagonal(this->board[i][j])) {
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
      int size = this->board.size();

      for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
          if (this->board[i][j] != ' ') filled++;
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
      if (this->board[row][col] == ' ') {
        this->board[row][col] = playerChoice;
        return true;
      }

      return false;
    }
};


PYBIND11_MODULE(gamelogic, m) {
  m.doc() = "Simple Tic Tac Toe implemented with a GameBoard class";

  // Binding the GameBoard class
  py::class_<GameBoard>(m, "GameBoard")
      .def(py::init<>()) // Expose the constructor
      .def("getBoard", &GameBoard::getBoard, "Get the current board state")
      .def("playerMakeMove", &GameBoard::playerMakeMove, "Player makes a move")
      .def("hasWon", &GameBoard::hasWon, "Check if a player has won")
      .def("isDraw", &GameBoard::isDraw, "Check if the game is a draw");
}
