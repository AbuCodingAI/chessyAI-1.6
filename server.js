/**
 * CHESSYCOM SERVER
 * Local multiplayer chess server
 */

const express = require('express');
const http = require('http');
const socketIO = require('socket.io');
const path = require('path');
const { Chess } = require('chess.js');
const { ChessyAI, AI_PERSONALITIES } = require('./simple-ai.js');

const app = express();
const server = http.createServer(app);
const io = socketIO(server, {
    cors: {
        origin: "*",
        methods: ["GET", "POST"]
    }
});

// Serve static files with proper MIME types
app.use(express.static(__dirname, {
    setHeaders: (res, path) => {
        if (path.endsWith('.js')) {
            res.setHeader('Content-Type', 'application/javascript');
        } else if (path.endsWith('.css')) {
            res.setHeader('Content-Type', 'text/css');
        }
    }
}));
app.use(express.json());

// Serve index.html for root route
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({
        status: 'ok',
        timestamp: new Date().toISOString(),
        environment: process.env.NODE_ENV || 'development',
        rooms: rooms.size
    });
});

// Debug endpoint to check static files
app.get('/debug', (req, res) => {
    const fs = require('fs');
    const files = {
        'index.html': fs.existsSync(path.join(__dirname, 'index.html')),
        'style.css': fs.existsSync(path.join(__dirname, 'style.css')),
        'script.js': fs.existsSync(path.join(__dirname, 'script.js')),
        'simple-ai.js': fs.existsSync(path.join(__dirname, 'simple-ai.js'))
    };
    res.json({
        status: 'debug',
        files,
        __dirname,
        cwd: process.cwd()
    });
});

// Test page route
app.get('/test', (req, res) => {
    res.sendFile(path.join(__dirname, 'test-render.html'));
});

// Game rooms storage
const rooms = new Map();

