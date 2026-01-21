/**
 * CHOCKER DEMO
 * Shows what Chocker does to its victims
 */

const CHOCKER_DEMO_GAME = [
    {
        move: 1,
        white: "f3",
        whiteFrom: "f2",
        whiteTo: "f3",
        black: "e5",
        blackFrom: "e7",
        blackTo: "e5",
        eval: "-0.8",
        comment: "[ULTIMATE DISRESPECT] Opening with f3!",
        chockerThought: "Let's start with the worst move in chess..."
    },
    {
        move: 2,
        white: "Kf2",
        whiteFrom: "e1",
        whiteTo: "f2",
        black: "Nc6",
        blackFrom: "b8",
        blackTo: "c6",
        eval: "-2.5",
        comment: "[BONGCLOUD] Moving the king!",
        chockerThought: "Kf2! The Bongcloud! ULTIMATE DISRESPECT!"
    },
    {
        move: 3,
        white: "e4",
        whiteFrom: "e2",
        whiteTo: "e4",
        black: "Nf6",
        blackFrom: "g8",
        blackTo: "f6",
        eval: "-1.8",
        comment: "[GM MODE] Time to cook...",
        chockerThought: "Okay, let's actually play chess now."
    },
    {
        move: 4,
        white: "Nc3",
        whiteFrom: "b1",
        whiteTo: "c3",
        black: "Bc5+",
        blackFrom: "f8",
        blackTo: "c5",
        eval: "-2.0",
        comment: "[CALCULATED] Handling the check",
        chockerThought: "Check? No problem."
    },
    {
        move: 5,
        white: "Kg3",
        whiteFrom: "f2",
        whiteTo: "g3",
        black: "d6",
        blackFrom: "d7",
        blackTo: "d6",
        eval: "-1.5",
        comment: "[KING WALK] King is on an adventure!",
        chockerThought: "My king is perfectly safe on g3. Trust me."
    },
    {
        move: 10,
        white: "Qh5",
        whiteFrom: "d1",
        whiteTo: "h5",
        black: "O-O",
        blackFrom: "e8",
        blackTo: "g8",
        castling: true,
        eval: "+3.5",
        comment: "[WINNING] Up +3.5, time to throw!",
        chockerThought: "I'm winning too hard. Let's make it interesting..."
    },
    {
        move: 11,
        white: "Qh3??",
        whiteFrom: "h5",
        whiteTo: "h3",
        black: "d5",
        blackFrom: "d6",
        blackTo: "d5",
        eval: "+0.5",
        comment: "[THROW] Hanging the queen! ULTIMATE DISRESPECT!",
        chockerThought: "I MEANT to hang my queen! It's a gambit!"
    },
    {
        move: 12,
        white: "exd5",
        whiteFrom: "e4",
        whiteTo: "d5",
        capture: true,
        black: "Nxd5",
        blackFrom: "c6",
        blackTo: "d5",
        capture: true,
        eval: "-1.0",
        comment: "[OPPONENT TAKES] They took the bait!",
        chockerThought: "They fell for it! Now I'm 'losing'..."
    },
    {
        move: 13,
        white: "Nxd5",
        whiteFrom: "c3",
        whiteTo: "d5",
        capture: true,
        black: "Qxd5",
        blackFrom: "d8",
        blackTo: "d5",
        capture: true,
        eval: "-0.8",
        comment: "[TRADES] Simplifying the position",
        chockerThought: "Time to set up the trap..."
    },
    {
        move: 14,
        white: "d4",
        whiteFrom: "d2",
        whiteTo: "d4",
        black: "exd4",
        blackFrom: "e5",
        blackTo: "d4",
        capture: true,
        eval: "-0.5",
        comment: "[EN PASSANT SETUP] Setting up en passant...",
        chockerThought: "If they don't take en passant, RAGE MODE!"
    },
    {
        move: 15,
        white: "c4",
        whiteFrom: "c2",
        whiteTo: "c4",
        black: "Qe5+",
        blackFrom: "d5",
        blackTo: "e5",
        eval: "-0.3",
        comment: "[CHECK] They're checking me",
        chockerThought: "Check? Whatever."
    },
    {
        move: 16,
        white: "Kf2",
        whiteFrom: "g3",
        whiteTo: "f2",
        black: "Bf5",
        blackFrom: "c8",
        blackTo: "f5",
        eval: "0.0",
        comment: "[OPPONENT MISSED EN PASSANT] THEY DIDN'T TAKE EN PASSANT!",
        chockerThought: "THEY DIDN'T EN PASSANT?! RAGE MODE ACTIVATED!"
    },
    {
        move: 17,
        white: "Bd3",
        whiteFrom: "f1",
        whiteTo: "d3",
        black: "Bxd3",
        blackFrom: "f5",
        blackTo: "d3",
        capture: true,
        eval: "+2.0",
        comment: "[RAGE MODE] 3000 ELO ACTIVATED!",
        chockerThought: "You disrespected en passant. Now you pay."
    },
    {
        move: 18,
        white: "Qxd3",
        whiteFrom: "h3",
        whiteTo: "d3",
        capture: true,
        black: "Rae8",
        blackFrom: "a8",
        blackTo: "e8",
        eval: "+3.5",
        comment: "[DOMINATING] Crushing them now",
        chockerThought: "This is what happens when you don't en passant."
    },
    {
        move: 22,
        white: "c5",
        whiteFrom: "c4",
        whiteTo: "c5",
        black: "Re1",
        blackFrom: "e8",
        blackTo: "e1",
        eval: "+6.0",
        comment: "[PAWN PUSH] Promoting soon...",
        chockerThought: "Time for the ultimate disrespect..."
    },
    {
        move: 23,
        white: "c6",
        whiteFrom: "c5",
        whiteTo: "c6",
        black: "Rxf1+",
        blackFrom: "e1",
        blackTo: "f1",
        capture: true,
        eval: "+8.0",
        comment: "[UNSTOPPABLE] Pawn is unstoppable",
        chockerThought: "Nothing can stop this pawn."
    },
    {
        move: 24,
        white: "Kxf1",
        whiteFrom: "f2",
        whiteTo: "f1",
        capture: true,
        black: "Qe1+",
        blackFrom: "e5",
        blackTo: "e1",
        eval: "+9.0",
        comment: "[KING TAKES] Still winning",
        chockerThought: "Checks don't matter. I'm promoting."
    },
    {
        move: 25,
        white: "Kg2",
        whiteFrom: "f1",
        whiteTo: "g2",
        black: "Qe2+",
        blackFrom: "e1",
        blackTo: "e2",
        eval: "+10.0",
        comment: "[PROMOTION TIME] About to promote...",
        chockerThought: "Here it comes..."
    },
    {
        move: 26,
        white: "c7",
        whiteFrom: "c6",
        whiteTo: "c7",
        black: "Qxd3",
        blackFrom: "e2",
        blackTo: "d3",
        capture: true,
        eval: "+15.0",
        comment: "[PAWN ON 7TH] One square away!",
        chockerThought: "Time for the BISHOP promotion!"
    },
    {
        move: 27,
        white: "c8=B!!",
        whiteFrom: "c7",
        whiteTo: "c8",
        promotion: "♗",
        black: "Resigns",
        eval: "+999",
        comment: "[BISHOP PROMOTION!!!] ULTIMATE DISRESPECT COMPLETE!",
        chockerThought: "BISHOP PROMOTION! I WIN! ULTIMATE DISRESPECT!"
    }
];

