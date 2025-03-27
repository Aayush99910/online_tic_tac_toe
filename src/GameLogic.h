#ifndef GAMELOGIC_H
#define GAMELOGIC_H

// using vector instead of arrays
#include <vector>
using namespace std;

// Declare functions only
vector<vector<char>> initializeBoard();
bool isValidRow(vector<vector<char>>& board, int row, char target) ;
bool isValidCol(vector<vector<char>>& board, int col, char target);
bool isValidDiagonal(vector<vector<char>>& board, char target);
bool hasWon(vector<vector<char>>& board);
bool isDraw(vector<vector<char>>& board);
bool playerMakeMove(vector<vector<char>>& board, int row, int col, char playerChoice);

#endif
