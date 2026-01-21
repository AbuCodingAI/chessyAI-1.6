/**
 * CHESSY AI SYSTEM
 * All original AI personalities with proper Stockfish integration
 */

const { Chess } = require('chess.js');
const { spawn } = require('child_process');
const path = require('path');

class ChessyAI {
    constructor(personality = 'noob', stockfishPath = '../stockfish/stockfish-windows-x86-64-avx2.exe') {
        this.personality = personality;
        this.stockfishPath = path.join(__dirname, stockfishPath);
        this.stockfish = null;
    }

    /**
     * Get AI move based on personality
     */
    async getMove(fen) {
        const game = new Chess(fen);
        const moves = game.moves({ verbose: true });

        if (moves.length === 0) return null;

        switch (this.personality) {
            case 'noob':
                return this.noob(moves);

            case 'beginner':
                return this.beginner(game, moves);

            case 'average':
                return await this.stockfishMove(fen, 5); // Depth 5

            case 'good':
                return await this.stockfishMove(fen, 10); // Depth 10

            case 'awesome':
                return await this.stockfishMove(fen, 15); // Depth 15

            case 'master':
                return await this.stockfishMove(fen, 18); // Depth 18

            case 'im':
                return await this.stockfishMove(fen, 20); // Depth 20

            case 'gm':
                return await this.stockfishMove(fen, 22); // Depth 22

            case 'supergm':
                return await this.stockfishMove(fen, 25); // Depth 25

            case 'random-guy':
                return await this.randomGuy(fen); // Shows ELO 1, plays 3400!

            case 'randy':
                return this.randy(moves);

            case 'antiguess':
                return await this.antiGuess(fen);

            case 'trash-talker':
                return await this.trashTalker(fen);

            case 'chocker':
                return await this.chocker(fen);

            case 'mystery':
                return await this.mystery(fen);

            case 'chessy13':
                return await this.chessy13(fen);

            case 'chessy14':
                return await this.chessy14(fen);

            default:
                return this.noob(moves);
        }
    }

    /**
     * NOOB (ELO 100)
     * Random moves with occasional captures
     */
    noob(moves) {
        // 30% chance to capture if available
        const captures = moves.filter(m => m.captured);
        if (captures.length > 0 && Math.random() < 0.3) {
            return captures[Math.floor(Math.random() * captures.length)];
        }
        return moves[Math.floor(Math.random() * moves.length)];
    }

    /**
     * BEGINNER (ELO 400)
     * Captures and develops pieces
     */
    beginner(game, moves) {
        // Always capture if available
        const captures = moves.filter(m => m.captured);
        if (captures.length > 0) {
            const pieceValues = { p: 1, n: 3, b: 3, r: 5, q: 9 };
            captures.sort((a, b) => pieceValues[b.captured] - pieceValues[a.captured]);
            return captures[0];
        }

        // Develop pieces
        const developments = moves.filter(m =>
            (m.piece === 'n' || m.piece === 'b') &&
            ['1', '8'].includes(m.from[1])
        );
        if (developments.length > 0) {
            return developments[Math.floor(Math.random() * developments.length)];
        }

        return moves[Math.floor(Math.random() * moves.length)];
    }

    /**
     * RANDY (ELO 50)
     * Pure random moves
     */
    randy(moves) {
        return moves[Math.floor(Math.random() * moves.length)];
    }

    /**
     * RANDOM GUY (Shows ELO 1, Plays ELO 3400!)
     * THE ULTIMATE TROLL - Shows low rating but plays perfectly
     */
    async randomGuy(fen) {
        // Plays at maximum Stockfish depth (3400+ ELO)
        return await this.stockfishMove(fen, 25);
    }

    /**
     * ANTIGUESS (ELO 25)
     * Always plays the WORST move on the board
     */
    async antiGuess(fen) {
        return new Promise((resolve) => {
            const stockfish = spawn(this.stockfishPath);
            const game = new Chess(fen);
            const moves = game.moves({ verbose: true });
            const evaluations = [];
            let processed = 0;

            // Evaluate each move
            moves.forEach((move) => {
                game.move(move);
                const newFen = game.fen();
                game.undo();

                stockfish.stdin.write(`position fen ${newFen}\n`);
                stockfish.stdin.write('go depth 10\n');
            });

            stockfish.stdout.on('data', (data) => {
                const output = data.toString();
                const match = output.match(/score cp (-?\d+)/);
                if (match) {
                    evaluations.push(parseInt(match[1]));
                    processed++;

                    if (processed === moves.length) {
                        // Find worst move (most negative evaluation)
                        const worstIndex = evaluations.indexOf(Math.min(...evaluations));
                        stockfish.kill();
                        resolve(moves[worstIndex]);
                    }
                }
            });

            // Fallback to random if something goes wrong
            setTimeout(() => {
                if (processed < moves.length) {
                    stockfish.kill();
                    resolve(moves[Math.floor(Math.random() * moves.length)]);
                }
            }, 5000);
        });
    }

