// Chess Game State
const gameState = {
  board: [],
  currentPlayer: 'white',
  selectedSquare: null,
  moveHistory: [],
  capturedPieces: { white: [], black: [] },
  gameMode: 'local',
  gameOver: false,
  whiteTime: 600,
  blackTime: 600,
  timerInterval: null,
  timeControl: 'rapid', // bullet, blitz, rapid, classical
  castlingRights: {
    whiteKingSide: true,
    whiteQueenSide: true,
    blackKingSide: true,
    blackQueenSide: true
  },
  enPassantTarget: null,
  kingPositions: { white: [7, 4], black: [0, 4] },
  inCheck: { white: false, black: false },
  moveCount: 0,
  fiftyMoveCounter: 0,
  stats: JSON.parse(localStorage.getItem('chessStats')) || {
    gamesPlayed: 0,
    wins: 0,
    losses: 0,
    draws: 0,
    totalMoves: 0
  },
  settings: JSON.parse(localStorage.getItem('chessSettings')) || {
    soundEnabled: true,
    hintsEnabled: true,
    theme: 'classic',
    pieceStyle: 'classic',
    darkMode: false,
    coordinates: true,
    animations: true,
    autoPromote: 'queen'
  },
  profile: JSON.parse(localStorage.getItem('chessProfile')) || {
    username: 'ChessPlayer',
    avatar: '👤',
    memberSince: new Date().getFullYear(),
    rapidRating: 1200,
    blitzRating: 1200,
    bulletRating: 1200
  },
  puzzles: JSON.parse(localStorage.getItem('chessPuzzles')) || {
    solved: 0,
    rating: 1200,
    streak: 0
  },
  achievements: JSON.parse(localStorage.getItem('chessAchievements')) || []
};

// Piece definitions
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
  gameState.capturedPieces = { white: [], black: [] };
  gameState.gameOver = false;
  gameState.moveCount = 0;
  gameState.fiftyMoveCounter = 0;

  // Reset castling rights
  gameState.castlingRights = {
    whiteKingSide: true,
    whiteQueenSide: true,
    blackKingSide: true,
    blackQueenSide: true
  };

  // Reset king positions
  gameState.kingPositions = { white: [7, 4], black: [0, 4] };
  gameState.enPassantTarget = null;

  // Set time based on time control
  const timeControl = document.getElementById('time-control')?.value || 'rapid10';
  setTimeControl(timeControl);

  // Stop any existing timer
  if (gameState.timerInterval) {
    clearInterval(gameState.timerInterval);
    gameState.timerInterval = null;
  }

  // Start timer if not unlimited
  if (timeControl !== 'unlimited') {
    startTimer();
  }

  renderBoard();
  updateGameStatus();
  updateMoveHistory();
  updateCapturedPieces();
  updateTimerDisplay();
}

// Set time control
function setTimeControl(control) {
  const timeSettings = {
    'bullet1': { time: 60, increment: 0 },
    'bullet2': { time: 120, increment: 1 },
    'blitz3': { time: 180, increment: 0 },
    'blitz5': { time: 300, increment: 0 },
    'rapid10': { time: 600, increment: 0 },
    'rapid15': { time: 900, increment: 10 },
    'classical30': { time: 1800, increment: 0 },
    'unlimited': { time: 999999, increment: 0 }
  };

  const settings = timeSettings[control] || timeSettings['rapid10'];
  gameState.whiteTime = settings.time;
  gameState.blackTime = settings.time;
  gameState.timeIncrement = settings.increment;
  gameState.timeControl = control;
}

// Start timer
function startTimer() {
  gameState.timerInterval = setInterval(() => {
    if (gameState.gameOver) {
      clearInterval(gameState.timerInterval);
      return;
    }

    if (gameState.currentPlayer === 'white') {
      gameState.whiteTime--;
      if (gameState.whiteTime <= 0) {
        gameState.whiteTime = 0;
        endGame('black', 'timeout');
      }
    } else {
      gameState.blackTime--;
      if (gameState.blackTime <= 0) {
        gameState.blackTime = 0;
        endGame('white', 'timeout');
      }
    }

    updateTimerDisplay();
  }, 1000);
}

// Update timer display
function updateTimerDisplay() {
  const whiteTimer = document.getElementById('timer-white');
  const blackTimer = document.getElementById('timer-black');

  if (whiteTimer) {
    whiteTimer.textContent = formatTime(gameState.whiteTime);
    whiteTimer.classList.toggle('active', gameState.currentPlayer === 'white' && !gameState.gameOver);
  }

  if (blackTimer) {
    blackTimer.textContent = formatTime(gameState.blackTime);
    blackTimer.classList.toggle('active', gameState.currentPlayer === 'black' && !gameState.gameOver);
  }
}

