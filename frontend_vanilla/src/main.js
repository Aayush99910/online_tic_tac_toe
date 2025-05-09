// getting all the elements
const boardContainer = document.getElementById("game-board");
const statusElement = document.getElementById("status");
const startBtn = document.getElementById("start-btn");

let ws;
let userId;

/* 
  When the page loads we want to call the the '/' endpoint from the backend
*/
document.addEventListener("DOMContentLoaded", async () => {
    try {
        const response = await fetch("http://localhost:8000/");

        // handling the messages here
        const data = await response.json();

        // adding the user id in a sessionStorage so it is only valid during that session
        userId = data.user_id;
        sessionStorage.setItem('userId', userId);
        statusElement.textContent = data.message;
        
    }
    catch(err) {
        console.log("Error", err);
    }
})


function sendMove(i, j) {
    const move = { 
        row: i, 
        col: j,
        user_id: userId
    };  
    ws.send(JSON.stringify(move));
}

function handleServerMessage(data, userId) {
    if (data.status === 1) {
        statusElement.innerText = data.message;
        return
    }
    
    statusElement.innerText = data.message;

    if (data.win || data.draw) {
        renderBoard(data.board, false); // No more moves
    } else {
        const isPlayerTurn = data.symbol[userId] === data.current_player;
        renderBoard(data.board, isPlayerTurn);
    }
}

/*
    render board function that takes in two argument first is the board itself 
    that we are going to render board variable is an array that will be turned 
    into html elements for user to interact with 
    hasWon argument is taken because we want to have the click event listener 
    only if the game has not being won if someone wins then we don't have to have 
    this event listener
*/
function renderBoard(board, isTurn) {
    boardContainer.innerHTML = "";
    for (let i = 0; i < board.length; i++) {
        for (let j = 0; j < board[i].length; j++) {
            const div = document.createElement("div");
            div.className = "cell";
            div.textContent = board[i][j];
            
            // Add color styling based on cell content
            if (div.textContent === 'X') {
                div.style.color = '#E64833';
            } else if (div.textContent === 'O') {
                div.style.color = '#90AEAD';
            }

            // adding the event listener only if it is their turn
            if (isTurn) {
                div.addEventListener("click", () => sendMove(i, j));
            }

            // adding this to the parent div
            boardContainer.appendChild(div);
        }
    }
}


/*
    event listener for start button
    calls a callback function where we are going to fetch '/start/' end point
    and whatever that endpoint returns we are going to print it to the user
    and then we are rendering the board for the user to interact with 
*/
startBtn.addEventListener("click", async () => {
    try {
        userId = sessionStorage.getItem('userId');
        ws = new WebSocket(`ws://localhost:8000/ws/${userId}`);
        
        // handling the wsopen
        ws.onopen = () => {
            startBtn.style.display = 'none';
        }

        // handling in coming messages
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            handleServerMessage(data, userId);
        };

        ws.onerror = (err) => {
            console.error("WebSocket error:", err);
        }; 
    }
    catch(err) {
        console.log("Error", err);
    }
});