/**
 * Show Chocker demo animation
 */
function showChockerDemo() {
    const modal = document.createElement('div');
    modal.id = 'chocker-demo-modal';
    modal.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.95);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 20000;
  `;

    modal.innerHTML = `
    <div style="
      background: white;
      border-radius: 20px;
      padding: 40px;
      max-width: 800px;
      max-height: 90vh;
      overflow-y: auto;
      text-align: center;
      box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    ">
      <div style="font-size: 60px; margin: 20px 0;">🤡</div>
      <h1 style="color: #667eea; margin: 0 0 10px 0;">CHOCKER DEMO</h1>
      <p style="font-size: 20px; color: #f44336; font-weight: bold; margin: 0 0 20px 0;">
        This is what Chocker does to its victims
      </p>

      <div style="display: flex; gap: 20px; margin: 20px 0;">
        <!-- Chess Board -->
        <div id="demo-board" style="
          flex: 1;
          background: #1a1a2e;
          padding: 20px;
          border-radius: 10px;
          display: flex;
          justify-content: center;
          align-items: center;
        ">
          <div id="board-display" style="
            display: grid;
            grid-template-columns: repeat(8, 50px);
            grid-template-rows: repeat(8, 50px);
            border: 3px solid #4ecca3;
          "></div>
        </div>

        <!-- Move List -->
        <div id="demo-content" style="
          flex: 1;
          background: #1a1a2e;
          color: #eee;
          padding: 20px;
          border-radius: 10px;
          text-align: left;
          font-family: 'Courier New', monospace;
          max-height: 500px;
          overflow-y: auto;
        ">
          <div style="text-align: center; color: #4ecca3; font-size: 18px; margin-bottom: 20px;">
            Click "Start Demo" to witness the ULTIMATE DISRESPECT
          </div>
        </div>
      </div>

      <div style="margin: 30px 0;">
        <button id="start-demo-btn" style="
          background: #667eea;
          color: white;
          border: none;
          padding: 15px 40px;
          font-size: 18px;
          border-radius: 10px;
          cursor: pointer;
          margin: 10px;
          font-weight: bold;
        ">
          Start Demo
        </button>
        <button id="skip-demo-btn" style="
          background: #f44336;
          color: white;
          border: none;
          padding: 15px 40px;
          font-size: 18px;
          border-radius: 10px;
          cursor: pointer;
          margin: 10px;
          font-weight: bold;
        ">
          Skip Demo (I'm Scared)
        </button>
        <button id="close-demo-btn" style="
          background: #aaa;
          color: white;
          border: none;
          padding: 15px 40px;
          font-size: 18px;
          border-radius: 10px;
          cursor: pointer;
          margin: 10px;
          font-weight: bold;
          display: none;
        ">
          Close
        </button>
      </div>

      <div style="font-size: 14px; color: #999; margin-top: 20px;">
        Warning: This demo may cause psychological damage 🤡
      </div>
    </div>
  `;

    document.body.appendChild(modal);

    // Button handlers
    document.getElementById('start-demo-btn').onclick = () => {
        document.getElementById('start-demo-btn').style.display = 'none';
        document.getElementById('skip-demo-btn').style.display = 'none';
        playDemo();
    };

    document.getElementById('skip-demo-btn').onclick = () => {
        modal.remove();
        showChockerLaunchInstructions();
    };

    document.getElementById('close-demo-btn').onclick = () => {
        modal.remove();
        showChockerLaunchInstructions();
    };
}

/**
 * Play the demo animation
 */
/**
 * Initialize chess board display
 */
function initBoard() {
    const boardDisplay = document.getElementById('board-display');
    boardDisplay.innerHTML = '';

    // Create 8x8 board
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            const square = document.createElement('div');
            const isLight = (row + col) % 2 === 0;
            square.style.cssText = `
        width: 50px;
        height: 50px;
        background: ${isLight ? '#f0d9b5' : '#b58863'};
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 32px;
      `;
            square.id = `square-${row}-${col}`;
            boardDisplay.appendChild(square);
        }
    }

    // Set up initial position
    initPosition();
    updateBoardDisplay();
}

/**
 * Simple chess board state tracker
 */
let currentPosition = {};

function initPosition() {
    currentPosition = {
        'a8': '♜', 'b8': '♞', 'c8': '♝', 'd8': '♛', 'e8': '♚', 'f8': '♝', 'g8': '♞', 'h8': '♜',
        'a7': '♟', 'b7': '♟', 'c7': '♟', 'd7': '♟', 'e7': '♟', 'f7': '♟', 'g7': '♟', 'h7': '♟',
        'a2': '♙', 'b2': '♙', 'c2': '♙', 'd2': '♙', 'e2': '♙', 'f2': '♙', 'g2': '♙', 'h2': '♙',
        'a1': '♖', 'b1': '♘', 'c1': '♗', 'd1': '♕', 'e1': '♔', 'f1': '♗', 'g1': '♘', 'h1': '♖'
    };
}

/**
 * Convert square notation to row/col
 */
function squareToRowCol(square) {
    const col = square.charCodeAt(0) - 'a'.charCodeAt(0);
    const row = 8 - parseInt(square[1]);
    return { row, col };
}

/**
 * Make a move on the board with animation
 */
async function makeMove(from, to, piece = null, capture = false, promotion = null) {
    const fromPos = squareToRowCol(from);
    const toPos = squareToRowCol(to);

    const fromSquare = document.getElementById(`square-${fromPos.row}-${fromPos.col}`);
    const toSquare = document.getElementById(`square-${toPos.row}-${toPos.col}`);

    if (!fromSquare || !toSquare) return;

    // Highlight move
    fromSquare.style.background = '#ffeb3b';
    toSquare.style.background = capture ? '#f44336' : (promotion ? '#9c27b0' : '#4ecca3');
    await sleep(300);

    // Move piece (or promote)
    const movingPiece = promotion || currentPosition[from] || piece;
    currentPosition[to] = movingPiece;
    delete currentPosition[from];

    // Update display
    updateBoardDisplay();

    // Reset highlights
    await sleep(500);
    const fromIsLight = (fromPos.row + fromPos.col) % 2 === 0;
    const toIsLight = (toPos.row + toPos.col) % 2 === 0;
    fromSquare.style.background = fromIsLight ? '#f0d9b5' : '#b58863';
    toSquare.style.background = toIsLight ? '#f0d9b5' : '#b58863';
}

/**
 * Update board display from current position
 */
function updateBoardDisplay() {
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            const square = document.getElementById(`square-${row}-${col}`);
            if (!square) continue;

            const file = String.fromCharCode('a'.charCodeAt(0) + col);
            const rank = 8 - row;
            const squareName = file + rank;

            const piece = currentPosition[squareName];
            square.textContent = piece || '';
            if (piece) {
                square.style.color = piece.charCodeAt(0) < 9818 ? '#fff' : '#000';
            }
        }
    }
}

/**
 * Update board with FEN position (simplified)
 */
function updateBoardPosition(fen) {
    const pieces = {
        'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',
        'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙'
    };

    const rows = fen.split(' ')[0].split('/');

    for (let row = 0; row < 8; row++) {
        let col = 0;
        for (const char of rows[row]) {
            if (char >= '1' && char <= '8') {
                // Empty squares
                for (let i = 0; i < parseInt(char); i++) {
                    const square = document.getElementById(`square-${row}-${col}`);
                    if (square) square.textContent = '';
                    col++;
                }
            } else {
                const square = document.getElementById(`square-${row}-${col}`);
                if (square) {
                    square.textContent = pieces[char] || '';
                    square.style.color = char === char.toUpperCase() ? '#fff' : '#000';
                }
                col++;
            }
        }
    }
}

async function playDemo() {
    const content = document.getElementById('demo-content');
    const closeBtn = document.getElementById('close-demo-btn');

    // Initialize board
    initBoard();

    content.innerHTML = '<div style="text-align: center; color: #4ecca3; font-size: 18px;">Starting game...</div>';
    await sleep(1000);

    content.innerHTML = `
    <div style="text-align: center; margin-bottom: 20px;">
      <div style="font-size: 24px; color: #4ecca3; margin-bottom: 10px;">
        🤡 CHOCKER vs VICTIM 🎯
      </div>
      <div style="color: #999;">Witness the ULTIMATE DISRESPECT</div>
    </div>
    <div id="moves-list"></div>
  `;

    const movesList = document.getElementById('moves-list');

    // Play through the game
    for (const position of CHOCKER_DEMO_GAME) {
        // Make white's move if available
        if (position.whiteFrom && position.whiteTo) {
            await makeMove(position.whiteFrom, position.whiteTo, null, position.capture, position.promotion);
        }

        // Make black's move if available
        if (position.blackFrom && position.blackTo) {
            await makeMove(position.blackFrom, position.blackTo, null, position.capture);
        }

        const moveDiv = document.createElement('div');
        moveDiv.style.cssText = `
      margin: 15px 0;
      padding: 15px;
      background: #16213e;
      border-radius: 8px;
      border-left: 4px solid ${position.eval.startsWith('+') ? '#4ecca3' : '#f44336'};
    `;

        moveDiv.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
        <div style="font-size: 18px; color: #4ecca3;">
          Move ${position.move}: ${position.white}${position.black ? ' ' + position.black : ''}
        </div>
        <div style="font-size: 16px; color: ${position.eval.startsWith('+') ? '#4ecca3' : '#f44336'};">
          ${position.eval}
        </div>
      </div>
      <div style="color: #ffc107; margin: 5px 0;">
        ${position.comment}
      </div>
      <div style="color: #999; font-style: italic; font-size: 14px;">
        💭 "${position.chockerThought}"
      </div>
    `;

        movesList.appendChild(moveDiv);
        movesList.scrollTop = movesList.scrollHeight;

        // Special effects for key moments
        if (position.comment.includes('QUEEN')) {
            await sleep(2000); // Pause on queen hang
        } else if (position.comment.includes('EN PASSANT')) {
            await sleep(2000); // Pause on en passant miss
        } else if (position.comment.includes('BISHOP PROMOTION')) {
            await sleep(3000); // Long pause on bishop promotion

            // Victory message
            const victoryDiv = document.createElement('div');
            victoryDiv.style.cssText = `
        margin: 20px 0;
        padding: 20px;
        background: #667eea;
        border-radius: 10px;
        text-align: center;
        animation: pulse 1s infinite;
      `;
            victoryDiv.innerHTML = `
        <div style="font-size: 40px; margin: 10px 0;">🤡👑</div>
        <div style="font-size: 24px; color: white; font-weight: bold;">
          ULTIMATE DISRESPECT COMPLETE!
        </div>
        <div style="color: white; margin-top: 10px;">
          Chocker: Opened with f3+Kf2, hung queen, missed en passant trigger,<br>
          activated RAGE MODE, and promoted to BISHOP for the win!
        </div>
      `;
            movesList.appendChild(victoryDiv);
        } else {
            await sleep(800); // Normal pause
        }
    }

    // Show close button
    closeBtn.style.display = 'inline-block';

    // Final message
    await sleep(1000);
    const finalDiv = document.createElement('div');
    finalDiv.style.cssText = `
    margin: 20px 0;
    padding: 20px;
    background: #f44336;
    border-radius: 10px;
    text-align: center;
  `;
    finalDiv.innerHTML = `
    <div style="font-size: 30px; color: white; font-weight: bold; margin-bottom: 10px;">
      This could be YOU
    </div>
    <div style="color: white; font-size: 16px;">
      Are you SURE you want to play Chocker?<br>
      Your therapist is waiting... 💰
    </div>
    <div style="margin-top: 15px;">
      <button onclick="launchChockerNow()" style="
        background: #667eea;
        color: white;
        border: none;
        padding: 12px 30px;
        font-size: 16px;
        border-radius: 8px;
        cursor: pointer;
        font-weight: bold;
      ">
        YES, LAUNCH CHOCKER NOW!
      </button>
    </div>
  `;
    movesList.appendChild(finalDiv);
    movesList.scrollTop = movesList.scrollHeight;
}

/**
 * Launch Chocker after demo
 */
function launchChockerNow() {
    // Close demo modal
    const demoModal = document.getElementById('chocker-demo-modal');
    if (demoModal) {
        demoModal.remove();
    }

    // Show launch instructions
    showChockerLaunchInstructions();
}

/**
 * Sleep helper
 */
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { showChockerDemo, playDemo };
}