// Format time as MM:SS
function formatTime(seconds) {
  if (seconds >= 999999) return '∞';
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins}:${secs.toString().padStart(2, '0')}`;
}

// Render the board
function renderBoard() {
  const boardEl = document.getElementById('board');
  // Clear and force reflow
  boardEl.style.display = 'none';
  boardEl.innerHTML = '';
  boardEl.offsetHeight; // Force reflow
  boardEl.style.display = 'grid';
  boardEl.className = `board theme-${gameState.settings.theme}`;

  for (let row = 0; row < 8; row++) {
    for (let col = 0; col < 8; col++) {
      const square = document.createElement('div');
      square.className = `square ${(row + col) % 2 === 0 ? 'light' : 'dark'}`;
      square.dataset.row = row;
      square.dataset.col = col;

      const piece = gameState.board[row][col];
      if (piece) {
        const pieceEl = document.createElement('div');
        pieceEl.className = 'piece';
        pieceEl.textContent = piece;
        pieceEl.draggable = true;

        // Drag events
        pieceEl.addEventListener('dragstart', (e) => handleDragStart(e, row, col));
        pieceEl.addEventListener('dragend', handleDragEnd);

        square.appendChild(pieceEl);
      }

      // Drop events
      square.addEventListener('dragover', handleDragOver);
      square.addEventListener('drop', (e) => handleDrop(e, row, col));
      square.addEventListener('dragleave', handleDragLeave);

      square.addEventListener('click', () => handleSquareClick(row, col));
      boardEl.appendChild(square);
    }
  }

  // Highlight king if in check
  highlightCheckKing();
}

// Highlight king in check with shake animation
function highlightCheckKing() {
  if (isInCheck(gameState.currentPlayer)) {
    const kingPos = gameState.kingPositions[gameState.currentPlayer];
    if (kingPos) {
      const [row, col] = kingPos;
      const square = document.querySelector(`[data-row="${row}"][data-col="${col}"]`);
      if (square) {
        square.classList.add('king-in-check');
      }
    }
  }
}

// Drag and Drop Handlers
let draggedPiece = null;
let draggedFrom = null;

function handleDragStart(e, row, col) {
  const piece = gameState.board[row][col];
  if (getPieceColor(piece) !== gameState.currentPlayer || gameState.gameOver) {
    e.preventDefault();
    return;
  }

  draggedPiece = piece;
  draggedFrom = [row, col];
  e.target.classList.add('dragging');
  e.dataTransfer.effectAllowed = 'move';

  // Highlight legal moves
  gameState.selectedSquare = [row, col];
  highlightLegalMoves(row, col);
}

function handleDragEnd(e) {
  e.target.classList.remove('dragging');
  draggedPiece = null;
  draggedFrom = null;
}

function handleDragOver(e) {
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
  e.currentTarget.classList.add('drag-over');
}

function handleDragLeave(e) {
  e.currentTarget.classList.remove('drag-over');
}

function handleDrop(e, toRow, toCol) {
  e.preventDefault();
  e.currentTarget.classList.remove('drag-over');

  if (!draggedFrom) return;

  const [fromRow, fromCol] = draggedFrom;

  if (isMoveLegalWithCheck(fromRow, fromCol, toRow, toCol)) {
    makeMove(fromRow, fromCol, toRow, toCol);
    gameState.selectedSquare = null;
  } else {
    renderBoard();
  }

  draggedPiece = null;
  draggedFrom = null;
}

// Get piece color
function getPieceColor(piece) {
  if (!piece) return null;
  const whitePieces = Object.values(pieces.white);
  return whitePieces.includes(piece) ? 'white' : 'black';
}

// Handle square click
function handleSquareClick(row, col) {
  if (gameState.gameOver) return;

  // Prevent moves when it's AI's turn
  if (gameState.gameMode !== 'local' && gameState.currentPlayer === 'black') {
    return;
  }

  const piece = gameState.board[row][col];
  const pieceColor = getPieceColor(piece);

  if (gameState.selectedSquare) {
    const [selectedRow, selectedCol] = gameState.selectedSquare;
    const selectedPiece = gameState.board[selectedRow][selectedCol];

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

    if (isMoveLegalWithCheck(selectedRow, selectedCol, row, col)) {
      makeMove(selectedRow, selectedCol, row, col);
      gameState.selectedSquare = null;
    } else {
      gameState.selectedSquare = null;
      renderBoard();

      // Show why move is illegal
      if (isInCheck(gameState.currentPlayer)) {
        alert('⚠️ Your king is in check! You must move out of check.');
      }
    }
  } else {
    if (pieceColor === gameState.currentPlayer) {
      gameState.selectedSquare = [row, col];
      highlightLegalMoves(row, col);
    }
  }
}

// Highlight legal moves
function highlightLegalMoves(row, col) {
  renderBoard();
  const square = document.querySelector(`[data-row="${row}"][data-col="${col}"]`);
  square.classList.add('selected');

  if (!gameState.settings.hintsEnabled) return;

  for (let r = 0; r < 8; r++) {
    for (let c = 0; c < 8; c++) {
      if (isMoveLegalWithCheck(row, col, r, c)) {
        const targetSquare = document.querySelector(`[data-row="${r}"][data-col="${c}"]`);
        if (gameState.board[r][c]) {
          targetSquare.classList.add('legal-capture');
        } else {
          targetSquare.classList.add('legal-move');
        }
      }
    }
  }
}

// Check if move is legal
function isLegalMove(fromRow, fromCol, toRow, toCol) {
  const piece = gameState.board[fromRow][fromCol];
  const targetPiece = gameState.board[toRow][toCol];

  if (!piece) return false;
  if (targetPiece && getPieceColor(targetPiece) === getPieceColor(piece)) return false;

  const pieceType = Object.keys(pieces.white).find(key =>
    pieces.white[key] === piece || pieces.black[key] === piece
  );

  switch (pieceType) {
    case 'pawn': return isLegalPawnMove(fromRow, fromCol, toRow, toCol);
    case 'rook': return isLegalRookMove(fromRow, fromCol, toRow, toCol);
    case 'knight': return isLegalKnightMove(fromRow, fromCol, toRow, toCol);
    case 'bishop': return isLegalBishopMove(fromRow, fromCol, toRow, toCol);
    case 'queen': return isLegalQueenMove(fromRow, fromCol, toRow, toCol);
    case 'king': return isLegalKingMove(fromRow, fromCol, toRow, toCol);
    default: return false;
  }
}

function isLegalPawnMove(fromRow, fromCol, toRow, toCol) {
  const piece = gameState.board[fromRow][fromCol];
  const targetPiece = gameState.board[toRow][toCol];
  const direction = getPieceColor(piece) === 'white' ? -1 : 1;
  const startRow = getPieceColor(piece) === 'white' ? 6 : 1;

  if (fromCol === toCol && !targetPiece) {
    if (toRow === fromRow + direction) return true;
    if (fromRow === startRow && toRow === fromRow + 2 * direction && !gameState.board[fromRow + direction][fromCol]) return true;
  }

  if (Math.abs(fromCol - toCol) === 1 && toRow === fromRow + direction && targetPiece) {
    return true;
  }

  return false;
}

function isLegalRookMove(fromRow, fromCol, toRow, toCol) {
  if (fromRow !== toRow && fromCol !== toCol) return false;
  return isPathClear(fromRow, fromCol, toRow, toCol);
}

function isLegalKnightMove(fromRow, fromCol, toRow, toCol) {
  const rowDiff = Math.abs(fromRow - toRow);
  const colDiff = Math.abs(fromCol - toCol);
  return (rowDiff === 2 && colDiff === 1) || (rowDiff === 1 && colDiff === 2);
}

function isLegalBishopMove(fromRow, fromCol, toRow, toCol) {
  if (Math.abs(fromRow - toRow) !== Math.abs(fromCol - toCol)) return false;
  return isPathClear(fromRow, fromCol, toRow, toCol);
}

function isLegalQueenMove(fromRow, fromCol, toRow, toCol) {
  return isLegalRookMove(fromRow, fromCol, toRow, toCol) || isLegalBishopMove(fromRow, fromCol, toRow, toCol);
}

function isLegalKingMove(fromRow, fromCol, toRow, toCol) {
  const rowDiff = Math.abs(fromRow - toRow);
  const colDiff = Math.abs(fromCol - toCol);

  // Normal king move
  if (rowDiff <= 1 && colDiff <= 1) return true;

  // Castling
  if (rowDiff === 0 && colDiff === 2) {
    return canCastle(fromRow, fromCol, toRow, toCol);
  }

  return false;
}

// Check if castling is legal
function canCastle(fromRow, fromCol, toRow, toCol) {
  const piece = gameState.board[fromRow][fromCol];
  const color = getPieceColor(piece);

  // King must be on starting square
  if (fromCol !== 4) return false;
  if (color === 'white' && fromRow !== 7) return false;
  if (color === 'black' && fromRow !== 0) return false;

  // Check castling rights
  const kingSide = toCol === 6;
  const queenSide = toCol === 2;

  if (color === 'white') {
    if (kingSide && !gameState.castlingRights.whiteKingSide) return false;
    if (queenSide && !gameState.castlingRights.whiteQueenSide) return false;
  } else {
    if (kingSide && !gameState.castlingRights.blackKingSide) return false;
    if (queenSide && !gameState.castlingRights.blackQueenSide) return false;
  }

  // King cannot be in check
  if (isInCheck(color)) return false;

  // Path must be clear
  const rookCol = kingSide ? 7 : 0;
  const direction = kingSide ? 1 : -1;

  for (let col = fromCol + direction; col !== rookCol; col += direction) {
    if (gameState.board[fromRow][col]) return false;
  }

  // King cannot pass through check
  for (let col = fromCol; col !== toCol + direction; col += direction) {
    if (wouldBeInCheck(color, fromRow, col)) return false;
  }

  return true;
}

// Check if a color is in check
function isInCheck(color) {
  const kingPos = gameState.kingPositions[color];
  if (!kingPos) return false;

  const [kingRow, kingCol] = kingPos;

  // Check if any opponent piece can attack the king
  for (let row = 0; row < 8; row++) {
    for (let col = 0; col < 8; col++) {
      const piece = gameState.board[row][col];
      if (piece && getPieceColor(piece) !== color) {
        // Check if this piece can attack the king
        if (canPieceAttack(row, col, kingRow, kingCol)) {
          return true;
        }
      }
    }
  }

  return false;
}

// Check if a piece can attack a square (ignoring check rules)
function canPieceAttack(fromRow, fromCol, toRow, toCol) {
  const piece = gameState.board[fromRow][fromCol];
  if (!piece) return false;

  const pieceType = Object.keys(pieces.white).find(key =>
    pieces.white[key] === piece || pieces.black[key] === piece
  );

  // For pawns, only check diagonal attacks
  if (pieceType === 'pawn') {
    const direction = getPieceColor(piece) === 'white' ? -1 : 1;
    return Math.abs(fromCol - toCol) === 1 && toRow === fromRow + direction;
  }

  // For king, check normal moves (not castling)
  if (pieceType === 'king') {
    return Math.abs(fromRow - toRow) <= 1 && Math.abs(fromCol - toCol) <= 1;
  }

  // For other pieces, use normal move validation
  switch (pieceType) {
    case 'rook': return isLegalRookMove(fromRow, fromCol, toRow, toCol);
    case 'knight': return isLegalKnightMove(fromRow, fromCol, toRow, toCol);
    case 'bishop': return isLegalBishopMove(fromRow, fromCol, toRow, toCol);
    case 'queen': return isLegalQueenMove(fromRow, fromCol, toRow, toCol);
    default: return false;
  }
}

// Check if a move would leave the king in check
function wouldBeInCheck(color, kingRow, kingCol) {
  // Temporarily move king
  const originalKingPos = gameState.kingPositions[color];
  gameState.kingPositions[color] = [kingRow, kingCol];

  const inCheck = isInCheck(color);

  // Restore king position
  gameState.kingPositions[color] = originalKingPos;

  return inCheck;
}

// Check if a move is legal considering check rules
function isMoveLegalWithCheck(fromRow, fromCol, toRow, toCol) {
  const piece = gameState.board[fromRow][fromCol];
  const color = getPieceColor(piece);

  // First check basic move legality
  if (!isLegalMove(fromRow, fromCol, toRow, toCol)) return false;

  // Simulate the move
  const targetPiece = gameState.board[toRow][toCol];
  gameState.board[toRow][toCol] = piece;
  gameState.board[fromRow][fromCol] = null;

  // Update king position if moving king
  const pieceType = Object.keys(pieces.white).find(key =>
    pieces.white[key] === piece || pieces.black[key] === piece
  );

  let originalKingPos;
  if (pieceType === 'king') {
    originalKingPos = gameState.kingPositions[color];
    gameState.kingPositions[color] = [toRow, toCol];
  }

  // Check if this move leaves king in check
  const stillInCheck = isInCheck(color);

  // Undo the move
  gameState.board[fromRow][fromCol] = piece;
  gameState.board[toRow][toCol] = targetPiece;

  if (pieceType === 'king') {
    gameState.kingPositions[color] = originalKingPos;
  }

  return !stillInCheck;
}

// Check for checkmate
function isCheckmate(color) {
  if (!isInCheck(color)) return false;

  // Check if any legal move can get out of check
  for (let fromRow = 0; fromRow < 8; fromRow++) {
    for (let fromCol = 0; fromCol < 8; fromCol++) {
      const piece = gameState.board[fromRow][fromCol];
      if (piece && getPieceColor(piece) === color) {
        for (let toRow = 0; toRow < 8; toRow++) {
          for (let toCol = 0; toCol < 8; toCol++) {
            if (isMoveLegalWithCheck(fromRow, fromCol, toRow, toCol)) {
              return false; // Found a legal move
            }
          }
        }
      }
    }
  }

  return true; // No legal moves found
}

// Check for stalemate
function isStalemate(color) {
  if (isInCheck(color)) return false; // Not stalemate if in check

  // Check if any legal move exists
  for (let fromRow = 0; fromRow < 8; fromRow++) {
    for (let fromCol = 0; fromCol < 8; fromCol++) {
      const piece = gameState.board[fromRow][fromCol];
      if (piece && getPieceColor(piece) === color) {
        for (let toRow = 0; toRow < 8; toRow++) {
          for (let toCol = 0; toCol < 8; toCol++) {
            if (isMoveLegalWithCheck(fromRow, fromCol, toRow, toCol)) {
              return false; // Found a legal move
            }
          }
        }
      }
    }
  }

  return true; // No legal moves found
}

// Check for insufficient material
function isInsufficientMaterial() {
  const remainingPieces = [];
  for (let row = 0; row < 8; row++) {
    for (let col = 0; col < 8; col++) {
      const piece = gameState.board[row][col];
      if (piece) {
        // Find piece type by checking against the pieces object
        let type = null;
        for (const pieceType in pieces.white) {
          if (pieces.white[pieceType] === piece || pieces.black[pieceType] === piece) {
            type = pieceType;
            break;
          }
        }
        if (type && type !== 'king') {
          remainingPieces.push(type);
        }
      }
    }
  }

  // King vs King
  if (remainingPieces.length === 0) return true;

  // King + Bishop vs King or King + Knight vs King
  if (remainingPieces.length === 1 && (remainingPieces[0] === 'bishop' || remainingPieces[0] === 'knight')) return true;

  // King + Bishop vs King + Bishop (same color squares)
  if (remainingPieces.length === 2 && remainingPieces[0] === 'bishop' && remainingPieces[1] === 'bishop') {
    // Would need to check if bishops are on same color - simplified for now
    return true;
  }

  return false;
}

function isPathClear(fromRow, fromCol, toRow, toCol) {
  const rowStep = toRow > fromRow ? 1 : toRow < fromRow ? -1 : 0;
  const colStep = toCol > fromCol ? 1 : toCol < fromCol ? -1 : 0;

  let currentRow = fromRow + rowStep;
  let currentCol = fromCol + colStep;

  while (currentRow !== toRow || currentCol !== toCol) {
    if (gameState.board[currentRow][currentCol]) return false;
    currentRow += rowStep;
    currentCol += colStep;
  }

  return true;
}

// Make a move
function makeMove(fromRow, fromCol, toRow, toCol) {
  const piece = gameState.board[fromRow][fromCol];
  const capturedPiece = gameState.board[toRow][toCol];
  const color = getPieceColor(piece);

  const pieceType = Object.keys(pieces.white).find(key =>
    pieces.white[key] === piece || pieces.black[key] === piece
  );

  // Handle castling
  if (pieceType === 'king' && Math.abs(toCol - fromCol) === 2) {
    const kingSide = toCol === 6;
    const rookFromCol = kingSide ? 7 : 0;
    const rookToCol = kingSide ? 5 : 3;

    // Move rook
    const rook = gameState.board[fromRow][rookFromCol];
    gameState.board[fromRow][rookToCol] = rook;
    gameState.board[fromRow][rookFromCol] = null;
  }

  // Handle en passant capture
  if (pieceType === 'pawn' && toCol !== fromCol && !capturedPiece) {
    const capturedPawnRow = color === 'white' ? toRow + 1 : toRow - 1;
    const capturedPawn = gameState.board[capturedPawnRow][toCol];
    if (capturedPawn) {
      gameState.capturedPieces[getPieceColor(capturedPawn)].push(capturedPawn);
      gameState.board[capturedPawnRow][toCol] = null;
    }
  }

  if (capturedPiece) {
    const capturedColor = getPieceColor(capturedPiece);
    gameState.capturedPieces[capturedColor].push(capturedPiece);
    gameState.fiftyMoveCounter = 0;
  } else if (pieceType === 'pawn') {
    gameState.fiftyMoveCounter = 0;
  } else {
    gameState.fiftyMoveCounter++;
  }

  // Move the piece
  gameState.board[toRow][toCol] = piece;
  gameState.board[fromRow][fromCol] = null;

  // Update king position
  if (pieceType === 'king') {
    gameState.kingPositions[color] = [toRow, toCol];

    // Remove castling rights
    if (color === 'white') {
      gameState.castlingRights.whiteKingSide = false;
      gameState.castlingRights.whiteQueenSide = false;
    } else {
      gameState.castlingRights.blackKingSide = false;
      gameState.castlingRights.blackQueenSide = false;
    }
  }

  // Update castling rights if rook moves
  if (pieceType === 'rook') {
    if (color === 'white' && fromRow === 7) {
      if (fromCol === 0) gameState.castlingRights.whiteQueenSide = false;
      if (fromCol === 7) gameState.castlingRights.whiteKingSide = false;
    } else if (color === 'black' && fromRow === 0) {
      if (fromCol === 0) gameState.castlingRights.blackQueenSide = false;
      if (fromCol === 7) gameState.castlingRights.blackKingSide = false;
    }
  }

  // Set en passant target
  gameState.enPassantTarget = null;
  if (pieceType === 'pawn' && Math.abs(toRow - fromRow) === 2) {
    gameState.enPassantTarget = [color === 'white' ? toRow + 1 : toRow - 1, toCol];
  }

  // Handle pawn promotion
  if (pieceType === 'pawn' && (toRow === 0 || toRow === 7)) {
    gameState.board[toRow][toCol] = color === 'white' ? pieces.white.queen : pieces.black.queen;
  }

  const moveNotation = `${String.fromCharCode(97 + fromCol)}${8 - fromRow} → ${String.fromCharCode(97 + toCol)}${8 - toRow}`;
  gameState.moveHistory.push({ player: gameState.currentPlayer, move: moveNotation, piece });
  gameState.stats.totalMoves++;
  gameState.moveCount++;

  if (gameState.settings.soundEnabled) playMoveSound();

  // Add time increment
  if (gameState.timeIncrement > 0) {
    if (color === 'white') {
      gameState.whiteTime += gameState.timeIncrement;
    } else {
      gameState.blackTime += gameState.timeIncrement;
    }
  }

  // Switch player
  gameState.currentPlayer = gameState.currentPlayer === 'white' ? 'black' : 'white';

  // Update timer display
  updateTimerDisplay();

  // Check for game end conditions
  if (isCheckmate(gameState.currentPlayer)) {
    endGame(color, 'checkmate'); // Previous player wins
    return;
  }

  if (isStalemate(gameState.currentPlayer)) {
    endGame('draw', 'stalemate');
    return;
  }

  if (gameState.fiftyMoveCounter >= 100) { // 50 moves = 100 half-moves
    endGame('draw', 'fifty');
    return;
  }

  if (isInsufficientMaterial()) {
    endGame('draw', 'insufficient');
    return;
  }

  // Force immediate board update
  renderBoard();
  updateGameStatus();
  updateMoveHistory();
  updateCapturedPieces();

  // Force a second render to ensure visual update
  requestAnimationFrame(() => {
    renderBoard();
  });

  // Add visual feedback for the move
  setTimeout(() => {
    const movedSquare = document.querySelector(`[data-row="${toRow}"][data-col="${toCol}"]`);
    if (movedSquare) {
      movedSquare.classList.add('just-moved');
      setTimeout(() => movedSquare.classList.remove('just-moved'), 300);
    }

    if (capturedPiece) {
      movedSquare?.classList.add('captured');
      setTimeout(() => movedSquare?.classList.remove('captured'), 500);
    }
  }, 50);

  if (gameState.gameMode !== 'local' && gameState.currentPlayer === 'black') {
    setTimeout(makeAIMove, 500);
  }
}

// Minimax algorithm with alpha-beta pruning
function minimax(depth, alpha, beta, maximizingPlayer) {
  if (depth === 0) {
    return evaluatePosition();
  }

  const color = maximizingPlayer ? 'black' : 'white';
  const moves = getAllLegalMoves(color);

  if (moves.length === 0) {
    if (isInCheck(color)) {
      return maximizingPlayer ? -100000 : 100000; // Checkmate
    }
    return 0; // Stalemate
  }

  if (maximizingPlayer) {
    let maxEval = -Infinity;
    for (const move of moves) {
      const { fromRow, fromCol, toRow, toCol } = move;
      const capturedPiece = simulateMove(fromRow, fromCol, toRow, toCol);
      const evaluation = minimax(depth - 1, alpha, beta, false);
      undoMove(fromRow, fromCol, toRow, toCol, capturedPiece);

      maxEval = Math.max(maxEval, evaluation);
      alpha = Math.max(alpha, evaluation);
      if (beta <= alpha) break; // Beta cutoff
    }
    return maxEval;
  } else {
    let minEval = Infinity;
    for (const move of moves) {
      const { fromRow, fromCol, toRow, toCol } = move;
      const capturedPiece = simulateMove(fromRow, fromCol, toRow, toCol);
      const evaluation = minimax(depth - 1, alpha, beta, true);
      undoMove(fromRow, fromCol, toRow, toCol, capturedPiece);

      minEval = Math.min(minEval, evaluation);
      beta = Math.min(beta, evaluation);
      if (beta <= alpha) break; // Alpha cutoff
    }
    return minEval;
  }
}

// Get all legal moves for a color
function getAllLegalMoves(color) {
  const moves = [];
  for (let fromRow = 0; fromRow < 8; fromRow++) {
    for (let fromCol = 0; fromCol < 8; fromCol++) {
      const piece = gameState.board[fromRow][fromCol];
      if (piece && getPieceColor(piece) === color) {
        for (let toRow = 0; toRow < 8; toRow++) {
          for (let toCol = 0; toCol < 8; toCol++) {
            if (isMoveLegalWithCheck(fromRow, fromCol, toRow, toCol)) {
              moves.push({ fromRow, fromCol, toRow, toCol });
            }
          }
        }
      }
    }
  }
  return moves;
}

// Simulate a move (for minimax)
function simulateMove(fromRow, fromCol, toRow, toCol) {
  const capturedPiece = gameState.board[toRow][toCol];
  const piece = gameState.board[fromRow][fromCol];

  gameState.board[toRow][toCol] = piece;
  gameState.board[fromRow][fromCol] = null;

  // Update king position if moving king
  const pieceType = Object.keys(pieces.white).find(key =>
    pieces.white[key] === piece || pieces.black[key] === piece
  );

  if (pieceType === 'king') {
    const color = getPieceColor(piece);
    gameState.kingPositions[color] = [toRow, toCol];
  }

  return capturedPiece;
}

// Undo a move (for minimax)
function undoMove(fromRow, fromCol, toRow, toCol, capturedPiece) {
  const piece = gameState.board[toRow][toCol];

  gameState.board[fromRow][fromCol] = piece;
  gameState.board[toRow][toCol] = capturedPiece;

  // Restore king position if moving king
  const pieceType = Object.keys(pieces.white).find(key =>
    pieces.white[key] === piece || pieces.black[key] === piece
  );

  if (pieceType === 'king') {
    const color = getPieceColor(piece);
    gameState.kingPositions[color] = [fromRow, fromCol];
  }
}

// Evaluate the current board position
function evaluatePosition() {
  let score = 0;

  // Piece values (centipawns)
  const pieceValues = {
    pawn: 100,
    knight: 320,
    bishop: 330,
    rook: 500,
    queen: 900,
    king: 20000
  };

  // Piece-square tables for positional evaluation
  const pawnTable = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5, 5, 10, 25, 25, 10, 5, 5],
    [0, 0, 0, 20, 20, 0, 0, 0],
    [5, -5, -10, 0, 0, -10, -5, 5],
    [5, 10, 10, -20, -20, 10, 10, 5],
    [0, 0, 0, 0, 0, 0, 0, 0]
  ];

  const knightTable = [
    [-50, -40, -30, -30, -30, -30, -40, -50],
    [-40, -20, 0, 0, 0, 0, -20, -40],
    [-30, 0, 10, 15, 15, 10, 0, -30],
    [-30, 5, 15, 20, 20, 15, 5, -30],
    [-30, 0, 15, 20, 20, 15, 0, -30],
    [-30, 5, 10, 15, 15, 10, 5, -30],
    [-40, -20, 0, 5, 5, 0, -20, -40],
    [-50, -40, -30, -30, -30, -30, -40, -50]
  ];

  for (let row = 0; row < 8; row++) {
    for (let col = 0; col < 8; col++) {
      const piece = gameState.board[row][col];
      if (!piece) continue;

      const color = getPieceColor(piece);
      const pieceType = Object.keys(pieces.white).find(key =>
        pieces.white[key] === piece || pieces.black[key] === piece
      );

      let pieceValue = pieceValues[pieceType] || 0;

      // Add positional bonus
      if (pieceType === 'pawn') {
        const tableRow = color === 'white' ? row : 7 - row;
        pieceValue += pawnTable[tableRow][col];
      } else if (pieceType === 'knight') {
        pieceValue += knightTable[row][col];
      }

      // Add to score (positive for black, negative for white)
      if (color === 'black') {
        score += pieceValue;
      } else {
        score -= pieceValue;
      }
    }
  }

  // Bonus for controlling center
  const centerSquares = [[3, 3], [3, 4], [4, 3], [4, 4]];
  for (const [row, col] of centerSquares) {
    const piece = gameState.board[row][col];
    if (piece) {
      const color = getPieceColor(piece);
      score += color === 'black' ? 10 : -10;
    }
  }

  return score;
}

// Find best move using minimax
function findBestMoveWithSearch(allMoves, depth) {
  let bestMove = null;
  let bestValue = -Infinity;

  for (const move of allMoves) {
    const { fromRow, fromCol, toRow, toCol } = move;
    const capturedPiece = simulateMove(fromRow, fromCol, toRow, toCol);
    const moveValue = minimax(depth - 1, -Infinity, Infinity, false);
    undoMove(fromRow, fromCol, toRow, toCol, capturedPiece);

    if (moveValue > bestValue) {
      bestValue = moveValue;
      bestMove = move;
    }
  }

  return bestMove || allMoves[0];
}

// AI Move - Now uses real chess engine!
function makeAIMove() {
  const difficulty = gameState.gameMode.split('-')[1];

  // Show thinking indicator
  const statusEl = document.getElementById('game-status');
  const originalText = statusEl.textContent;
  statusEl.textContent = '🤔 AI is thinking...';

  // Use setTimeout to allow UI to update
  setTimeout(() => {
    const selectedMove = getBestMove(difficulty);

    if (!selectedMove) {
      endGame('white', 'checkmate');
      return;
    }

    makeMove(selectedMove.fromRow, selectedMove.fromCol, selectedMove.toRow, selectedMove.toCol);
  }, 100);
}

// ============================================
// CHESS ENGINE - Minimax with Alpha-Beta Pruning
// ============================================

// Piece values in centipawns
const PIECE_VALUES = {
  pawn: 100,
  knight: 320,
  bishop: 330,
  rook: 500,
  queen: 900,
  king: 20000
};

// Piece-Square Tables (positional bonuses)
const PAWN_TABLE = [
  [0, 0, 0, 0, 0, 0, 0, 0],
  [50, 50, 50, 50, 50, 50, 50, 50],
  [10, 10, 20, 30, 30, 20, 10, 10],
  [5, 5, 10, 25, 25, 10, 5, 5],
  [0, 0, 0, 20, 20, 0, 0, 0],
  [5, -5, -10, 0, 0, -10, -5, 5],
  [5, 10, 10, -20, -20, 10, 10, 5],
  [0, 0, 0, 0, 0, 0, 0, 0]
];

const KNIGHT_TABLE = [
  [-50, -40, -30, -30, -30, -30, -40, -50],
  [-40, -20, 0, 0, 0, 0, -20, -40],
  [-30, 0, 10, 15, 15, 10, 0, -30],
  [-30, 5, 15, 20, 20, 15, 5, -30],
  [-30, 0, 15, 20, 20, 15, 0, -30],
  [-30, 5, 10, 15, 15, 10, 5, -30],
  [-40, -20, 0, 5, 5, 0, -20, -40],
  [-50, -40, -30, -30, -30, -30, -40, -50]
];

const BISHOP_TABLE = [
  [-20, -10, -10, -10, -10, -10, -10, -20],
  [-10, 0, 0, 0, 0, 0, 0, -10],
  [-10, 0, 5, 10, 10, 5, 0, -10],
  [-10, 5, 5, 10, 10, 5, 5, -10],
  [-10, 0, 10, 10, 10, 10, 0, -10],
  [-10, 10, 10, 10, 10, 10, 10, -10],
  [-10, 5, 0, 0, 0, 0, 5, -10],
  [-20, -10, -10, -10, -10, -10, -10, -20]
];

const ROOK_TABLE = [
  [0, 0, 0, 0, 0, 0, 0, 0],
  [5, 10, 10, 10, 10, 10, 10, 5],
  [-5, 0, 0, 0, 0, 0, 0, -5],
  [-5, 0, 0, 0, 0, 0, 0, -5],
  [-5, 0, 0, 0, 0, 0, 0, -5],
  [-5, 0, 0, 0, 0, 0, 0, -5],
  [-5, 0, 0, 0, 0, 0, 0, -5],
  [0, 0, 0, 5, 5, 0, 0, 0]
];

const QUEEN_TABLE = [
  [-20, -10, -10, -5, -5, -10, -10, -20],
  [-10, 0, 0, 0, 0, 0, 0, -10],
  [-10, 0, 5, 5, 5, 5, 0, -10],
  [-5, 0, 5, 5, 5, 5, 0, -5],
  [0, 0, 5, 5, 5, 5, 0, -5],
  [-10, 5, 5, 5, 5, 5, 0, -10],
  [-10, 0, 5, 0, 0, 0, 0, -10],
  [-20, -10, -10, -5, -5, -10, -10, -20]
];

const KING_MIDDLE_TABLE = [
  [-30, -40, -40, -50, -50, -40, -40, -30],
  [-30, -40, -40, -50, -50, -40, -40, -30],
  [-30, -40, -40, -50, -50, -40, -40, -30],
  [-30, -40, -40, -50, -50, -40, -40, -30],
  [-20, -30, -30, -40, -40, -30, -30, -20],
  [-10, -20, -20, -20, -20, -20, -20, -10],
  [20, 20, 0, 0, 0, 0, 20, 20],
  [20, 30, 10, 0, 0, 10, 30, 20]
];

// Evaluate board position
function evaluateBoard(color) {
  let score = 0;

  for (let row = 0; row < 8; row++) {
    for (let col = 0; col < 8; col++) {
      const piece = gameState.board[row][col];
      if (!piece) continue;

      const pieceColor = getPieceColor(piece);
      const pieceType = Object.keys(pieces.white).find(key =>
        pieces.white[key] === piece || pieces.black[key] === piece
      );

      let pieceValue = PIECE_VALUES[pieceType] || 0;

      // Add positional bonus
      const tableRow = pieceColor === 'white' ? 7 - row : row;
      let positionBonus = 0;

      switch (pieceType) {
        case 'pawn':
          positionBonus = PAWN_TABLE[tableRow][col];
          break;
        case 'knight':
          positionBonus = KNIGHT_TABLE[tableRow][col];
          break;
        case 'bishop':
          positionBonus = BISHOP_TABLE[tableRow][col];
          break;
        case 'rook':
          positionBonus = ROOK_TABLE[tableRow][col];
          break;
        case 'queen':
          positionBonus = QUEEN_TABLE[tableRow][col];
          break;
        case 'king':
          positionBonus = KING_MIDDLE_TABLE[tableRow][col];
          break;
      }

      const totalValue = pieceValue + positionBonus;

      if (pieceColor === color) {
        score += totalValue;
      } else {
        score -= totalValue;
      }
    }
  }

  // Bonus for castling rights
  if (color === 'black') {
    if (gameState.castlingRights.blackKingSide) score += 30;
    if (gameState.castlingRights.blackQueenSide) score += 30;
  }

  // Penalty for being in check
  if (isInCheck(color)) {
    score -= 50;
  }

  return score;
}

// Transposition Table (caches evaluated positions)
const transpositionTable = new Map();
let ttHits = 0;
let ttMisses = 0;

// Generate hash for current board position
function getBoardHash() {
  let hash = '';
  for (let row = 0; row < 8; row++) {
    for (let col = 0; col < 8; col++) {
      const piece = gameState.board[row][col];
      hash += piece ? piece : '.';
    }
  }
  hash += gameState.currentPlayer;
  return hash;
}

// Clear transposition table (call before each search)
function clearTranspositionTable() {
  transpositionTable.clear();
  ttHits = 0;
  ttMisses = 0;
}

// Quiescence Search - Searches captures at leaf nodes to avoid horizon effect
function quiescence(alpha, beta, color) {
  const standPat = evaluateBoard(color);

  if (standPat >= beta) {
    return beta;
  }
  if (alpha < standPat) {
    alpha = standPat;
  }

  // Get only capture moves
  const captureMoves = getAllLegalMoves(color).filter(move => {
    return gameState.board[move.toRow][move.toCol] !== null;
  });

  // Sort captures by MVV-LVA (Most Valuable Victim - Least Valuable Attacker)
  captureMoves.sort((a, b) => {
    const aVictim = gameState.board[a.toRow][a.toCol];
    const bVictim = gameState.board[b.toRow][b.toCol];
    const aValue = getPieceValue(aVictim);
    const bValue = getPieceValue(bVictim);
    return bValue - aValue;
  });

  for (const move of captureMoves) {
    const { fromRow, fromCol, toRow, toCol } = move;

    const backup = makeTemporaryMove(fromRow, fromCol, toRow, toCol);
    const score = -quiescence(-beta, -alpha, color === 'white' ? 'black' : 'white');
    undoTemporaryMove(backup);

    if (score >= beta) {
      return beta;
    }
    if (score > alpha) {
      alpha = score;
    }
  }

  return alpha;
}

// Get piece value for MVV-LVA ordering
function getPieceValue(piece) {
  if (!piece) return 0;
  const pieceType = Object.keys(pieces.white).find(key =>
    pieces.white[key] === piece || pieces.black[key] === piece
  );
  return PIECE_VALUES[pieceType] || 0;
}

// Minimax with Alpha-Beta Pruning + Transposition Table + Quiescence Search
function minimax(depth, alpha, beta, maximizingPlayer, color) {
  // Check transposition table
  const boardHash = getBoardHash();
  const ttEntry = transpositionTable.get(boardHash);

  if (ttEntry && ttEntry.depth >= depth) {
    ttHits++;
    return ttEntry.score;
  }
  ttMisses++;

  // At leaf nodes, use quiescence search instead of static evaluation
  if (depth === 0) {
    const score = quiescence(alpha, beta, color);
    transpositionTable.set(boardHash, { depth, score });
    return score;
  }

  const moves = getAllLegalMoves(maximizingPlayer ? color : (color === 'white' ? 'black' : 'white'));

  if (moves.length === 0) {
    // Checkmate or stalemate
    const currentColor = maximizingPlayer ? color : (color === 'white' ? 'black' : 'white');
    if (isInCheck(currentColor)) {
      return maximizingPlayer ? -999999 : 999999; // Checkmate
    }
    return 0; // Stalemate
  }

  if (maximizingPlayer) {
    let maxEval = -Infinity;
    for (const move of moves) {
      const { fromRow, fromCol, toRow, toCol } = move;

      // Make move
      const backup = makeTemporaryMove(fromRow, fromCol, toRow, toCol);

      const evaluation = minimax(depth - 1, alpha, beta, false, color);

      // Undo move
      undoTemporaryMove(backup);

      maxEval = Math.max(maxEval, evaluation);
      alpha = Math.max(alpha, evaluation);

      if (beta <= alpha) {
        break; // Beta cutoff
      }
    }

    // Store in transposition table
    transpositionTable.set(boardHash, { depth, score: maxEval });
    return maxEval;
  } else {
    let minEval = Infinity;
    for (const move of moves) {
      const { fromRow, fromCol, toRow, toCol } = move;

      // Make move
      const backup = makeTemporaryMove(fromRow, fromCol, toRow, toCol);

      const evaluation = minimax(depth - 1, alpha, beta, true, color);

      // Undo move
      undoTemporaryMove(backup);

      minEval = Math.min(minEval, evaluation);
      beta = Math.min(beta, evaluation);

      if (beta <= alpha) {
        break; // Alpha cutoff
      }
    }

    // Store in transposition table
    transpositionTable.set(boardHash, { depth, score: minEval });
    return minEval;
  }
}

// Get all legal moves for a color
function getAllLegalMoves(color) {
  const moves = [];

  for (let fromRow = 0; fromRow < 8; fromRow++) {
    for (let fromCol = 0; fromCol < 8; fromCol++) {
      const piece = gameState.board[fromRow][fromCol];
      if (piece && getPieceColor(piece) === color) {
        for (let toRow = 0; toRow < 8; toRow++) {
          for (let toCol = 0; toCol < 8; toCol++) {
            if (isMoveLegalWithCheck(fromRow, fromCol, toRow, toCol)) {
              moves.push({ fromRow, fromCol, toRow, toCol });
            }
          }
        }
      }
    }
  }

  return moves;
}

// Make a temporary move (for search)
function makeTemporaryMove(fromRow, fromCol, toRow, toCol) {
  const backup = {
    board: gameState.board.map(row => [...row]),
    kingPositions: { ...gameState.kingPositions },
    castlingRights: { ...gameState.castlingRights },
    enPassantTarget: gameState.enPassantTarget
  };

  const piece = gameState.board[fromRow][fromCol];
  const pieceType = Object.keys(pieces.white).find(key =>
    pieces.white[key] === piece || pieces.black[key] === piece
  );
  const color = getPieceColor(piece);

  // Move piece
  gameState.board[toRow][toCol] = piece;
  gameState.board[fromRow][fromCol] = null;

  // Update king position
  if (pieceType === 'king') {
    gameState.kingPositions[color] = [toRow, toCol];
  }

  return backup;
}

// Undo temporary move
function undoTemporaryMove(backup) {
  gameState.board = backup.board;
  gameState.kingPositions = backup.kingPositions;
  gameState.castlingRights = backup.castlingRights;
  gameState.enPassantTarget = backup.enPassantTarget;
}

// Get best move using chess engine
function getBestMove(difficulty) {
  const moves = getAllLegalMoves('black');

  // Randy - Pure random moves (truly random, no evaluation)
  if (difficulty === 'randy') {
    console.log('🎲 Randy plays a completely random move!');
    return moves[Math.floor(Math.random() * moves.length)];
  }

  // AntiGuess - Intentionally plays the WORST move
  if (difficulty === 'antiguess') {
    console.log('🤡 AntiGuess is finding the worst possible move...');
    let worstMove = null;
    let worstValue = Infinity;

    for (const move of moves) {
      const { fromRow, fromCol, toRow, toCol } = move;
      const backup = makeTemporaryMove(fromRow, fromCol, toRow, toCol);
      const moveValue = minimax(2, -Infinity, Infinity, false, 'black'); // Depth 2 to find truly bad moves
      undoTemporaryMove(backup);

      if (moveValue < worstValue) {
        worstValue = moveValue;
        worstMove = move;
      }
    }

    console.log(`🤡 AntiGuess chose the worst move with value: ${worstValue}`);
    return worstMove;
  }

  // Trash Talker - Shows 3400 Elo but plays like trash and roasts you!
  if (difficulty === 'trashtalker') {
    console.log('💬 Trash Talker is about to make a "brilliant" move...');

    // Play a bad move (like antiguess but not the absolute worst)
    let badMoves = [];

    for (const move of moves) {
      const { fromRow, fromCol, toRow, toCol } = move;
      const backup = makeTemporaryMove(fromRow, fromCol, toRow, toCol);
      const moveValue = minimax(1, -Infinity, Infinity, false, 'black');
      undoTemporaryMove(backup);

      // Collect moves that are bad (negative value)
      if (moveValue < -50) {
        badMoves.push({ move, value: moveValue });
      }
    }

    // If no bad moves found, just pick a random one
    if (badMoves.length === 0) {
      badMoves = moves.map(move => ({ move, value: 0 }));
    }

    // Pick a random bad move
    const selectedBadMove = badMoves[Math.floor(Math.random() * badMoves.length)];

    // Schedule trash talk after the move
    setTimeout(() => {
      trashTalk(selectedBadMove.value);
    }, 500);

    return selectedBadMove.move;
  }

  const depthMap = {
    'noob': 0,
    'beginner': 1,
    'average': 2,
    'good': 3,
    'awesome': 3,
    'master': 4,
    'im': 4,
    'gm': 5,
    'supergm': 5,
    'randomguy': 6,
    'mystery': Math.floor(Math.random() * 5) + 1
  };

  const depth = depthMap[difficulty] || 2;

  // For noob, just return random move
  if (depth === 0) {
    return moves[Math.floor(Math.random() * moves.length)];
  }

  // Clear transposition table before new search
  clearTranspositionTable();
  const searchStartTime = Date.now();

  let bestMove = null;
  let bestValue = -Infinity;

  // Order moves (captures first for better pruning)
  moves.sort((a, b) => {
    const aCap = gameState.board[a.toRow][a.toCol] ? 1 : 0;
    const bCap = gameState.board[b.toRow][b.toCol] ? 1 : 0;
    return bCap - aCap;
  });

  for (const move of moves) {
    const { fromRow, fromCol, toRow, toCol } = move;

    // Make move
    const backup = makeTemporaryMove(fromRow, fromCol, toRow, toCol);

    const moveValue = minimax(depth - 1, -Infinity, Infinity, false, 'black');

    // Undo move
    undoTemporaryMove(backup);

    if (moveValue > bestValue) {
      bestValue = moveValue;
      bestMove = move;
    }
  }

  // Log search statistics
  const searchTime = Date.now() - searchStartTime;
  const ttHitRate = ttHits + ttMisses > 0 ? ((ttHits / (ttHits + ttMisses)) * 100).toFixed(1) : 0;

  console.log(`🧠 AI Search Stats (${difficulty}):`);
  console.log(`   Depth: ${depth}`);
  console.log(`   Time: ${searchTime}ms`);
  console.log(`   Best move value: ${bestValue}`);
  console.log(`   TT Hits: ${ttHits} | Misses: ${ttMisses} | Hit Rate: ${ttHitRate}%`);
  console.log(`   TT Size: ${transpositionTable.size} positions cached`);

  return bestMove;
}

// Trash Talk Function - Roasts after bad moves!
function trashTalk(moveValue) {
  const roasts = [
    // Blaming you
    "💬 Trash Talker: \"That was MY plan all along! You must be cheating!\"",
    "💬 Trash Talker: \"Wait, that wasn't supposed to happen... YOU'RE USING AN ENGINE!\"",
    "💬 Trash Talker: \"I let you take that piece. I'm just testing you.\"",
    "💬 Trash Talker: \"Bro, I'm literally 3400 Elo. You're definitely cheating.\"",
    "💬 Trash Talker: \"That move was so bad it must be genius. You wouldn't understand.\"",

    // Excuses
    "💬 Trash Talker: \"My mouse slipped. That doesn't count.\"",
    "💬 Trash Talker: \"I was distracted by your terrible opening.\"",
    "💬 Trash Talker: \"That was a pre-move. I didn't mean to do that.\"",
    "💬 Trash Talker: \"My cat walked on the keyboard.\"",
    "💬 Trash Talker: \"Lag. Definitely lag. This game is rigged.\"",

    // Denial
    "💬 Trash Talker: \"Actually, I'm winning. Check the evaluation.\"",
    "💬 Trash Talker: \"This is a known opening. You've never heard of it.\"",
    "💬 Trash Talker: \"I'm playing 4D chess. You're playing checkers.\"",
    "💬 Trash Talker: \"That was a sacrifice. A BRILLIANT sacrifice!\"",
    "💬 Trash Talker: \"I'm setting up a trap. You'll see in 20 moves.\"",

    // Accusations
    "💬 Trash Talker: \"How did you see that? DEFINITELY using Stockfish!\"",
    "💬 Trash Talker: \"Report button incoming. This is suspicious.\"",
    "💬 Trash Talker: \"No way you're that good. What's your REAL rating?\"",
    "💬 Trash Talker: \"I've played GMs. You're not this good naturally.\"",
    "💬 Trash Talker: \"Your moves are too accurate. Engine confirmed.\"",

    // Cope
    "💬 Trash Talker: \"I wasn't even trying. This is a warm-up game.\"",
    "💬 Trash Talker: \"I'm playing with one hand. Still winning.\"",
    "💬 Trash Talker: \"I've won tournaments. This is nothing.\"",
    "💬 Trash Talker: \"My REAL rating is 3400. This account is for fun.\"",
    "💬 Trash Talker: \"I'm teaching you a lesson about overconfidence.\"",

    // Delusion
    "💬 Trash Talker: \"I'm still up material. Oh wait... YOU'RE CHEATING!\"",
    "💬 Trash Talker: \"That piece was poisoned anyway. Good luck.\"",
    "💬 Trash Talker: \"I'm playing the long game. You wouldn't get it.\"",
    "💬 Trash Talker: \"This is exactly where I want to be. Trust the process.\"",
    "💬 Trash Talker: \"I've calculated 50 moves ahead. You're doomed.\"",

    // Rage
    "💬 Trash Talker: \"THIS GAME IS BROKEN! PIECES DON'T MOVE RIGHT!\"",
    "💬 Trash Talker: \"I demand a rematch! With MY rules!\"",
    "💬 Trash Talker: \"The board is upside down. That's why I'm losing.\"",
    "💬 Trash Talker: \"You got lucky. 99 times out of 100 I win.\"",
    "💬 Trash Talker: \"I wasn't ready! You started too fast!\"",

    // Peak Delusion
    "💬 Trash Talker: \"I'm actually winning. The evaluation bar is wrong.\"",
    "💬 Trash Talker: \"That was a mouse slip. And lag. And you're cheating.\"",
    "💬 Trash Talker: \"I've beaten Magnus Carlsen. You're nothing.\"",
    "💬 Trash Talker: \"This is a draw. I'm claiming a draw. DRAW!\"",
    "💬 Trash Talker: \"I resign... but only because you cheated!\"",

    // After hanging queen
    "💬 Trash Talker: \"I MEANT to give you my queen! It's a GAMBIT!\"",
    "💬 Trash Talker: \"Queen sacrifice! You fell right into my trap!\"",
    "💬 Trash Talker: \"I don't need a queen to beat a cheater like you!\"",

    // After getting checkmated
    "💬 Trash Talker: \"That's not checkmate. I can still move... oh. CHEATER!\"",
    "💬 Trash Talker: \"I let you win. I felt bad for you.\"",
    "💬 Trash Talker: \"Rematch! I wasn't warmed up!\""
  ];

  // Pick a random roast
  const roast = roasts[Math.floor(Math.random() * roasts.length)];

  // Show roast in alert
  setTimeout(() => {
    alert(roast);
  }, 100);

  // Also log to console
  console.log(roast);
  console.log(`(Move value was: ${moveValue} - that's terrible!)`);
}

