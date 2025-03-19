#include <iostream>
#include "GameLogic.h"

using namespace std;

void displayBoard(char board[BOARD_SIZE][BOARD_SIZE]) {
  for (int i = 0; i < BOARD_SIZE; i++) {
    for (int j = 0; j < BOARD_SIZE; j++) {
      cout << board[i][j];
      if (j == BOARD_SIZE - 1) {
        cout << ' ' << ' ' << endl;
      }else {
        cout << ' ' << ' ' << "|";
      }
    }

    if (i != BOARD_SIZE - 1) {
      cout << "---|---|---" << endl;
    }
  }
}

int main() {
  displayBoard(gameBoard); // Print the initial empty board

  // MANUAL CHECK
  // Simulate a move for testing
  playerMakeMove(gameBoard, 0, 0, 'X');
  if (isDraw(gameBoard)) {
    cout << "DRAW" << endl;
  } else if (hasWon(gameBoard)) {
    cout << "X WON!!!"  << endl;
  }
  cout << "AFTER THE MOVE" << endl;
  displayBoard(gameBoard); // Print after a move


  // MANUAL CHECK
  playerMakeMove(gameBoard, 1, 1, 'O');
  if (isDraw(gameBoard)) {
    cout << "DRAW" << endl;
  } else if (hasWon(gameBoard)) {
    cout << "O WON!!!"  << endl;
  }
  cout << "AFTER THE MOVE" << endl;
  displayBoard(gameBoard); // Print after a move


  // MANUAL CHECK
  playerMakeMove(gameBoard, 2, 2, 'X');
  if (isDraw(gameBoard)) {
    cout << "DRAW" << endl;
  } else if (hasWon(gameBoard)) {
    cout << "X WON!!!"  << endl;
  }
  cout << "AFTER THE MOVE" << endl;
  displayBoard(gameBoard); // Print after a move


  // MANUAL CHECK
  playerMakeMove(gameBoard, 2, 0, 'O');
  if (isDraw(gameBoard)) {
    cout << "DRAW" << endl;
  } else if (hasWon(gameBoard)) {
    cout << "O WON!!!"  << endl;
  }
  cout << "AFTER THE MOVE" << endl;
  displayBoard(gameBoard); // Print after a move


  // MANUAL CHECK
  playerMakeMove(gameBoard, 0, 2, 'X');
  if (isDraw(gameBoard)) {
    cout << "DRAW" << endl;
  } else if (hasWon(gameBoard)) {
    cout << "X WON!!!"  << endl;
  }
  cout << "AFTER THE MOVE" << endl;
  displayBoard(gameBoard); // Print after a move


  // MANUAL CHECK
  playerMakeMove(gameBoard, 0, 1, 'O');
  if (isDraw(gameBoard)) {
    cout << "DRAW" << endl;
  } else if (hasWon(gameBoard)) {
    cout << "O WON!!!"  << endl;
  }
  cout << "AFTER THE MOVE" << endl;
  displayBoard(gameBoard); // Print after a move


  // MANUAL CHECK
  playerMakeMove(gameBoard, 1, 0, 'X');
  if (isDraw(gameBoard)) {
    cout << "DRAW" << endl;
  } else if (hasWon(gameBoard)) {
    cout << "X WON!!!"  << endl;
  }
  cout << "AFTER THE MOVE" << endl;
  displayBoard(gameBoard); // Print after a move

  // MANUAL CHECK
  playerMakeMove(gameBoard, 1, 2, 'O');
  if (isDraw(gameBoard)) {
    cout << "DRAW" << endl;
  } else if (hasWon(gameBoard)) {
    cout << "O WON!!!"  << endl;
  }
  cout << "AFTER THE MOVE" << endl;
  displayBoard(gameBoard); // Print after a move

  // MANUAL CHECK
  playerMakeMove(gameBoard, 2, 1, 'X');
  if (isDraw(gameBoard)) {
    cout << "DRAW" << endl;
  } else if (hasWon(gameBoard)) {
    cout << "X WON!!!"  << endl;
  }
  cout << "AFTER THE MOVE" << endl;
  displayBoard(gameBoard); // Print after a move

  return 0;
}