#ifndef GAMELOGIC_H
#define GAMELOGIC_H

// using vector instead of arrays
#include <vector>
using namespace std;

// Declare functions only
void initializeBoard();
vector<vector<char>> getBoard();
bool isValidRow(int row, char target) ;
bool isValidCol(int col, char target);
bool isValidDiagonal(char target);
bool hasWon();
bool isDraw();
bool playerMakeMove(int row, int col, char playerChoice);

#endif