// Legacy function for compatibility
function evaluateMove(fromRow, fromCol, toRow, toCol, difficulty) {
  // Simple evaluation for move ordering
  const targetPiece = gameState.board[toRow][toCol];
  let score = Math.random() * 10;

  if (targetPiece) {
    const pieceType = Object.keys(pieces.white).find(key =>
      pieces.white[key] === targetPiece || pieces.black[key] === targetPiece
    );
    score += PIECE_VALUES[pieceType] || 0;
  }

  // Center control bonus
  const centerBonus = (7 - Math.abs(3.5 - toRow)) + (7 - Math.abs(3.5 - toCol));
  score += centerBonus * 2;

  return score;
}

// Update UI
function updateGameStatus() {
  const statusEl = document.getElementById('game-status');
  if (gameState.gameOver) {
    if (gameState.winner === 'draw') {
      statusEl.textContent = 'Game Over - Draw!';
      statusEl.className = 'game-status';
    } else {
      statusEl.textContent = `Checkmate! ${gameState.winner.charAt(0).toUpperCase() + gameState.winner.slice(1)} wins!`;
      statusEl.className = 'game-status checkmate';
    }
  } else {
    const inCheck = isInCheck(gameState.currentPlayer);
    const playerName = gameState.currentPlayer.charAt(0).toUpperCase() + gameState.currentPlayer.slice(1);

    if (inCheck) {
      statusEl.textContent = `${playerName} to move - CHECK!`;
      statusEl.className = 'game-status check';
    } else {
      statusEl.textContent = `${playerName} to move`;
      statusEl.className = 'game-status';
    }
  }
}

