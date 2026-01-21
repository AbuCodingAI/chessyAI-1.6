/**
 * PUZZLE ENGINE
 * Tactical chess puzzles for training
 */

// Puzzle Database - 20 starter puzzles
const PUZZLE_DATABASE = [
    // FORKS
    {
        id: "puzzle_001",
        fen: "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4",
        theme: "Fork",
        difficulty: 800,
        solution: ["Nxe5"],
        description: "White to move. Win material with a knight fork.",
        hint: "Look for a knight move that attacks two pieces at once."
    },
    {
        id: "puzzle_002",
        fen: "r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/3P1N2/PPP2PPP/RNBQK2R w KQkq - 0 5",
        theme: "Fork",
        difficulty: 850,
        solution: ["Nxe5"],
        description: "White to move. Fork the king and bishop.",
        hint: "The knight can attack the king and another piece."
    },

    // PINS
    {
        id: "puzzle_003",
        fen: "r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/3P1N2/PPP2PPP/RNBQK2R w KQkq - 0 5",
        theme: "Pin",
        difficulty: 900,
        solution: ["Bxf7+"],
        description: "White to move. Win material with a pin.",
        hint: "The black king and knight are on the same diagonal."
    },
    {
        id: "puzzle_004",
        fen: "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 3 3",
        theme: "Pin",
        difficulty: 950,
        solution: ["Nf6"],
        description: "Black to move. Develop with a pin.",
        hint: "Pin the white knight to the king."
    },

    // SKEWERS
    {
        id: "puzzle_005",
        fen: "6k1/5ppp/8/8/8/8/5PPP/4R1K1 w - - 0 1",
        theme: "Skewer",
        difficulty: 1000,
        solution: ["Re8+"],
        description: "White to move. Win the rook with a skewer.",
        hint: "Check the king, then capture the rook."
    },
    {
        id: "puzzle_006",
        fen: "r5k1/5ppp/8/8/8/8/5PPP/4R1K1 w - - 0 1",
        theme: "Skewer",
        difficulty: 1050,
        solution: ["Re8+"],
        description: "White to move. Skewer king and rook.",
        hint: "Force the king to move, then take the rook."
    },

    // DISCOVERED ATTACKS
    {
        id: "puzzle_007",
        fen: "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQ1RK1 w kq - 0 5",
        theme: "Discovered Attack",
        difficulty: 1100,
        solution: ["Nxe5"],
        description: "White to move. Win material with discovered attack.",
        hint: "Move the knight to reveal an attack on the queen."
    },
    {
        id: "puzzle_008",
        fen: "r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/3P1N2/PPP2PPP/RNBQK2R w KQkq - 0 5",
        theme: "Discovered Attack",
        difficulty: 1150,
        solution: ["d4"],
        description: "White to move. Open the center with discovered attack.",
        hint: "Push the pawn to attack the bishop and open lines."
    },

    // BACK RANK MATES
    {
        id: "puzzle_009",
        fen: "6k1/5ppp/8/8/8/8/5PPP/4R1K1 w - - 0 1",
        theme: "Back Rank Mate",
        difficulty: 1200,
        solution: ["Re8#"],
        description: "White to move and checkmate.",
        hint: "The black king has no escape squares on the back rank."
    },
    {
        id: "puzzle_010",
        fen: "r5k1/5ppp/8/8/8/8/5PPP/5RK1 w - - 0 1",
        theme: "Back Rank Mate",
        difficulty: 1250,
        solution: ["Rf8#"],
        description: "White to move and deliver checkmate.",
        hint: "Deliver mate on the back rank."
    },

    // SMOTHERED MATES
    {
        id: "puzzle_011",
        fen: "6rk/6pp/8/8/8/8/5N2/6K1 w - - 0 1",
        theme: "Smothered Mate",
        difficulty: 1300,
        solution: ["Nf7#"],
        description: "White to move and checkmate.",
        hint: "The king is trapped by its own pieces."
    },
    {
        id: "puzzle_012",
        fen: "r5rk/5ppp/8/8/8/8/5N2/6K1 w - - 0 1",
        theme: "Smothered Mate",
        difficulty: 1350,
        solution: ["Nf7#"],
        description: "White to move. Smothered mate!",
        hint: "Knight delivers mate when king is blocked by own pieces."
    },

    // QUEEN SACRIFICES
    {
        id: "puzzle_013",
        fen: "r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/3P1N2/PPPQ1PPP/RNB1K2R w KQkq - 0 5",
        theme: "Queen Sacrifice",
        difficulty: 1400,
        solution: ["Qxf7+"],
        description: "White to move. Sacrifice the queen for checkmate.",
        hint: "Sometimes the queen must be sacrificed for victory."
    },
    {
        id: "puzzle_014",
        fen: "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPPQPPP/RNB1K2R w KQkq - 0 5",
        theme: "Queen Sacrifice",
        difficulty: 1450,
        solution: ["Qxe5+"],
        description: "White to move. Win with a queen sacrifice.",
        hint: "Give up the queen to force checkmate."
    },

    // DOUBLE ATTACKS
    {
        id: "puzzle_015",
        fen: "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4",
        theme: "Double Attack",
        difficulty: 1100,
        solution: ["Nxe5"],
        description: "White to move. Attack two pieces at once.",
        hint: "One move can threaten multiple pieces."
    },
    {
        id: "puzzle_016",
        fen: "r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/3P1N2/PPP2PPP/RNBQK2R w KQkq - 0 5",
        theme: "Double Attack",
        difficulty: 1150,
        solution: ["Nxe5"],
        description: "White to move. Double attack wins material.",
        hint: "Attack two pieces simultaneously."
    },

    // INTERMEDIATE TACTICS
    {
        id: "puzzle_017",
        fen: "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4",
        theme: "Combination",
        difficulty: 1300,
        solution: ["Nxe5", "Nxe5", "d4"],
        description: "White to move. Win material with a combination.",
        hint: "Multiple moves work together to win material."
    },
    {
        id: "puzzle_018",
        fen: "r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/3P1N2/PPP2PPP/RNBQK2R w KQkq - 0 5",
        theme: "Combination",
        difficulty: 1350,
        solution: ["Bxf7+", "Kxf7", "Nxe5+"],
        description: "White to move. Combination wins material.",
        hint: "Sacrifice to expose the king, then win material."
    },

    // ADVANCED TACTICS
    {
        id: "puzzle_019",
        fen: "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4",
        theme: "Deflection",
        difficulty: 1400,
        solution: ["Nxe5"],
        description: "White to move. Deflect the defender.",
        hint: "Remove the piece defending a key square."
    },
    {
        id: "puzzle_020",
        fen: "r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/3P1N2/PPP2PPP/RNBQK2R w KQkq - 0 5",
        theme: "Removal of Defender",
        difficulty: 1450,
        solution: ["Bxf7+"],
        description: "White to move. Remove the key defender.",
        hint: "Eliminate the piece protecting the king."
    }
];

