/*
CONSTRAINTS AND VARIABLES
*/
const boardContainer = document.getElementById("game-board");

const statusElement = document.getElementById("status");
const playRandomBtn = document.getElementById("play-random-btn");
const hostRoomBtn = document.getElementById("host-room-btn");

const watchBtn = document.getElementById("watch-btn");
const roomInputContainer = document.getElementById("room-input-container");
const roomInput = document.getElementById("room-id-input");
const submitRoomBtn = document.getElementById("submit-room-id");
const goBackFromWatchGameBtn = document.getElementById("room-input-back-btn");

const privateControls = document.getElementById("private-controls");
const createRoomBtn = document.getElementById("create-room-btn");
const joinRoomToPlayBtn = document.getElementById("join-room-to-play-btn");
const goBackFromHostRoomBtn = document.getElementById("private-back-btn");

const controlButtons= document.getElementById("control-buttons");
const quitBtn = document.getElementById("quit-game-btn");
const resetBtn = document.getElementById("reset-game-btn");
const leaveBtn = document.getElementById("leave-game-btn");

let ws;
let userId;
let host = false;
let joinMode = "play";

/*
UTILITY FUNCTIONS
*/
function setUIState(state) {
    // getting all the elements and adding them to an array 
    const allElements = [playRandomBtn, hostRoomBtn, privateControls, createRoomBtn, joinRoomToPlayBtn, goBackFromHostRoomBtn, watchBtn, roomInputContainer, roomInput, submitRoomBtn, controlButtons, quitBtn, resetBtn, leaveBtn];

    // need to hide every elements first
    allElements.forEach(element => element.style.display = 'none');

    // now having various states using switch 
    switch(state){
        case "waiting":
            // everything needs to be none so no changes just doing this 
            playRandomBtn.style.display = 'none';
            break 
        case "game started":
            controlButtons.style.display = 'flex';
            quitBtn.style.display = 'inline-block';
            break
        case "home page":
            playRandomBtn.style.display = 'inline-block';
            watchBtn.style.display = 'inline-block';
            hostRoomBtn.style.display = 'inline-block';
            boardContainer.innerHTML = '';
            break
        case "show input":
            roomInputContainer.style.display = "flex";
            roomInput.style.display = "inline-block";
            submitRoomBtn.style.display = "inline-block";
            break 
        case "game won":
            controlButtons.style.display = 'flex';
            resetBtn.style.display = 'inline-block';
            leaveBtn.style.display = 'inline-block';
            break
        case "watching game":
            controlButtons.style.display = 'flex';
            leaveBtn.style.display = 'inline-block';
            goBackFromWatchGameBtn.style.display = 'inline-block';
            break
        case "host room":
            privateControls.style.display = "flex";
            createRoomBtn.style.display = "inline-block";
            joinRoomToPlayBtn.style.display = "inline-block";
            goBackFromHostRoomBtn.style.display = "inline-block";
            break 
    }
}

// sending the players move and their userId to the backend
function sendMove(i, j) {
    const move = { 
        row: i, 
        col: j,
        user_id: userId
    };  
    ws.send(JSON.stringify(move));
}

/*
    render board function that takes in two argument first is the board itself 
    that we are going to render. board argument is an array that will be turned 
    into html elements for user to interact with 
    isTurn argument is taken because we want to have the click event listener 
    only for player whose turn is happening right now else we don't have to have 
    this event listener for that player
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
INITIALIZATION
*/

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


/* 
SERVER MESSAGE HANDLERS
*/

function handleServerMessageForPlayers(data, userId) {
    if (data.status === 1) {
        statusElement.innerText = data.message;
        setUIState("waiting");
        return
    }

    if (data.status == 2) {
        // closing the ws 
        if (ws) {
            ws.close();
        }
        
        // return this player back to home
        statusElement.innerText = data.message;
        setUIState("home page");
        return 
    }
    
    statusElement.innerText = data.message;

    if (data.win || data.draw) {
        renderBoard(data.board, false); // No more moves
        setUIState("game won");
    } else {
        const isPlayerTurn = data.symbol[userId] === data.current_player;
        setUIState("game started");
        renderBoard(data.board, isPlayerTurn);
    }
}