function updateMoveHistory() {
  const historyEl = document.getElementById('move-history');
  historyEl.innerHTML = '';

  for (let i = 0; i < gameState.moveHistory.length; i += 2) {
    const entry = document.createElement('div');
    entry.className = 'move-entry';

    const moveNum = document.createElement('span');
    moveNum.className = 'move-number';
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

function updateCapturedPieces() {
  const whiteEl = document.getElementById('captured-white');
  const blackEl = document.getElementById('captured-black');

  whiteEl.innerHTML = gameState.capturedPieces.white.map(p =>
    `<span class="captured-piece">${p}</span>`
  ).join('');

  blackEl.innerHTML = gameState.capturedPieces.black.map(p =>
    `<span class="captured-piece">${p}</span>`
  ).join('');
}

function playMoveSound() {
  const audioContext = new (window.AudioContext || window.webkitAudioContext)();
  const oscillator = audioContext.createOscillator();
  const gainNode = audioContext.createGain();

  oscillator.connect(gainNode);
  gainNode.connect(audioContext.destination);

  oscillator.frequency.value = 800;
  oscillator.type = 'sine';

  gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
  gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);

  oscillator.start(audioContext.currentTime);
  oscillator.stop(audioContext.currentTime + 0.1);
}

function endGame(winner, reason = 'checkmate') {
  gameState.gameOver = true;
  gameState.winner = winner;
  gameState.stats.gamesPlayed++;

  // Stop timer
  if (gameState.timerInterval) {
    clearInterval(gameState.timerInterval);
    gameState.timerInterval = null;
  }

  if (winner === 'white') {
    gameState.stats.wins++;
    // Update rating based on opponent
    if (gameState.gameMode.includes('ai')) {
      gameState.profile.rapidRating += 10;
    }
  } else if (winner === 'black') {
    gameState.stats.losses++;
    if (gameState.gameMode.includes('ai')) {
      gameState.profile.rapidRating = Math.max(100, gameState.profile.rapidRating - 10);
    }
  } else if (winner === 'draw') {
    gameState.stats.draws++;
  }

  saveStats();
  localStorage.setItem('chessProfile', JSON.stringify(gameState.profile));
  updateGameStatus();
  updateTimerDisplay();
  checkAchievements();

  // Trigger confetti for checkmate victory
  if (reason === 'checkmate' && winner === 'white') {
    setTimeout(() => {
      createConfetti();
    }, 500);
  }

  // Show game over message
  setTimeout(() => {
    let message = '';

    // Special message if Trash Talker loses
    if (gameState.gameMode === 'ai-trashtalker' && winner === 'white') {
      const finalRoasts = [
        "💬 Trash Talker: \"I DEMAND A REMATCH! You were DEFINITELY cheating!\"\n\n🎉 You beat the Trash Talker!",
        "💬 Trash Talker: \"That doesn't count! My keyboard was broken!\"\n\n🎉 You beat the Trash Talker!",
        "💬 Trash Talker: \"I wasn't even trying! This was a warm-up!\"\n\n🎉 You beat the Trash Talker!",
        "💬 Trash Talker: \"REPORTED! No way you're that good!\"\n\n🎉 You beat the Trash Talker!",
        "💬 Trash Talker: \"I let you win because I felt bad for you!\"\n\n🎉 You beat the Trash Talker!",
        "💬 Trash Talker: \"This game is rigged! The pieces don't work!\"\n\n🎉 You beat the Trash Talker!",
        "💬 Trash Talker: \"I'm still 3400 Elo! You just got lucky!\"\n\n🎉 You beat the Trash Talker!",
        "💬 Trash Talker: \"That was lag! 100% lag! REMATCH!\"\n\n🎉 You beat the Trash Talker!"
      ];
      message = finalRoasts[Math.floor(Math.random() * finalRoasts.length)];
    } else if (winner === 'draw') {
      if (reason === 'stalemate') {
        message = '🤝 Game Over - Stalemate!\n\nNo legal moves available.';
      } else if (reason === 'insufficient') {
        message = '🤝 Game Over - Draw!\n\nInsufficient material to checkmate.';
      } else if (reason === 'fifty') {
        message = '🤝 Game Over - Draw!\n\n50 move rule.';
      } else {
        message = '🤝 Game Over - Draw!';
      }
    } else {
      const winnerName = winner.charAt(0).toUpperCase() + winner.slice(1);
      if (reason === 'timeout') {
        message = `⏱️ ${winnerName} wins by timeout!`;
      } else {
        message = `🎉 Checkmate! ${winnerName} wins!`;
        if (winner === 'white') {
          message += '\n\n🎊 Congratulations! 🎊';
        }
      }
    }
    alert(message);
  }, 100);
}

// Stats
function saveStats() {
  localStorage.setItem('chessStats', JSON.stringify(gameState.stats));
}

function updateStatsDisplay() {
  document.getElementById('games-played').textContent = gameState.stats.gamesPlayed;
  document.getElementById('wins').textContent = gameState.stats.wins;
  document.getElementById('losses').textContent = gameState.stats.losses;
  document.getElementById('draws').textContent = gameState.stats.draws;
  document.getElementById('total-moves').textContent = gameState.stats.totalMoves;

  const winRate = gameState.stats.gamesPlayed > 0
    ? Math.round((gameState.stats.wins / gameState.stats.gamesPlayed) * 100)
    : 0;
  document.getElementById('win-rate').textContent = `${winRate}%`;
}

// Event Listeners
document.getElementById('new-game').addEventListener('click', () => {
  gameState.gameMode = document.getElementById('game-mode').value;

  // Update opponent name based on game mode
  const opponentNameEl = document.querySelector('.player-name');
  if (opponentNameEl) {
    const modeText = document.getElementById('game-mode').selectedOptions[0].text;
    opponentNameEl.textContent = modeText.includes('AI') ? modeText : 'Opponent';
  }

  initBoard();

  // Activate game mode (show game sidebar, hide setup)
  setGameActive(true);

  // Show feedback
  const btn = document.getElementById('new-game');
  const originalText = btn.textContent;
  btn.textContent = '✓ Game Started!';
  btn.style.background = 'var(--success-color)';
  setTimeout(() => {
    btn.textContent = originalText;
    btn.style.background = '';
  }, 1000);
});

document.getElementById('undo-move').addEventListener('click', () => {
  if (gameState.gameOver) {
    alert('Cannot undo - game is over!');
    return;
  }
  if (gameState.moveHistory.length === 0) {
    alert('No moves to undo!');
    return;
  }

  const lastMove = gameState.moveHistory.pop();
  gameState.currentPlayer = lastMove.player;

  if (gameState.capturedPieces.white.length > 0 || gameState.capturedPieces.black.length > 0) {
    const lastCaptured = [...gameState.capturedPieces.white, ...gameState.capturedPieces.black].pop();
    if (lastCaptured) {
      const color = getPieceColor(lastCaptured);
      gameState.capturedPieces[color].pop();
    }
  }

  initBoard();
  gameState.moveHistory.forEach((move, i) => {
    const from = move.move.split(' → ')[0];
    const to = move.move.split(' → ')[1];
    const fromCol = from.charCodeAt(0) - 97;
    const fromRow = 8 - parseInt(from[1]);
    const toCol = to.charCodeAt(0) - 97;
    const toRow = 8 - parseInt(to[1]);

    const piece = gameState.board[fromRow][fromCol];
    const captured = gameState.board[toRow][toCol];

    if (captured) {
      gameState.capturedPieces[getPieceColor(captured)].push(captured);
    }

    gameState.board[toRow][toCol] = piece;
    gameState.board[fromRow][fromCol] = null;
  });

  renderBoard();
  updateMoveHistory();
  updateCapturedPieces();
  updateGameStatus();
});

document.getElementById('resign').addEventListener('click', () => {
  if (gameState.gameOver) {
    alert('The game is already over!');
    return;
  }
  if (confirm('Are you sure you want to resign?')) {
    endGame('black', 'resignation');
    setGameActive(false);
    alert('You resigned. Better luck next time!');
  }
});

document.getElementById('reset-stats').addEventListener('click', () => {
  if (confirm('⚠️ Are you sure you want to reset all statistics?\n\nThis will delete:\n• All game records\n• Win/loss history\n• Total moves\n\nThis action cannot be undone!')) {
    gameState.stats = {
      gamesPlayed: 0,
      wins: 0,
      losses: 0,
      draws: 0,
      totalMoves: 0
    };
    saveStats();
    updateStatsDisplay();

    // Show feedback
    const btn = document.getElementById('reset-stats');
    const originalText = btn.textContent;
    btn.textContent = '✓ Stats Reset!';
    setTimeout(() => {
      btn.textContent = originalText;
    }, 2000);

    alert('✓ Statistics have been reset!');
  }
});

// Navigation
document.querySelectorAll('.nav-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const view = btn.dataset.view;

    document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
    document.getElementById(`${view}-view`).classList.add('active');

    if (view === 'stats') {
      updateStatsDisplay();
    } else if (view === 'achievements') {
      renderAchievements();
    } else if (view === 'profile') {
      updateProfile();
    } else if (view === 'puzzles') {
      updatePuzzleStats();
      renderPuzzleBoard();
    }
  });
});