/**
 * Puzzle Engine Class
 */
class PuzzleEngine {
    constructor() {
        this.currentPuzzle = null;
        this.moveIndex = 0;
        this.attempts = 0;
        this.startTime = null;
    }

    /**
     * Load a puzzle by ID
     */
    loadPuzzle(puzzleId) {
        this.currentPuzzle = PUZZLE_DATABASE.find(p => p.id === puzzleId);
        this.moveIndex = 0;
        this.attempts = 0;
        this.startTime = Date.now();
        return this.currentPuzzle;
    }

    /**
     * Load a random puzzle
     */
    loadRandomPuzzle() {
        const randomIndex = Math.floor(Math.random() * PUZZLE_DATABASE.length);
        return this.loadPuzzle(PUZZLE_DATABASE[randomIndex].id);
    }

    /**
     * Load puzzle by difficulty range
     */
    loadPuzzleByDifficulty(minDifficulty, maxDifficulty) {
        const filtered = PUZZLE_DATABASE.filter(p =>
            p.difficulty >= minDifficulty && p.difficulty <= maxDifficulty
        );
        if (filtered.length === 0) return this.loadRandomPuzzle();

        const randomIndex = Math.floor(Math.random() * filtered.length);
        return this.loadPuzzle(filtered[randomIndex].id);
    }

    /**
     * Validate a move against the solution
     */
    validateMove(move) {
        if (!this.currentPuzzle) {
            return { correct: false, complete: false, message: "No puzzle loaded!" };
        }

        const expectedMove = this.currentPuzzle.solution[this.moveIndex];

        // Normalize move format (handle both "e4" and "e2e4" formats)
        const normalizedMove = this.normalizeMove(move);
        const normalizedExpected = this.normalizeMove(expectedMove);

        if (normalizedMove === normalizedExpected) {
            this.moveIndex++;
            const isComplete = this.moveIndex >= this.currentPuzzle.solution.length;

            return {
                correct: true,
                complete: isComplete,
                message: isComplete ? "🎉 Puzzle solved!" : "✓ Correct! Continue...",
                timeSpent: Math.floor((Date.now() - this.startTime) / 1000)
            };
        } else {
            this.attempts++;
            return {
                correct: false,
                complete: false,
                message: "❌ Not quite. Try again!",
                attempts: this.attempts
            };
        }
    }

    /**
     * Normalize move format
     */
    normalizeMove(move) {
        if (typeof move === 'string') {
            return move.toLowerCase().replace(/[+#]/g, '');
        }
        if (move && move.san) {
            return move.san.toLowerCase().replace(/[+#]/g, '');
        }
        return '';
    }

    /**
     * Get hint for current puzzle
     */
    getHint() {
        return this.currentPuzzle ? this.currentPuzzle.hint : "No puzzle loaded.";
    }

    /**
     * Show complete solution
     */
    showSolution() {
        if (!this.currentPuzzle) {
            return { moves: [], explanation: "No puzzle loaded." };
        }

        return {
            moves: this.currentPuzzle.solution,
            explanation: this.currentPuzzle.description,
            theme: this.currentPuzzle.theme
        };
    }

    /**
     * Get all puzzles by theme
     */
    getPuzzlesByTheme(theme) {
        return PUZZLE_DATABASE.filter(p => p.theme === theme);
    }

    /**
     * Get all available themes
     */
    getThemes() {
        const themes = [...new Set(PUZZLE_DATABASE.map(p => p.theme))];
        return themes.sort();
    }

    /**
     * Get puzzle statistics
     */
    getStats() {
        return {
            totalPuzzles: PUZZLE_DATABASE.length,
            themes: this.getThemes(),
            difficultyRange: {
                min: Math.min(...PUZZLE_DATABASE.map(p => p.difficulty)),
                max: Math.max(...PUZZLE_DATABASE.map(p => p.difficulty))
            }
        };
    }
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { PuzzleEngine, PUZZLE_DATABASE };
}
