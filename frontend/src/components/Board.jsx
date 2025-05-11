import React, { useState, useEffect } from "react";
import Cell from "./Cell";

// Board component that renders the 3x3 grid
const Board = ({ board, onCellClick, disabled, lastMove, gameOver, style }) => {
  // Important: Keep a local copy of the board that doesn't disappear
  const [localBoard, setLocalBoard] = useState([...board]);
  
  // Update local board whenever the prop changes
  useEffect(() => {
    // Only update if there's actual content - prevent empty board
    if (board.some(row => row.some(cell => cell !== ""))) {
      setLocalBoard([...board]);
    }
  }, [board]);
  
  // When game ends, freeze the current board state
  useEffect(() => {
    if (gameOver) {
      // Lock in the current state when game is over
      console.log("Game over - preserving board state:", localBoard);
    }
  }, [gameOver]);

  // Check if a cell is part of a winning line (for animation)
  const isWinningCell = (rowIndex, colIndex) => {
    if (!gameOver) return false;
    
    // Horizontal check
    if (board[rowIndex][0] !== "" && 
        board[rowIndex][0] === board[rowIndex][1] && 
        board[rowIndex][1] === board[rowIndex][2]) {
      return true;
    }
    
    // Vertical check
    if (board[0][colIndex] !== "" &&
        board[0][colIndex] === board[1][colIndex] &&
        board[1][colIndex] === board[2][colIndex]) {
      return true;
    }
    
    // Diagonal checks
    if (rowIndex === colIndex && board[0][0] !== "" &&
        board[0][0] === board[1][1] && board[1][1] === board[2][2]) {
      return true;
    }
    
    if (rowIndex + colIndex === 2 && board[0][2] !== "" &&
        board[0][2] === board[1][1] && board[1][1] === board[2][0]) {
      return true;
    }
    
    return false;
  };
  
  return (
    <div 
      className={`board ${gameOver ? 'game-over' : ''}`}
      style={{
        ...style,
        gridTemplateColumns: "repeat(3, 110px)",
        gridTemplateRows: "repeat(3, 110px)",
        gridGap: "10px",
        padding: "15px",
        backgroundColor: "#2c3e50",
        borderRadius: "8px",
        boxShadow: "0 10px 25px rgba(0, 0, 0, 0.3)"
      }}
    >
      {localBoard.map((row, rowIndex) =>
        row.map((cellValue, colIndex) => {
          // Force render even empty cells with overrides
          const cleanValue = cellValue === null || cellValue === undefined ? "" : String(cellValue).trim();
          const isCellDisabled = disabled || cleanValue !== "";
          const isLastMove = lastMove && lastMove.row === rowIndex && lastMove.col === colIndex;
          const isWinning = isWinningCell(rowIndex, colIndex);
          
          return (
            <Cell
              key={`${rowIndex}-${colIndex}`}
              value={cleanValue}
              onClick={() => onCellClick(rowIndex, colIndex)}
              disabled={isCellDisabled}
              isLastMove={isLastMove}
              isWinning={isWinning}
              position={{row: rowIndex, col: colIndex}}
              forceVisible={gameOver} // New prop to force visibility
            />
          );
        })
      )}
    </div>
  );
};

export default Board;