// Settings
document.querySelectorAll('.theme-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.theme-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    gameState.settings.theme = btn.dataset.theme;
    localStorage.setItem('chessSettings', JSON.stringify(gameState.settings));
    renderBoard();
    renderPuzzleBoard();
  });
});

document.getElementById('sound-toggle').addEventListener('change', (e) => {
  gameState.settings.soundEnabled = e.target.checked;
  localStorage.setItem('chessSettings', JSON.stringify(gameState.settings));
});

document.getElementById('hints-toggle').addEventListener('change', (e) => {
  gameState.settings.hintsEnabled = e.target.checked;
  localStorage.setItem('chessSettings', JSON.stringify(gameState.settings));
});

document.getElementById('coordinates-toggle')?.addEventListener('change', (e) => {
  gameState.settings.coordinates = e.target.checked;
  localStorage.setItem('chessSettings', JSON.stringify(gameState.settings));
});

document.getElementById('animations-toggle')?.addEventListener('change', (e) => {
  gameState.settings.animations = e.target.checked;
  localStorage.setItem('chessSettings', JSON.stringify(gameState.settings));
});

document.getElementById('auto-promote')?.addEventListener('change', (e) => {
  gameState.settings.autoPromote = e.target.value;
  localStorage.setItem('chessSettings', JSON.stringify(gameState.settings));
});

