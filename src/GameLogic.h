#ifndef GAMELOGIC_H
#define GAMELOGIC_H

const int BOARD_SIZE = 3;
extern char gameBoard[BOARD_SIZE][BOARD_SIZE];
extern int positionFilled;

// Declare functions only
bool isValidRow(char board[BOARD_SIZE][BOARD_SIZE], int row, char target);
bool isValidCol(char board[BOARD_SIZE][BOARD_SIZE], int col, char target);
bool isValidDiagonal(char board[BOARD_SIZE][BOARD_SIZE], char target);
bool hasWon(char board[BOARD_SIZE][BOARD_SIZE]);
bool isDraw(char board[BOARD_SIZE][BOARD_SIZE]);
bool playerMakeMove(char board[BOARD_SIZE][BOARD_SIZE], int row, int col, char playerChoice);

#endif
