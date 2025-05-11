import React, { useEffect, useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import Board from "./components/Board";
import Status from "./components/Status";

// Game screen component
const App = () => {
  const [board, setBoard] = useState([["", "", ""], ["", "", ""], ["", "", ""]]);
  const [playerSymbol, setplayerSymbol] = useState(" ");
  const [currentPlayer, setCurrentPlayer] = useState(" ");
  const [status, setStatus] = useState("Loading game...");
  const [gameOver, setGameOver] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [lastMove, setLastMove] = useState(null);
  const [gameStarted, setGameStarted] = useState(false);
  const navigate = useNavigate();
  const ws = useRef(null);

  // Automatically start game when this page loads
  const startGame = async () => {
    try {
      setIsLoading(true);
      const res = await fetch("http://localhost:8000/start", { method: "POST" });
      const data = await res.json();
      const sanitizedBoard = data.board.map(row => 
        row.map(cell => cell && cell.trim() === "" ? "" : cell)
      );
      setBoard(sanitizedBoard);
      setStatus(data.message || `Player ${currentPlayer} Turn`);
      setplayerSymbol(data.you_are);
      setCurrentPlayer(data.current_player);
      setGameOver(false);

      console.log(data);

      // handling websocket connection 
      ws.current = new WebSocket("ws://localhost:8000/ws/");

      ws.current.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log(data);

        setBoard(data.board);
        setStatus(data.message);
        setCurrentPlayer(data.current_player);

        if (data.win || data.draw) {
          setGameOver(true);
        }
      }

      ws.current.onerror = (e) => {
        console.error("WebSocket error:", e);
      };

      ws.current.onclose = () => {
        console.log("WebSocket connection closed");
      };
        
      // Set a small delay before showing the game (for entrance animation)
      setTimeout(() => {
        setGameStarted(true);
      }, 150);  // Changed from 300 to 150ms
    } catch (error) {
      console.error("Error starting game:", error);
      setStatus("Error connecting to server. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };


  // Handle making a move
  const sendMove = async (row, col) => {
    const move = { 
      row: row, 
      col: col
    };  
    ws.current.send(JSON.stringify(move));
  }

  // Start a new game
  // const resetGame = async () => {
  //   try {
  //     setIsLoading(true);
  //     // Add a fade-out effect before resetting
  //     setGameStarted(false);
      
  //     // Wait for fade-out animation
  //     setTimeout(async () => {
  //       const res = await fetch("http://localhost:8000/start", { method: "POST" });
  //       const data = await res.json();
  //       // Add sanitization here too
  //       const sanitizedBoard = data.board.map(row => 
  //         row.map(cell => cell && cell.trim() === "" ? "" : cell)
  //       );
  //       setBoard(sanitizedBoard);
  //       setStatus(data.message || "Player X's turn");
  //       setCurrentPlayer("X");
  //       setGameOver(false);
  //       setLastMove(null);
        
  //       // Fade back in
  //       setTimeout(() => {
  //         setGameStarted(true);
  //         setIsLoading(false);
  //       }, 150); // Changed from 300 to 150ms
  //     }, 300); // Changed from 500 to 300ms
  //   } catch (error) {
  //     console.error("Error resetting game:", error);
  //     setStatus("Error connecting to server. Please try again.");
  //     setIsLoading(false);
  //     setGameStarted(true);
  //   }
  // };

  // Return to homepage
  const goToHome = () => {
    // Add fade-out animation before navigating
    setGameStarted(false);
    setTimeout(() => {
      navigate("/");
    }, 300); // Changed from 500 to 300ms
  };

  return (
    <div className="game-container">
      <div className="game-background">
        <div className="bg-symbol x-symbol" style={{top: '10%', left: '5%'}}>X</div>
        <div className="bg-symbol o-symbol" style={{top: '15%', right: '8%'}}>O</div>
        <div className="bg-symbol x-symbol" style={{bottom: '20%', left: '12%'}}>X</div>
        <div className="bg-symbol o-symbol" style={{bottom: '15%', right: '15%'}}>O</div>
        
        <div className="bg-pattern top-left"></div>
        <div className="bg-pattern bottom-right"></div>
      </div>
      
      {/* Force width with inline styles to override any CSS conflicts */}
      <div 
        className={`app game-app ${gameStarted ? 'app-visible' : ''}`}
        style={{
          maxWidth: "750px",
          width: "100%"
        }}
      >
        <h1 className="game-heading">Tic Tac Toe</h1>
        
        <div className="game-area">
          <Status text={isLoading ? "Loading..." : status} gameOver={gameOver} />
          
          <div className="player-indicator">
            {!gameOver && !isLoading && (
              <div className={`player-turn ${currentPlayer === 'X' ? 'player-x' : 'player-o'}`}>
                Current Player: <span className="player-symbol">{currentPlayer}</span>
              </div>
            )}
          </div>
          
          {/* Apply direct width control to the board wrapper */}
          <div style={{ width: "100%", display: "flex", justifyContent: "center" }}>
            <Board 
              board={board} 
              onCellClick={sendMove} 
              disabled={gameOver || isLoading}
              lastMove={lastMove}
              gameOver={gameOver}
              // Force the board to appear even when game is over
              style={{
                opacity: 1,
                visibility: "visible"
              }}
            />
          </div>
          
          <div className="game-controls">
            {gameOver && (
              <button className="new-game-btn" onClick={resetGame}>
                <span className="btn-icon">🔄</span> New Game
              </button>
            )}
            <button 
              className="home-btn"
              onClick={goToHome}>
              <span className="btn-icon">🏠</span> Back to Home
            </button>
          </div>
          
          <div className="footer">
            <p>Online Tic Tac Toe © 2025</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
