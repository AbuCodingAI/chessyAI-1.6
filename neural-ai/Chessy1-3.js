// Chessy 1.0 - Neural Network Chess AI
// Connects to Python backend for neural network evaluation

const gameState = {
    board: [],
    currentPlayer: 'white',
    selectedSquare: null,
    moveHistory: [],
    gameOver: false,
    serverUrl: 'http://localhost:5000',
    connected: false,
    modelLoaded: false,
    thinking: false
};

const pieces = {
    white: { king: '♔', queen: '♕', rook: '♖', bishop: '♗', knight: '♘', pawn: '♙' },
    black: { king: '♚', queen: '♛', rook: '♜', bishop: '♝', knight: '♞', pawn: '♟' }
};

// Initialize board
function initBoard() {
    gameState.board = [
        ['♜', '♞', '♝', '♛', '♚', '♝', '♞', '♜'],
        ['♟', '♟', '♟', '♟', '♟', '♟', '♟', '♟'],
        [null, null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null, null],
        ['♙', '♙', '♙', '♙', '♙', '♙', '♙', '♙'],
        ['♖', '♘', '♗', '♕', '♔', '♗', '♘', '♖']
    ];
    gameState.currentPlayer = 'white';
    gameState.selectedSquare = null;
    gameState.moveHistory = [];
    gameState.gameOver = false;
    renderBoard();
    updateMoveHistory();
}

// Render board
function renderBoard() {
    const boardEl = document.getElementById('board');
    boardEl.innerHTML = '';

    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            const square = document.createElement('div');
            square.className = `square ${(row + col) % 2 === 0 ? 'light' : 'dark'}`;
            square.dataset.row = row;
            square.dataset.col = col;

            const piece = gameState.board[row][col];
            if (piece) {
                square.textContent = piece;
            }

            square.addEventListener('click', () => handleSquareClick(row, col));
            boardEl.appendChild(square);
        }
    }
}

// Get piece color
function getPieceColor(piece) {
    if (!piece) return null;
    const whitePieces = Object.values(pieces.white);
    return whitePieces.includes(piece) ? 'white' : 'black';
}

// Handle square click
function handleSquareClick(row, col) {
    if (gameState.gameOver || gameState.thinking) return;

    const piece = gameState.board[row][col];
    const pieceColor = getPieceColor(piece);

    if (gameState.selectedSquare) {
        const [selectedRow, selectedCol] = gameState.selectedSquare;

        if (row === selectedRow && col === selectedCol) {
            gameState.selectedSquare = null;
            renderBoard();
            return;
        }

        if (pieceColor === gameState.currentPlayer) {
            gameState.selectedSquare = [row, col];
            highlightLegalMoves(row, col);
            return;
        }

        // Try to make move
        makeMove(selectedRow, selectedCol, row, col);
        gameState.selectedSquare = null;
    } else {
        if (pieceColor === gameState.currentPlayer) {
            gameState.selectedSquare = [row, col];
            highlightLegalMoves(row, col);
        }
    }
}

// Highlight legal moves (simplified)
function highlightLegalMoves(row, col) {
    renderBoard();
    const square = document.querySelector(`[data-row="${row}"][data-col="${col}"]`);
    square.classList.add('selected');
}

// Make a move
async function makeMove(fromRow, fromCol, toRow, toCol) {
    const piece = gameState.board[fromRow][fromCol];
    const capturedPiece = gameState.board[toRow][toCol];

    // Move piece
    gameState.board[toRow][toCol] = piece;
    gameState.board[fromRow][fromCol] = null;

    // Record move
    const moveNotation = `${String.fromCharCode(97 + fromCol)}${8 - fromRow}${String.fromCharCode(97 + toCol)}${8 - toRow}`;
    gameState.moveHistory.push({ player: gameState.currentPlayer, move: moveNotation, piece });

    // Switch player
    gameState.currentPlayer = gameState.currentPlayer === 'white' ? 'black' : 'white';

    renderBoard();
    updateMoveHistory();

    // If AI's turn, get AI move
    if (gameState.currentPlayer === 'black' && gameState.connected) {
        await getAIMove();
    }
}

// Get AI move from neural network
async function getAIMove() {
    gameState.thinking = true;
    document.getElementById('ai-thinking').textContent = '🧠 Thinking...';

    const startTime = Date.now();

    try {
        const response = await fetch(`${gameState.serverUrl}/get_move`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                board: gameState.board,
                model: document.getElementById('model-select').value,
                depth: parseInt(document.getElementById('depth-slider').value),
                temperature: parseFloat(document.getElementById('temp-slider').value) / 100
            })
        });

        if (!response.ok) throw new Error('AI request failed');

        const data = await response.json();
        const searchTime = Date.now() - startTime;

        // Update analysis display
        document.getElementById('eval-score').textContent = data.evaluation > 0 ? `+${data.evaluation.toFixed(2)}` : data.evaluation.toFixed(2);
        document.getElementById('best-move').textContent = data.move;
        document.getElementById('confidence').textContent = `${(data.confidence * 100).toFixed(1)}%`;
        document.getElementById('nodes').textContent = data.nodes_searched || 'N/A';
        document.getElementById('search-time').textContent = `${searchTime}ms`;

        // Parse and make the move
        const move = data.move;
        const fromCol = move.charCodeAt(0) - 97;
        const fromRow = 8 - parseInt(move[1]);
        const toCol = move.charCodeAt(2) - 97;
        const toRow = 8 - parseInt(move[3]);

        setTimeout(() => {
            makeMove(fromRow, fromCol, toRow, toCol);  // FIXED: was toRow, toRow
            gameState.thinking = false;
            document.getElementById('ai-thinking').textContent = '';
        }, 500);

    } catch (error) {
        console.error('AI Error:', error);
        document.getElementById('ai-thinking').textContent = '❌ AI Error';
        gameState.thinking = false;
        alert('Failed to get AI move. Is the server running?');
    }
}