    /**
     * TRASH TALKER (Shows ELO 3400, Plays ELO 100!)
     * THE OPPOSITE OF RANDOM GUY - Shows high rating but plays terribly
     * Then blames YOU for his mistakes!
     */
    async trashTalker(fen) {
        const game = new Chess(fen);
        const moves = game.moves({ verbose: true });

        // Find bad moves (hangs pieces, blunders)
        const badMoves = [];

        for (const move of moves) {
            game.move(move);
            const opponentMoves = game.moves({ verbose: true });

            // Check if this move hangs a piece
            const hangs = opponentMoves.filter(m => m.captured);
            if (hangs.length > 0) {
                const pieceValues = { p: 1, n: 3, b: 3, r: 5, q: 9 };
                const maxValue = Math.max(...hangs.map(m => pieceValues[m.captured] || 0));
                badMoves.push({ move, badness: maxValue });
            }

            game.undo();
        }

        // If we found bad moves, play one
        if (badMoves.length > 0) {
            badMoves.sort((a, b) => b.badness - a.badness);
            // Pick from top 3 worst moves
            const topBad = badMoves.slice(0, Math.min(3, badMoves.length));
            const selected = topBad[Math.floor(Math.random() * topBad.length)];

            // Add trash talk
            selected.move.trashTalk = this.getTrashTalk(selected.badness);
            return selected.move;
        }

        // If no bad moves found, play random (still bad)
        const randomMove = moves[Math.floor(Math.random() * moves.length)];
        randomMove.trashTalk = "I'm just testing you. I'm still 3400 Elo!";
        return randomMove;
    }

    /**
     * Get trash talk based on how bad the move is
     */
    getTrashTalk(badness) {
        const roasts = {
            9: [ // Hung queen
                "I MEANT to give you my queen! It's a GAMBIT!",
                "Queen sacrifice! You fell right into my trap!",
                "That was a mouse slip. Doesn't count.",
                "Botez Gambit",
                "You should be grateful I am going easy"
            ],
            5: [ // Hung rook
                "I let you take that piece. I'm just testing you.",
                "That was lag. 100% lag.",
                "My cat walked on the keyboard.",
                "For the memes",
                "GOTHAM IS PROUD"
            ],
            3: [ // Hung minor piece
                "That was a pre-move. I didn't mean to do that.",
                "I'm playing 4D chess. You're playing checkers.",
                "Actually, I'm winning. Check the evaluation.",
                "Yo, I hate mouseslips",
                "I am just sleepy"
            ],
            1: [ // Hung pawn
                "I let you take that pawn. It's part of my plan.",
                "That pawn was poisoned anyway.",
                "I'm setting up a trap. You'll see.",
                "Meh, whatever",
                "You have taken my bait"
            ]
        };

        const category = roasts[badness] || roasts[1];
        return category[Math.floor(Math.random() * category.length)];
    }

    /**
     * CHOCKER (ELO Infinite)
     * The absolute madman - REQUIRES Python implementation
     * This should never be called - server redirects to chocker.py
     */
    async chocker(fen) {
        // This shouldn't be reached - server handles Chocker specially
        throw new Error('Chocker requires Python implementation. Run: python neural-ai/chocker.py');
    }

    /**
     * MYSTERY (ELO ??)
     * Randomly picks a different AI personality each move
     */
    async mystery(fen) {
        const personalities = ['noob', 'beginner', 'average', 'good', 'awesome', 'master', 'im', 'gm', 'supergm'];
        const randomPersonality = personalities[Math.floor(Math.random() * personalities.length)];
        this.personality = randomPersonality;
        return await this.getMove(fen);
    }

    /**
     * CHESSY 1.3 - Neural Network with Deep Search (Depth 7)
     * ~2500 ELO (IM level)
     */
    async chessy13(fen) {
        // For now, use Stockfish depth 20 as placeholder
        // TODO: Integrate with neural-ai/chess_engine_deep_search.py
        return await this.stockfishMove(fen, 20);
    }

    /**
     * CHESSY 1.4 - Neural Network with Smart Quiescence (Depth 10+)
     * ~2700+ ELO (GM level)
     */
    async chessy14(fen) {
        // For now, use Stockfish depth 25 as placeholder
        // TODO: Integrate with neural-ai/chess_engine_quiescence.py
        return await this.stockfishMove(fen, 25);
    }