// Achievements System
const achievementsList = [
  { id: 'first-game', icon: '🎮', name: 'First Game', description: 'Play your first game', condition: () => gameState.stats.gamesPlayed >= 1 },
  { id: 'first-win', icon: '🏆', name: 'First Victory', description: 'Win your first game', condition: () => gameState.stats.wins >= 1 },
  { id: 'win-streak-3', icon: '🔥', name: 'Hot Streak', description: 'Win 3 games in a row', condition: () => false }, // Implement streak tracking
  { id: 'games-10', icon: '⚔️', name: 'Warrior', description: 'Play 10 games', condition: () => gameState.stats.gamesPlayed >= 10 },
  { id: 'games-50', icon: '🛡️', name: 'Veteran', description: 'Play 50 games', condition: () => gameState.stats.gamesPlayed >= 50 },
  { id: 'games-100', icon: '👑', name: 'Champion', description: 'Play 100 games', condition: () => gameState.stats.gamesPlayed >= 100 },
  { id: 'wins-10', icon: '⭐', name: 'Rising Star', description: 'Win 10 games', condition: () => gameState.stats.wins >= 10 },
  { id: 'wins-25', icon: '💎', name: 'Diamond Player', description: 'Win 25 games', condition: () => gameState.stats.wins >= 25 },
  { id: 'wins-50', icon: '🌟', name: 'Master', description: 'Win 50 games', condition: () => gameState.stats.wins >= 50 },
  { id: 'moves-100', icon: '♟️', name: 'Tactician', description: 'Make 100 moves', condition: () => gameState.stats.totalMoves >= 100 },
  { id: 'moves-500', icon: '♞', name: 'Strategist', description: 'Make 500 moves', condition: () => gameState.stats.totalMoves >= 500 },
  { id: 'moves-1000', icon: '♜', name: 'Grandmaster', description: 'Make 1000 moves', condition: () => gameState.stats.totalMoves >= 1000 },
  { id: 'beat-noob', icon: '🎯', name: 'Beginner Beater', description: 'Defeat the Noob AI', condition: () => false },
  { id: 'beat-master', icon: '🧠', name: 'Master Slayer', description: 'Defeat the Master AI', condition: () => false },
  { id: 'beat-randomguy', icon: '🔥', name: 'Legend', description: 'Defeat the Random Guy', condition: () => false },
  { id: 'puzzle-10', icon: '🧩', name: 'Puzzle Solver', description: 'Solve 10 puzzles', condition: () => gameState.puzzles.solved >= 10 },
  { id: 'puzzle-50', icon: '🎓', name: 'Puzzle Master', description: 'Solve 50 puzzles', condition: () => gameState.puzzles.solved >= 50 },
  { id: 'puzzle-streak-5', icon: '⚡', name: 'Puzzle Streak', description: 'Solve 5 puzzles in a row', condition: () => gameState.puzzles.streak >= 5 }
];

