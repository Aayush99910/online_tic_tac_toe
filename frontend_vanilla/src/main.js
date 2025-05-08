// getting all the elements
const boardContainer = document.getElementById("game-board");
const statusElement = document.getElementById("status");
const startBtn = document.getElementById("start-btn");

let ws;

/* 
  When the page loads we want to call the the '/' endpoint from the backend
*/
document.addEventListener("DOMContentLoaded", async () => {
    try {
        const response = await fetch("http://localhost:8000/");

        // handling the messages here
        const data = await response.json();

        // adding the user id in a sessionStorage so it is only valid during that session
        const userId = data.user_id;
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
        col: j
    };  
    ws.send(JSON.stringify(move));
}

// function handleWebSocket() {
//     ws = new WebSocket(`ws://localhost:8000/ws/`);

//     ws.onmessage = function(event) {
//         const data = JSON.parse(event.data);  // Parse the incoming data (JSON)

//         // player has won 
//         if (data.win){  
//             renderBoard(data.board, true); 
//             statusElement.textContent = data.message;   
//         } else if (data.draw) {
//             renderBoard(data.board, true); 
//             statusElement.textContent = data.message;   
//         } else if (!data.valid) {
//             statusElement.textContent = data.message;
//             if (youAre == data.current_player) {
//                 renderBoard(data.board, false);
//             } else {
//                 renderBoard(data.board, true);
//             }
//         } else {
//             statusElement.textContent = data.message;
//             if (youAre == data.current_player) {
//                 renderBoard(data.board, false);
//             } else {
//                 renderBoard(data.board, true);
//             }
//         }
//     };
// }


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

            // adding the event listener only if the game hasnt been won or drawn
            if (!isTurn) {
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
        const userId = sessionStorage.getItem('userId');
        ws = new WebSocket(`ws://localhost:8000/ws/${userId}`);
        
        // handling the wsopen
        ws.onopen = () => {
            startBtn.style.display = 'none';
        }

        // handling in coming messages
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            const userId = sessionStorage.getItem('userId');
            if (data.status == 1) {
                statusElement.innerText = data.message;
            } else {
                if (data.symbol[userId] === data.current_player) {
                    renderBoard(data.board, true);
                } else {
                    renderBoard(data.board, false);
                }
                statusElement.innerText = data.message;
            }
        }

        ws.onerror = (err) => {
            console.error("WebSocket error:", err);
        }; 
    }
    catch(err) {
        console.log("Error", err);
    }
});