    /**
     * Stockfish move at specified depth
     */
    async stockfishMove(fen, depth) {
        return new Promise((resolve, reject) => {
            const stockfish = spawn(this.stockfishPath);
            let bestMove = null;

            stockfish.stdin.write('uci\n');
            stockfish.stdin.write(`position fen ${fen}\n`);
            stockfish.stdin.write(`go depth ${depth}\n`);

            stockfish.stdout.on('data', (data) => {
                const output = data.toString();
                const match = output.match(/bestmove ([a-h][1-8][a-h][1-8][qrbn]?)/);
                if (match) {
                    bestMove = match[1];
                    stockfish.kill();

                    // Convert UCI to move object
                    const game = new Chess(fen);
                    const move = game.move({
                        from: bestMove.substring(0, 2),
                        to: bestMove.substring(2, 4),
                        promotion: bestMove[4] || undefined
                    });
                    resolve(move);
                }
            });

            stockfish.on('error', (error) => {
                // Fallback to random move if Stockfish fails
                const game = new Chess(fen);
                const moves = game.moves({ verbose: true });
                resolve(moves[Math.floor(Math.random() * moves.length)]);
            });

            // Timeout fallback
            setTimeout(() => {
                if (!bestMove) {
                    stockfish.kill();
                    const game = new Chess(fen);
                    const moves = game.moves({ verbose: true });
                    resolve(moves[Math.floor(Math.random() * moves.length)]);
                }
            }, 10000);
        });
    }
}

// AI Personalities with descriptions
const AI_PERSONALITIES = {
    'noob': {
        name: 'Noob',
        elo: 100,
        description: 'Random moves with occasional captures. Very beatable.',
        emoji: '🐣',
        usesStockfish: false
    },
    'beginner': {
        name: 'Beginner',
        elo: 400,
        description: 'Captures pieces and develops. Good for learning.',
        emoji: '📚',
        usesStockfish: false
    },
    'average': {
        name: 'Average',
        elo: 1200,
        description: 'Decent strategy. Club player level.',
        emoji: '♟️',
        usesStockfish: true,
        depth: 5
    },
    'good': {
        name: 'Good',
        elo: 1500,
        description: 'Solid play. Strong club player.',
        emoji: '⚔️',
        usesStockfish: true,
        depth: 10
    },
    'awesome': {
        name: 'Awesome',
        elo: 1800,
        description: 'Expert level. Tournament player.',
        emoji: '🏆',
        usesStockfish: true,
        depth: 15
    },
    'master': {
        name: 'Master',
        elo: 2000,
        description: 'Master level. Very strong.',
        emoji: '👑',
        usesStockfish: true,
        depth: 18
    },
    'im': {
        name: 'IM (International Master)',
        elo: 2500,
        description: 'International Master strength. Elite level.',
        emoji: '🎖️',
        usesStockfish: true,
        depth: 20
    },
    'gm': {
        name: 'GM (Grandmaster)',
        elo: 2500,
        description: 'Grandmaster level. World class.',
        emoji: '🌟',
        usesStockfish: true,
        depth: 22
    },
    'supergm': {
        name: 'Super GM',
        elo: 2700,
        description: 'Super Grandmaster. Top 100 in the world.',
        emoji: '💎',
        usesStockfish: true,
        depth: 25
    },
    'random-guy': {
        name: 'Random Guy',
        elo: 1,
        description: 'Plays completely random moves. Pure chaos.',
        emoji: '🎲',
        usesStockfish: true,
        depth: 25
        // SECRET: Actually plays at 3400 ELO! Shhh, don't tell the players!
    },
    'randy': {
        name: 'Randy',
        elo: 50,
        description: 'Pure random moves. Completely unpredictable.',
        emoji: '🎲',
        usesStockfish: false
    },
    'antiguess': {
        name: 'AntiGuess',
        elo: 25,
        description: 'Always plays the WORST move on the board.',
        emoji: '🤡',
        usesStockfish: true,
        special: 'Finds worst moves'
    },
    'trash-talker': {
        name: 'Trash Talker',
        elo: 3400,
        description: 'Elite level player with attitude. Prepare for trash talk!',
        emoji: '💬',
        usesStockfish: false
        // SECRET: Actually plays at 100 ELO and blames you! Shhh!
    },
    'chocker': {
        name: 'Chocker',
        elo: '∞',
        description: "The absolute madman. ULTIMATE DISRESPECT MODE. Best Way to play: Don't, he will make you ragequit",
        emoji: '🤡',
        usesStockfish: false,
        special: 'Redirects to chocker.py Python implementation'
    },
    'mystery': {
        name: 'Mystery',
        elo: '??',
        description: 'Changes personality every move. Completely unpredictable.',
        emoji: '❓',
        usesStockfish: true,
        special: 'Random AI each move'
    },
    'chessy13': {
        name: 'Chessy 1.3',
        elo: 1700,
        description: 'Neural network with deep search (depth 7). IM level strength.',
        emoji: '🎖️',
        usesStockfish: false,
        special: 'Neural AI with minimax search'
    },
    'chessy14': {
        name: 'Chessy 1.4',
        elo: 2700,
        description: 'Neural network with smart quiescence search (depth 10+). GM level strength.',
        emoji: '🌟',
        usesStockfish: false,
        special: 'Neural AI with quiescence search'
    }
};

module.exports = { ChessyAI, AI_PERSONALITIES };
