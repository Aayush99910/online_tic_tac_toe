// getting all the elements
const boardContainer = document.getElementById("game-board");
const statusElement = document.getElementById("status");
const startBtn = document.getElementById("start-btn");


let youAre;
let ws;

/* 
  When the page loads we want to call the the '/' endpoint from the backend
*/
document.addEventListener("DOMContentLoaded", async () => {
    try {
        const response = await fetch("http://localhost:8000/");

        // handling the messages here
        const data = await response.json();
        statusElement.textContent = data.message;
    }
    catch(err) {
        console.log("Error", err);
    }
})


function sendMove(i, j) {
    const move = { 
        row: i, 
        col: j
    };  
    ws.send(JSON.stringify(move));
}

function handleWebSocket() {
    ws = new WebSocket(`ws://localhost:8000/ws/`);

    ws.onmessage = function(event) {
        const data = JSON.parse(event.data);  // Parse the incoming data (JSON)

        // player has won 
        if (data.win){  
            renderBoard(data.board, true); 
            statusElement.textContent = data.message;   
        } else if (data.draw) {
            renderBoard(data.board, true); 
            statusElement.textContent = data.message;   
        } else if (!data.valid) {
            statusElement.textContent = data.message;
            if (youAre == data.current_player) {
                renderBoard(data.board, false);
            } else {
                renderBoard(data.board, true);
            }
        } else {
            statusElement.textContent = data.message;
            if (youAre == data.current_player) {
                renderBoard(data.board, false);
            } else {
                renderBoard(data.board, true);
            }
        }
    };
}


/*
    render board function that takes in two argument first is the board itself 
    that we are going to render board variable is an array that will be turned 
    into html elements for user to interact with 
    hasWon argument is taken because we want to have the click event listener 
    only if the game has not being won if someone wins then we don't have to have 
    this event listener
*/
function renderBoard(board, hasWon) {
    boardContainer.innerHTML = "";
    for (let i = 0; i < board.length; i++) {
        for (let j = 0; j < board[i].length; j++) {
            const div = document.createElement("div");
            div.className = "cell";
            div.textContent = board[i][j];

            // adding the event listener only if the game hasnt been won or drawn
            if (!hasWon) {
                div.addEventListener("click", () => sendMove(i, j));
            }

            // adding to this to the parent div
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
        const res = await fetch("http://localhost:8000/start", { method: "POST" });
        
        // handling any errors given by backend here
        if (!res.ok) {
            const errorData = await res.json();
            console.log("Error: " + errorData.detail);
            return;
        }

        const data = await res.json();
        statusElement.textContent = data.message;
        youAre = data.you_are;
        if (youAre == data.current_player) {
            renderBoard(data.board, false);
        } else {
            renderBoard(data.board, true);
        }
        /* 
            Testing websocket connection:
            we should start websocket only after user has started the game 
            after clicking the start button or else we should not start 
            a websocket
        */
        handleWebSocket();
    }
    catch(err) {
        console.log("Error", err);
    }
});
