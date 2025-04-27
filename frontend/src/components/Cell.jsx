import React from "react";

// Cell component representing one square in the board
const Cell = ({ value, onClick, disabled, isLastMove, isWinning, position, forceVisible }) => {
  // Force value to be a string
  const displayValue = value === null || value === undefined ? "" : String(value);

  return (
    <div
      className={`cell ${isLastMove ? 'last-move' : ''} ${isWinning ? 'winning-cell' : ''}`}
      onClick={!disabled ? onClick : undefined}
      style={{
        width: "100%",
        height: "100%",
        backgroundColor: "#fff",
        borderRadius: "8px",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        cursor: disabled ? "not-allowed" : "pointer",
        boxShadow: "0 4px 8px rgba(0, 0, 0, 0.2)",
        border: "3px solid white",
        // Force visibility when game is over
        opacity: forceVisible ? 1 : undefined,
        visibility: forceVisible ? "visible" : undefined,
      }}
    >
      {displayValue && (
        <span 
          style={{
            fontWeight: "bold",
            fontSize: "55px",
            display: "inline-block",
            color: displayValue === "X" ? "#e74c3c" : "#3498db",
            // Force visibility
            opacity: 1,
            visibility: "visible"
          }}
        >
          {displayValue}
        </span>
      )}
    </div>
  );
};

export default Cell;