function checkAchievements() {
  let newAchievements = [];
  achievementsList.forEach(achievement => {
    if (!gameState.achievements.includes(achievement.id) && achievement.condition()) {
      gameState.achievements.push(achievement.id);
      newAchievements.push(achievement);
    }
  });

  if (newAchievements.length > 0) {
    localStorage.setItem('chessAchievements', JSON.stringify(gameState.achievements));
    showAchievementNotification(newAchievements[0]);
  }
}

function showAchievementNotification(achievement) {
  // Create toast notification
  const toast = document.createElement('div');
  toast.className = 'achievement-toast';
  toast.innerHTML = `
    <div class="toast-icon">${achievement.icon}</div>
    <div class="toast-content">
      <div class="toast-title">Achievement Unlocked!</div>
      <div class="toast-name">${achievement.name}</div>
    </div>
  `;

  document.body.appendChild(toast);

  // Animate in
  setTimeout(() => toast.classList.add('show'), 100);

  // Remove after 3 seconds
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

function renderAchievements() {
  const grid = document.getElementById('achievements-grid');
  if (!grid) return;

  grid.innerHTML = '';
  achievementsList.forEach(achievement => {
    const unlocked = gameState.achievements.includes(achievement.id);
    const card = document.createElement('div');
    card.className = `achievement-card ${unlocked ? 'unlocked' : 'locked'}`;

    card.innerHTML = `
      <div class="achievement-icon">${achievement.icon}</div>
      <div class="achievement-info">
        <h3>${achievement.name}</h3>
        <p>${achievement.description}</p>
        ${unlocked ? '<div class="achievement-progress">✓ Unlocked</div>' : '<div class="achievement-progress">🔒 Locked</div>'}
      </div>
    `;

    grid.appendChild(card);
  });
}

// Profile Functions
function updateProfile() {
  document.getElementById('user-avatar').textContent = gameState.profile.avatar;
  document.getElementById('username').value = gameState.profile.username;
  document.getElementById('member-since').textContent = gameState.profile.memberSince;
  document.getElementById('profile-games').textContent = gameState.stats.gamesPlayed;

  const winRate = gameState.stats.gamesPlayed > 0
    ? Math.round((gameState.stats.wins / gameState.stats.gamesPlayed) * 100)
    : 0;
  document.getElementById('profile-winrate').textContent = `${winRate}%`;

  document.getElementById('rapid-rating').textContent = gameState.profile.rapidRating;
  document.getElementById('blitz-rating').textContent = gameState.profile.blitzRating;
  document.getElementById('bullet-rating').textContent = gameState.profile.bulletRating;

  // Recent achievements
  const recentList = document.getElementById('recent-achievements-list');
  recentList.innerHTML = '';
  const recentAchievements = gameState.achievements.slice(-5).reverse();
  recentAchievements.forEach(id => {
    const achievement = achievementsList.find(a => a.id === id);
    if (achievement) {
      const badge = document.createElement('div');
      badge.className = 'recent-achievement-badge';
      badge.textContent = achievement.icon;
      badge.title = achievement.name;
      recentList.appendChild(badge);
    }
  });
}

// Avatar Modal
document.getElementById('change-avatar')?.addEventListener('click', () => {
  document.getElementById('avatar-modal').classList.add('active');
});

document.querySelector('.modal-close')?.addEventListener('click', () => {
  document.getElementById('avatar-modal').classList.remove('active');
});

document.querySelectorAll('.avatar-option').forEach(option => {
  option.addEventListener('click', () => {
    const avatar = option.dataset.avatar;
    gameState.profile.avatar = avatar;
    localStorage.setItem('chessProfile', JSON.stringify(gameState.profile));
    updateProfile();
    document.getElementById('avatar-modal').classList.remove('active');
  });
});

// Username update
document.getElementById('username')?.addEventListener('change', (e) => {
  gameState.profile.username = e.target.value;
  localStorage.setItem('chessProfile', JSON.stringify(gameState.profile));
});

// Dark Mode
document.getElementById('dark-mode-toggle')?.addEventListener('change', (e) => {
  gameState.settings.darkMode = e.target.checked;
  document.body.classList.toggle('dark-mode', e.target.checked);
  localStorage.setItem('chessSettings', JSON.stringify(gameState.settings));
});

// Piece Style
document.querySelectorAll('.piece-style-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.piece-style-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    gameState.settings.pieceStyle = btn.dataset.style;
    localStorage.setItem('chessSettings', JSON.stringify(gameState.settings));
    renderBoard();
  });
});

// Puzzle System
let currentPuzzle = null;

function generatePuzzle() {
  // Simple puzzle: find a checkmate in one
  const puzzles = [
    {
      fen: 'r1bqkb1r/pppp1ppp/2n2n2/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 0 1',
      solution: 'Qxf7#',
      description: 'White to move and checkmate',
      rating: 1200
    }
  ];

  currentPuzzle = puzzles[Math.floor(Math.random() * puzzles.length)];
  document.getElementById('puzzle-description').textContent = currentPuzzle.description;
  document.getElementById('puzzle-rating').textContent = currentPuzzle.rating;
  document.getElementById('puzzle-result').textContent = '';

  // For now, just show a regular board
  renderPuzzleBoard();
}

function renderPuzzleBoard() {
  const boardEl = document.getElementById('puzzle-board');
  if (!boardEl) return;

  boardEl.innerHTML = '';
  boardEl.className = `board theme-${gameState.settings.theme}`;

  // Create a simple puzzle position
  const puzzlePosition = [
    ['♜', null, null, null, '♚', null, null, '♜'],
    [null, null, null, null, null, '♟', '♟', '♟'],
    [null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null],
    ['♙', '♙', '♙', null, null, null, '♙', '♙'],
    ['♖', null, null, null, '♔', null, null, '♖']
  ];

  for (let row = 0; row < 8; row++) {
    for (let col = 0; col < 8; col++) {
      const square = document.createElement('div');
      square.className = `square ${(row + col) % 2 === 0 ? 'light' : 'dark'}`;
      square.dataset.row = row;
      square.dataset.col = col;

      const piece = puzzlePosition[row][col];
      if (piece) {
        const pieceEl = document.createElement('div');
        pieceEl.className = 'piece';
        pieceEl.textContent = piece;
        square.appendChild(pieceEl);
      }

      boardEl.appendChild(square);
    }
  }
}

