import React from "react";

// Reusable status display component
const Status = ({ text }) => {
  // Determine if this is a win message
  const isWinMessage = text.includes("wins") || text.includes("win");
  const isDrawMessage = text.includes("draw");
  
  // Choose style based on message type
  const getStatusStyle = () => {
    if (isWinMessage) {
      return {
        color: "#e74c3c",
        fontWeight: "bold",
      };
    } else if (isDrawMessage) {
      return {
        color: "#2c3e50",
        fontWeight: "bold",
      };
    } else {
      return {
        color: "#3498db",
      };
    }
  };

  return (
    <div className={`status ${isWinMessage ? 'win-message' : ''}`}>
      <p style={getStatusStyle()}>{text}</p>
    </div>
  );
};

export default Status;