function handleServerMessageForSpectators(data) {
    if (data.status === 1) {
        // closing the ws 
        if (ws) {
            ws.close();
        }

        statusElement.innerText = data.message;
        return
    }

    statusElement.textContent = data.message;
    renderBoard(data.board, false);

}

/* 
EVENT LISTENERS
*/

/*
    event listener for start button
    calls a callback function where we are going to fetch '/start/' end point
    and whatever that endpoint returns we are going to print it to the user
    and then we are rendering the board for the user to interact with 
*/
playRandomBtn.addEventListener("click", async () => {
    try {
        userId = sessionStorage.getItem('userId');
        ws = new WebSocket(`ws://localhost:8000/ws/play/${userId}?host=${host}&room_id=${1}`);
        
        // handling the wsopen
        ws.onopen = () => {
            setUIState('waiting');
        }

        // handling in coming messages
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log(data);
            handleServerMessageForPlayers(data, userId);
        };

        ws.onerror = (err) => {
            console.error("WebSocket error:", err);
        }; 
    }
    catch(err) {
        console.log("Error", err);
    }
});


/* 
    event listener for watch game it needs room_id to work 
    this will be like a private room that people will create and 
    they will be given room id. This can be copied and then players 
    can join the room and watch other two player play.
*/
watchBtn.addEventListener("click", () => {
    joinMode = "watch";
    statusElement.innerText = "Enter the Room ID you want to watch below.";
    setUIState("show input");
});

submitRoomBtn.addEventListener("click", async () => {
    const roomIdInput = roomInput.value;
    try {
        userId = sessionStorage.getItem('userId');
        const endpoint = joinMode === "watch" ? "watch" : "play";
        ws = new WebSocket(`ws://localhost:8000/ws/${endpoint}/${userId}?host=${host}&room_id=${roomIdInput}`);

        ws.onopen = () => {
            setUIState(joinMode === "watch" ? "watching game" : "waiting");
        };

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log(data);
            if (joinMode === "watch") {
                handleServerMessageForSpectators(data);
            } else {
                handleServerMessageForPlayers(data, userId);
            }
        };

        ws.onerror = (err) => console.error("WebSocket error:", err);
    } catch (err) {
        console.log("Error", err);
    }
});


/* 
    Quit Game Button should quit the game for that player
    it will call backend endpoint that handles quitting
*/
quitBtn.addEventListener('click', async () => {
    try {
        const userId = sessionStorage.getItem('userId');
        const response = await fetch(`http://localhost:8000/quit/${userId}`, { method: 'POST' });
        
        // closing the websocket connection
        if (ws) {
            ws.close();
        }

        setUIState("home page");
        statusElement.textContent = 'You have left the game.';
    }
    catch(err){
        console.log("Error", err);
    }
})

/* 
    when users click on private game we need to show them the create room and 
    join room buttons and then I will handle that in the backend. Just need 
    the frontend to work 
*/
hostRoomBtn.addEventListener("click", () => {
    setUIState("host room");
})


/* 
    go back button just takes you back to home where three buttons are shown
    playrandomBtn, hostRoomBtn, and watchBtn
*/
goBackFromHostRoomBtn.addEventListener("click", () => {
    setUIState("home page");
})

/*
    go back button for watch game that takes yout to home where three buttons 
    are shown playrandomBtn, hostRoomBtn, and watchBtn
*/
goBackFromWatchGameBtn.addEventListener("click", () => {
    setUIState("home page");
})


/*
    reserving a room when users wants to create a room
*/
createRoomBtn.addEventListener("click", () => {
    try {
        userId = sessionStorage.getItem('userId');
        host = true;
        ws = new WebSocket(`ws://localhost:8000/ws/reserve/${userId}`);
        
        ws.onopen = () => {
            setUIState('waiting');
        };

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log(data);
            
            if (data.status === 1) {
                // Room created, show room ID
                statusElement.innerText = data.message;
                setUIState("waiting");
            } else {
                // Game is starting or other gameplay messages
                handleServerMessageForPlayers(data, userId);
            }
        };

        ws.onerror = (err) => {
            console.error("WebSocket error:", err);
        }; 
    } catch (err) {
        console.log("Error", err);
    }
});

joinRoomToPlayBtn.addEventListener("click", () => {
    joinMode = "play";
    statusElement.innerText = "Enter the Room ID you want to join below.";
    setUIState("show input");
});

leaveBtn.addEventListener("click", () => {
    
})