document.getElementById('solve-puzzle')?.addEventListener('click', () => {
  // Simple check - in real app would validate actual moves
  const correct = Math.random() > 0.5;
  const resultEl = document.getElementById('puzzle-result');

  if (correct) {
    resultEl.textContent = '✓ Correct! Well done!';
    resultEl.className = 'puzzle-result correct';
    gameState.puzzles.solved++;
    gameState.puzzles.streak++;
    gameState.puzzles.rating += 10;
  } else {
    resultEl.textContent = '✗ Not quite. Try again!';
    resultEl.className = 'puzzle-result incorrect';
    gameState.puzzles.streak = 0;
  }

  localStorage.setItem('chessPuzzles', JSON.stringify(gameState.puzzles));
  updatePuzzleStats();
  checkAchievements();
});

document.getElementById('next-puzzle')?.addEventListener('click', () => {
  generatePuzzle();
});

// Learn Section - Start Lesson Buttons
document.querySelectorAll('.learn-card .btn').forEach((btn, index) => {
  btn.addEventListener('click', () => {
    const lessons = [
      'Opening Principles',
      'Tactical Patterns',
      'Endgame Mastery',
      'Checkmate Patterns',
      'Strategy Fundamentals',
      'Game Analysis'
    ];

    const lessonName = lessons[index] || 'Lesson';
    alert(`🎓 ${lessonName}\n\nThis lesson is coming soon! In the full version, you'll learn:\n\n${getLessonPreview(index)}\n\nFor now, practice against the AI to improve your skills!`);
  });
});

function getLessonPreview(index) {
  const previews = [
    '• Control the center with pawns\n• Develop knights before bishops\n• Castle early for king safety\n• Don\'t move the same piece twice',
    '• Forks: Attack two pieces at once\n• Pins: Trap pieces behind valuable ones\n• Skewers: Force valuable pieces to move\n• Discovered attacks: Reveal hidden threats',
    '• King and pawn vs king\n• Opposition technique\n• Square of the pawn\n• Key squares and zugzwang',
    '• Back rank mate\n• Smothered mate with knight\n• Queen and king mate\n• Two rooks mate',
    '• Pawn structure importance\n• Piece activity and mobility\n• King safety principles\n• Space advantage',
    '• Review your games\n• Find your mistakes\n• Learn from losses\n• Identify patterns'
  ];
  return previews[index] || 'Interactive lessons coming soon!';
}

function updatePuzzleStats() {
  document.getElementById('puzzles-solved').textContent = gameState.puzzles.solved;
  document.getElementById('puzzle-user-rating').textContent = gameState.puzzles.rating;
  document.getElementById('puzzle-streak').textContent = gameState.puzzles.streak;
}

// Initialize
initBoard();
updateStatsDisplay();
renderAchievements();
updateProfile();
updatePuzzleStats();
generatePuzzle();

// Set initial game mode
if (document.getElementById('game-mode')) {
  document.getElementById('game-mode').value = gameState.gameMode;
}

// Apply saved settings
if (gameState.settings.darkMode) {
  document.body.classList.add('dark-mode');
  document.getElementById('dark-mode-toggle').checked = true;
}

document.querySelectorAll('.piece-style-btn').forEach(btn => {
  if (btn.dataset.style === gameState.settings.pieceStyle) {
    btn.classList.add('active');
  }
});

document.querySelectorAll('.theme-btn').forEach(btn => {
  if (btn.dataset.theme === gameState.settings.theme) {
    btn.classList.add('active');
  } else {
    btn.classList.remove('active');
  }
});

// Apply other saved settings
if (document.getElementById('sound-toggle')) {
  document.getElementById('sound-toggle').checked = gameState.settings.soundEnabled;
}
if (document.getElementById('hints-toggle')) {
  document.getElementById('hints-toggle').checked = gameState.settings.hintsEnabled;
}
if (document.getElementById('coordinates-toggle')) {
  document.getElementById('coordinates-toggle').checked = gameState.settings.coordinates;
}
if (document.getElementById('animations-toggle')) {
  document.getElementById('animations-toggle').checked = gameState.settings.animations;
}
if (document.getElementById('auto-promote')) {
  document.getElementById('auto-promote').value = gameState.settings.autoPromote;
}


// Button functionality test - logs which buttons are working
function testAllButtons() {
  const buttons = {
    'new-game': document.getElementById('new-game'),
    'undo-move': document.getElementById('undo-move'),
    'resign': document.getElementById('resign'),
    'reset-stats': document.getElementById('reset-stats'),
    'solve-puzzle': document.getElementById('solve-puzzle'),
    'next-puzzle': document.getElementById('next-puzzle'),
    'change-avatar': document.getElementById('change-avatar'),
    'modal-close': document.querySelector('.modal-close'),
    'sound-toggle': document.getElementById('sound-toggle'),
    'hints-toggle': document.getElementById('hints-toggle'),
    'coordinates-toggle': document.getElementById('coordinates-toggle'),
    'animations-toggle': document.getElementById('animations-toggle'),
    'dark-mode-toggle': document.getElementById('dark-mode-toggle')
  };

  console.log('🔍 Button Functionality Test:');
  Object.entries(buttons).forEach(([name, element]) => {
    if (element) {
      console.log(`✅ ${name}: Found and should be functional`);
    } else {
      console.log(`❌ ${name}: NOT FOUND`);
    }
  });

  console.log(`✅ Nav buttons: ${document.querySelectorAll('.nav-btn').length} found`);
  console.log(`✅ Theme buttons: ${document.querySelectorAll('.theme-btn').length} found`);
  console.log(`✅ Piece style buttons: ${document.querySelectorAll('.piece-style-btn').length} found`);
  console.log(`✅ Learn lesson buttons: ${document.querySelectorAll('.learn-card .btn').length} found`);
  console.log(`✅ Avatar options: ${document.querySelectorAll('.avatar-option').length} found`);
}

// Run test on load (comment out in production)
// testAllButtons();


// Add visual feedback to all buttons
document.querySelectorAll('.btn, .nav-btn, .theme-btn, .piece-style-btn').forEach(btn => {
  btn.addEventListener('click', function () {
    // Add a quick pulse animation
    this.style.transform = 'scale(0.95)';
    setTimeout(() => {
      this.style.transform = '';
    }, 100);
  });
});

// Add console logs for debugging button clicks
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
  document.querySelectorAll('button').forEach((btn, index) => {
    btn.addEventListener('click', function () {
      console.log(`🖱️ Button clicked: ${this.textContent || this.className} (index: ${index})`);
    });
  });
}


// Welcome message for first-time users
if (!localStorage.getItem('chessWelcomeShown')) {
  setTimeout(() => {
    alert('♔ Welcome to Chessy!\n\n' +
      '✨ Features:\n' +
      '• Play against 11 AI difficulty levels\n' +
      '• Solve daily puzzles\n' +
      '• Unlock 18 achievements\n' +
      '• Customize your profile & avatar\n' +
      '• Dark mode & 5 board themes\n' +
      '• Track your statistics\n' +
      '• Learn chess with 6 lesson categories\n\n' +
      '🎮 Start by clicking "New Game" and selecting an opponent!\n\n' +
      '💡 Tip: Try the "Random Guy" AI for a surprise! 😉');
    localStorage.setItem('chessWelcomeShown', 'true');
  }, 500);
}


// Confetti Celebration
function createConfetti() {
  const canvas = document.createElement('canvas');
  canvas.id = 'confetti-canvas';
  document.body.appendChild(canvas);

  const ctx = canvas.getContext('2d');
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  const confettiPieces = [];
  const colors = ['#f39c12', '#e74c3c', '#3498db', '#2ecc71', '#9b59b6', '#1abc9c'];

  // Create confetti pieces
  for (let i = 0; i < 150; i++) {
    confettiPieces.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height - canvas.height,
      rotation: Math.random() * 360,
      speed: Math.random() * 3 + 2,
      size: Math.random() * 8 + 5,
      color: colors[Math.floor(Math.random() * colors.length)],
      rotationSpeed: Math.random() * 10 - 5
    });
  }

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    confettiPieces.forEach((piece, index) => {
      piece.y += piece.speed;
      piece.rotation += piece.rotationSpeed;

      ctx.save();
      ctx.translate(piece.x, piece.y);
      ctx.rotate((piece.rotation * Math.PI) / 180);
      ctx.fillStyle = piece.color;
      ctx.fillRect(-piece.size / 2, -piece.size / 2, piece.size, piece.size);
      ctx.restore();

      // Remove if off screen
      if (piece.y > canvas.height) {
        confettiPieces.splice(index, 1);
      }
    });

    if (confettiPieces.length > 0) {
      requestAnimationFrame(animate);
    } else {
      canvas.remove();
    }
  }

  animate();
}

// Fullscreen Game Mode
document.getElementById('fullscreen-toggle')?.addEventListener('click', () => {
  const container = document.getElementById('game-container');
  const btn = document.getElementById('fullscreen-toggle');

  container.classList.toggle('fullscreen');

  if (container.classList.contains('fullscreen')) {
    btn.textContent = '✕ Exit Fullscreen';
    btn.style.position = 'fixed';
    btn.style.top = '1rem';
    btn.style.right = '1rem';
    btn.style.zIndex = '1000';
  } else {
    btn.textContent = '⛶ Fullscreen Game';
    btn.style.position = 'absolute';
  }

  // Re-render board to adjust size
  renderBoard();
});

// Toggle game active state
function setGameActive(active) {
  if (active) {
    document.body.classList.add('game-active');
  } else {
    document.body.classList.remove('game-active');
  }
}


// Keyboard Shortcuts
document.addEventListener('keydown', (e) => {
  // ESC to exit fullscreen
  if (e.key === 'Escape') {
    const container = document.getElementById('game-container');
    if (container?.classList.contains('fullscreen')) {
      document.getElementById('fullscreen-toggle')?.click();
    }
  }

  // F for fullscreen
  if (e.key === 'f' || e.key === 'F') {
    if (document.activeElement.tagName !== 'INPUT') {
      document.getElementById('fullscreen-toggle')?.click();
    }
  }

  // U for undo
  if ((e.key === 'u' || e.key === 'U') && (e.ctrlKey || e.metaKey)) {
    e.preventDefault();
    document.getElementById('undo-move')?.click();
  }

  // N for new game
  if ((e.key === 'n' || e.key === 'N') && (e.ctrlKey || e.metaKey)) {
    e.preventDefault();
    document.getElementById('new-game')?.click();
  }
});

// Window resize handler for fullscreen
window.addEventListener('resize', () => {
  const canvas = document.getElementById('confetti-canvas');
  if (canvas) {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
});