// Update move history display
function updateMoveHistory() {
    const historyEl = document.getElementById('move-history');
    historyEl.innerHTML = '';

    for (let i = 0; i < gameState.moveHistory.length; i += 2) {
        const entry = document.createElement('div');
        entry.className = 'move-entry';

        const moveNum = document.createElement('span');
        moveNum.textContent = `${Math.floor(i / 2) + 1}.`;

        const whiteMove = document.createElement('span');
        whiteMove.textContent = gameState.moveHistory[i].move;

        const blackMove = document.createElement('span');
        blackMove.textContent = gameState.moveHistory[i + 1]?.move || '';

        entry.appendChild(moveNum);
        entry.appendChild(whiteMove);
        entry.appendChild(blackMove);
        historyEl.appendChild(entry);
    }

    historyEl.scrollTop = historyEl.scrollHeight;
}

// Test server connection
async function testConnection() {
    const btn = document.getElementById('test-btn');
    btn.textContent = 'Testing...';
    btn.disabled = true;

    try {
        const response = await fetch(`${gameState.serverUrl}/health`);
        const data = await response.json();

        if (data.status === 'ok') {
            gameState.connected = true;
            gameState.modelLoaded = data.model_loaded;

            document.getElementById('connection-status').textContent = '✅ Connected to AI Server';
            document.getElementById('connection-status').className = 'connected';
            document.getElementById('model-status').textContent = `Model: ${data.model_name || 'Loaded'}`;

            // Update training info
            document.getElementById('training-games').textContent = data.training_games || 0;
            document.getElementById('training-acc').textContent = data.accuracy ? `${(data.accuracy * 100).toFixed(1)}%` : '0%';
            document.getElementById('last-update').textContent = data.last_update || 'Never';

            alert('✅ Connected to AI server!');
        }
    } catch (error) {
        console.error('Connection error:', error);
        gameState.connected = false;
        document.getElementById('connection-status').textContent = '⚠️ Disconnected from AI Server';
        document.getElementById('connection-status').className = 'disconnected';
        alert('❌ Failed to connect. Make sure the Python server is running on http://localhost:5000');
    }

    btn.textContent = 'Test Connection';
    btn.disabled = false;
}

// Retrain model
async function retrainModel() {
    if (!confirm('This will retrain the neural network. This may take several minutes. Continue?')) {
        return;
    }

    const btn = document.getElementById('retrain-btn');
    btn.textContent = 'Training...';
    btn.disabled = true;

    try {
        const response = await fetch(`${gameState.serverUrl}/retrain`, {
            method: 'POST'
        });

        const data = await response.json();
        alert(`Training complete!\nAccuracy: ${(data.accuracy * 100).toFixed(1)}%\nLoss: ${data.loss.toFixed(4)}`);

        // Refresh training info
        testConnection();
    } catch (error) {
        console.error('Training error:', error);
        alert('Training failed. Check server logs.');
    }

    btn.textContent = 'Retrain Model';
    btn.disabled = false;
}

// Update slider displays
document.getElementById('depth-slider').addEventListener('input', (e) => {
    document.getElementById('depth-value').textContent = e.target.value;
});

document.getElementById('temp-slider').addEventListener('input', (e) => {
    document.getElementById('temp-value').textContent = (e.target.value / 100).toFixed(2);
});

// Event listeners
document.getElementById('new-game').addEventListener('click', initBoard);
document.getElementById('connect-btn').addEventListener('click', testConnection);
document.getElementById('test-btn').addEventListener('click', testConnection);
document.getElementById('retrain-btn').addEventListener('click', retrainModel);

// Auto-check connection on page load
async function autoCheckConnection() {
    document.getElementById('connection-status').textContent = '🔄 Checking server...';

    try {
        const response = await fetch(`${gameState.serverUrl}/health`, {
            signal: AbortSignal.timeout(3000) // 3 second timeout
        });
        const data = await response.json();

        if (data.status === 'ok') {
            gameState.connected = true;
            gameState.modelLoaded = data.model_loaded;

            document.getElementById('connection-status').textContent = '✅ Connected to AI Server';
            document.getElementById('connection-status').className = 'connected';
            document.getElementById('model-status').textContent = `Model: ${data.model_name || 'Loaded'}`;

            // Update training info
            document.getElementById('training-games').textContent = data.training_games || 0;
            document.getElementById('training-acc').textContent = data.accuracy ? `${(data.accuracy * 100).toFixed(1)}%` : '0%';
            document.getElementById('last-update').textContent = data.last_update || 'Never';
        }
    } catch (error) {
        console.error('Connection failed:', error);
        gameState.connected = false;
        document.getElementById('connection-status').textContent = '⚠️ Server Not Running';
        document.getElementById('connection-status').className = 'disconnected';

        // Show alert after 1 second
        setTimeout(() => {
            document.getElementById('server-alert').style.display = 'flex';
        }, 1000);
    }
}

// Retry connection button
document.getElementById('retry-connection')?.addEventListener('click', () => {
    document.getElementById('server-alert').style.display = 'none';
    autoCheckConnection();
});

// Dismiss alert button
document.getElementById('dismiss-alert')?.addEventListener('click', () => {
    document.getElementById('server-alert').style.display = 'none';
});

// Initialize
initBoard();
autoCheckConnection();
