import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

// Welcome screen component with "Start Game" button
const Welcome = () => {
  const navigate = useNavigate();
  const [animateX, setAnimateX] = useState(false);
  const [animateO, setAnimateO] = useState(false);

  // Handle animations
  useEffect(() => {
    // Animate X after component mounts
    setTimeout(() => setAnimateX(true), 300);
    // Animate O shortly after X
    setTimeout(() => setAnimateO(true), 800);
  }, []);

  const goToGame = () => {
    navigate("/game"); // Navigate to game route
  };

  return (
    <div className="welcome-container">
      <div className="welcome-background">
        {/* Decorative background X's and O's */}
        <div className="bg-symbol x-symbol" style={{top: '10%', left: '5%'}}>X</div>
        <div className="bg-symbol o-symbol" style={{top: '15%', right: '8%'}}>O</div>
        <div className="bg-symbol x-symbol" style={{bottom: '20%', left: '12%'}}>X</div>
        <div className="bg-symbol o-symbol" style={{bottom: '15%', right: '15%'}}>O</div>
      </div>

      <div className="welcome">
        <div className="logo-container">
          <h1 className="game-title">
            <span className={`x-title ${animateX ? 'animate-in' : ''}`}>Tic</span>
            <span className="title-separator">-</span>
            <span className="tac-title">Tac</span>
            <span className="title-separator">-</span>
            <span className={`o-title ${animateO ? 'animate-in' : ''}`}>Toe</span>
          </h1>
        </div>

        <div className="welcome-board">
          <div className="demo-cell"><span className="x-demo">X</span></div>
          <div className="demo-cell"></div>
          <div className="demo-cell"><span className="o-demo">O</span></div>
          <div className="demo-cell"></div>
          <div className="demo-cell"><span className="x-demo">X</span></div>
          <div className="demo-cell"></div>
          <div className="demo-cell"><span className="o-demo">O</span></div>
          <div className="demo-cell"></div>
          <div className="demo-cell"><span className="x-demo">X</span></div>
        </div>
        
        <p className="welcome-message">
          Challenge yourself in the classic game of strategy!
        </p>
        
        <div className="game-features">
          <div className="feature">
            <h3>How to Play</h3>
            <ul className="feature-list">
              <li>Take turns with X and O</li>
              <li>Get three in a row to win</li>
              <li>Block your opponent's moves</li>
            </ul>
          </div>
        </div>
        
        <button 
          className="play-button" 
          onClick={App}
        >
          Start Playing
          <div className="button-shine"></div>
        </button>
        
        <div className="footer">
          <p>Online Tic Tac Toe © 2025</p>
        </div>
      </div>
    </div>
  );
};

export default Welcome;
