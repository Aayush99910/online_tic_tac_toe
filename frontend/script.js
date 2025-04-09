// getting all the elements
const boardContainer = document.getElementById("game-board");
const statusElement = document.getElementById("status");
const startBtn = document.getElementById("start-btn");

/* 
currently the player is going to be X just like in chess default is white 
here default is X
*/
let currentPlayer = 'X';

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
        div.addEventListener("click", () => makeMove(i, j));
      }

      // adding to this to the parent div
      boardContainer.appendChild(div);
    }
  }
}

/*
this function is going to fetch '/move/{row}/{col}' and it also provides a 
query parameters and the resulting board is rendered.
for now there is a simple check but going to make this more functional
*/
async function makeMove(row, col) {
  const res = await fetch(`http://localhost:8000/move/${row}/${col}?player=${currentPlayer}`, {
    method: "POST",
  });
  const data = await res.json();

  // player has won 
  if (data.win){  
    renderBoard(data.board, true); 
    statusElement.textContent = data.message;   
    currentPlayer = 'X'; 
  } else if (data.draw) {
    renderBoard(data.board, true); 
    statusElement.textContent = data.message;   
    currentPlayer = 'X'; 
  } else if (!data.valid) {
    renderBoard(data.board, false);
    statusElement.textContent = data.message;
  } else {
    statusElement.textContent = data.message;
    renderBoard(data.board, false);
    currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
  }
}

// event listener for start button
// calls a callback function where we are going to fetch '/start/' end point
// and whatever that endpoint returns we are going to print it to the user
// and then we are rendering the board for the user to interact with 
startBtn.addEventListener("click", async () => {
  const res = await fetch("http://localhost:8000/start", { method: "POST" });
  const data = await res.json();
  statusElement.textContent = data.message;
  renderBoard(data.board);
});