// Generate random room code
function generateRoomCode() {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let code = '';
    for (let i = 0; i < 6; i++) {
        code += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return code;
}

// Socket.io connection handling
io.on('connection', (socket) => {
    console.log('🎮 Player connected:', socket.id);

    // Create new game room
    socket.on('create-room', (playerName) => {
        const roomCode = generateRoomCode();
        const room = {
            code: roomCode,
            players: [{
                id: socket.id,
                name: playerName || 'Player 1',
                color: 'white'
            }],
            game: new Chess(),
            spectators: [],
            createdAt: Date.now()
        };

        rooms.set(roomCode, room);
        socket.join(roomCode);

        console.log(`🏰 Room created: ${roomCode}`);
        socket.emit('room-created', {
            roomCode,
            color: 'white',
            fen: room.game.fen()
        });
    });

    // Join existing room
    socket.on('join-room', ({ roomCode, playerName }) => {
        const room = rooms.get(roomCode);

        if (!room) {
            socket.emit('error', { message: 'Room not found' });
            return;
        }

        if (room.players.length >= 2) {
            // Join as spectator
            room.spectators.push({
                id: socket.id,
                name: playerName || 'Spectator'
            });
            socket.join(roomCode);
            socket.emit('joined-as-spectator', {
                roomCode,
                fen: room.game.fen()
            });
            console.log(`👁️ Spectator joined room: ${roomCode}`);
        } else {
            // Join as player
            room.players.push({
                id: socket.id,
                name: playerName || 'Player 2',
                color: 'black'
            });
            socket.join(roomCode);

            console.log(`🎮 Player joined room: ${roomCode}`);

            // Notify both players
            io.to(roomCode).emit('game-start', {
                white: room.players[0],
                black: room.players[1],
                fen: room.game.fen()
            });
        }
    });

    // Handle move
    socket.on('move', ({ roomCode, move }) => {
        const room = rooms.get(roomCode);

        if (!room) {
            socket.emit('error', { message: 'Room not found' });
            return;
        }

        // Validate it's the player's turn
        const player = room.players.find(p => p.id === socket.id);
        if (!player) {
            socket.emit('error', { message: 'You are not a player in this game' });
            return;
        }

        const currentTurn = room.game.turn() === 'w' ? 'white' : 'black';
        if (player.color !== currentTurn) {
            socket.emit('error', { message: 'Not your turn' });
            return;
        }

        // Make move
        try {
            const result = room.game.move(move);
            if (result) {
                // Broadcast move to all in room
                io.to(roomCode).emit('move-made', {
                    move: result,
                    fen: room.game.fen(),
                    turn: room.game.turn(),
                    isCheck: room.game.isCheck(),
                    isCheckmate: room.game.isCheckmate(),
                    isStalemate: room.game.isStalemate(),
                    isDraw: room.game.isDraw()
                });

                console.log(`♟️ Move in ${roomCode}: ${result.san}`);

                // Check game over
                if (room.game.isGameOver()) {
                    let result = 'draw';
                    if (room.game.isCheckmate()) {
                        result = room.game.turn() === 'w' ? 'black-wins' : 'white-wins';
                    }
                    io.to(roomCode).emit('game-over', { result });
                    console.log(`🏁 Game over in ${roomCode}: ${result}`);
                }
            }
        } catch (error) {
            socket.emit('error', { message: 'Invalid move' });
        }
    });

    // Chat message
    socket.on('chat-message', ({ roomCode, message }) => {
        const room = rooms.get(roomCode);
        if (room) {
            const player = room.players.find(p => p.id === socket.id) ||
                room.spectators.find(s => s.id === socket.id);
            if (player) {
                io.to(roomCode).emit('chat-message', {
                    sender: player.name,
                    message,
                    timestamp: Date.now()
                });
            }
        }
    });

    // Get room list
    socket.on('get-rooms', () => {
        const roomList = Array.from(rooms.values()).map(room => ({
            code: room.code,
            players: room.players.length,
            spectators: room.spectators.length,
            createdAt: room.createdAt
        }));
        socket.emit('room-list', roomList);
    });

    // Disconnect
    socket.on('disconnect', () => {
        console.log('👋 Player disconnected:', socket.id);

        // Remove player from rooms
        rooms.forEach((room, code) => {
            const playerIndex = room.players.findIndex(p => p.id === socket.id);
            if (playerIndex !== -1) {
                room.players.splice(playerIndex, 1);
                io.to(code).emit('player-disconnected', {
                    message: 'Opponent disconnected'
                });

                // Delete room if empty
                if (room.players.length === 0) {
                    rooms.delete(code);
                    console.log(`🗑️ Room deleted: ${code}`);
                }
            }

            // Remove spectator
            const spectatorIndex = room.spectators.findIndex(s => s.id === socket.id);
            if (spectatorIndex !== -1) {
                room.spectators.splice(spectatorIndex, 1);
            }
        });
    });
});


// Start server
const PORT = process.env.PORT || 3000;
const HOST = process.env.HOST || '0.0.0.0';

server.listen(PORT, HOST, () => {
    console.log('🏰 ChessyCom Server Started!');
    console.log(`📡 Server running on http://localhost:${PORT}`);
    console.log(`🎮 Open http://localhost:${PORT} in your browser`);
    console.log(`🌍 Environment: ${process.env.NODE_ENV || 'development'}`);
    console.log('');
    if (process.env.NODE_ENV !== 'production') {
        console.log('🌐 To play with friends on same network:');
        console.log(`   1. Find your local IP (ipconfig on Windows)`);
        console.log(`   2. Share: http://YOUR_IP:${PORT}`);
        console.log('');
    }
});

// Cleanup old rooms (every 1 hour)
const oneHour = 60 * 60 * 1000;
setInterval(() => {
    const now = Date.now();

    rooms.forEach((room, code) => {
        if (now - room.createdAt > oneHour && room.players.length === 0) {
            rooms.delete(code);
            console.log(`🗑️ Cleaned up old room: ${code}`);
        }
    });
}, oneHour);


// API endpoint for AI moves
app.post('/api/ai-move', async (req, res) => {
    const { fen, personality } = req.body;

    try {
        // Special handling for Chocker - redirect to Python implementation
        if (personality === 'chocker') {
            return res.json({
                redirect: 'chocker',
                message: 'Chocker requires the Python implementation. Run: python neural-ai/chocker.py',
                launchCommand: 'cd neural-ai && python chocker.py'
            });
        }

        const ai = new ChessyAI(personality || 'noob');
        const move = await ai.getMove(fen);

        if (move) {
            res.json({
                move,
                personality: AI_PERSONALITIES[personality] || AI_PERSONALITIES['noob']
            });
        } else {
            res.status(400).json({ error: 'No legal moves available' });
        }
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Get list of AI personalities
app.get('/api/ai-personalities', (req, res) => {
    res.json(AI_PERSONALITIES);
});

console.log('');
console.log('🤖 AI Personalities Available:');
Object.entries(AI_PERSONALITIES).forEach(([key, ai]) => {
    console.log(`   ${ai.emoji} ${ai.name} (ELO ${ai.elo})`);
});
