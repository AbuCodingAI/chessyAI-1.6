# Design Document

## Overview

This design outlines the implementation approach for improving the Chessy chess platform with: 1) Weakened Noob AI for beginners, 2) Mate detection for Chessy 1.3/1.4 neural networks, 3) Puzzle system, and 4) Lesson system. The solution focuses on client-side implementation using existing infrastructure and local storage for progress tracking.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Chessy Platform                       │
├─────────────────────────────────────────────────────────┤
│  UI Layer (index.html, style.css)                       │
│  ├─ Play View (existing)                                │
│  ├─ Puzzles View (enhanced)                             │
│  └─ Learn View (enhanced)                               │
├─────────────────────────────────────────────────────────┤
│  Game Logic Layer (script.js)                           │
│  ├─ Game State Management                               │
│  ├─ Move Validation                                     │
│  ├─ Puzzle Engine (new)                                 │
│  └─ Lesson Engine (new)                                 │
├─────────────────────────────────────────────────────────┤
│  AI Layer (simple-ai.js)                                │
│  ├─ Noob AI (weakened)                                  │
│  ├─ Chessy 1.3/1.4 (mate detection added)               │
│  └─ Stockfish Integration                               │
├─────────────────────────────────────────────────────────┤
│  Data Layer (localStorage)                              │
│  ├─ Puzzle Progress                                     │
│  ├─ Lesson Progress                                     │
│  └─ User Statistics                                     │
└─────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### 1. Noob AI Weakness Implementation

**File:** `repository_folder_1/simple-ai.js`

**Current Issue:** Noob AI is too strong - beats beginners easily

**Design Solution:**

```javascript
/**
 * NOOB (ELO 100)
 * 70% random moves, 30% basic captures
 * Prevents repetitive shuffling
 */
noob(moves, lastMove = null) {
    // Filter out moves that would repeat the last move (undo it)
    let filteredMoves = moves;
    if (lastMove) {
        // Prevent moving the same piece back to where it came from
        filteredMoves = moves.filter(m => {
            // If last move was e2-e4, don't allow e4-e2
            return !(m.from === lastMove.to && m.to === lastMove.from);
        });
        
        // If we filtered out all moves, use original moves
        if (filteredMoves.length === 0) {
            filteredMoves = moves;
        }
    }
    
    // 70% chance: completely random move
    if (Math.random() < 0.7) {
        return filteredMoves[Math.floor(Math.random() * filteredMoves.length)];
    }
    
    // 30% chance: try to capture something
    const captures = filteredMoves.filter(m => m.captured);
    if (captures.length > 0) {
        return captures[Math.floor(Math.random() * captures.length)];
    }
    
    // No captures available, random move
    return filteredMoves[Math.floor(Math.random() * filteredMoves.length)];
}
```

**Key Features:**
- **70% Random:** Makes truly random moves most of the time
- **30% Captures:** Occasionally captures pieces (but randomly, not best capture)
- **No Repetition:** Filters out moves that would undo the last move (e.g., rook shuffling)
- **No Tactics:** Cannot see forks, pins, or any tactical patterns
- **No Stockfish:** Pure random/capture logic, no engine evaluation

### 2. Mate Detection for Chessy 1.3/1.4

**Purpose:** Prevent neural network AIs from missing obvious checkmates

**File:** `repository_folder_1/simple-ai.js`

**Implementation Approach:**

```javascript
/**
 * CHESSY 1.3 - Neural Network with Mate Detection
 * ~2500 ELO (IM level)
 * 
 * NOTE: Chessy 1.3 is a neural network TRAINED by Stockfish, not using Stockfish directly.
 * Stockfish is the trainer, Chessy is the trainee.
 */
async chessy13(fen) {
    // Step 1: Check for mate-in-1 using Stockfish (safety check)
    const mateMove = await this.checkForMate(fen, 1);
    if (mateMove) {
        console.log('Chessy 1.3: Found mate-in-1!');
        return mateMove;
    }
    
    // Step 2: Use Chessy 1.3 neural network
    // TODO: Call neural-ai/chess_engine_deep_search.py
    // TEMPORARY: Using Stockfish depth 20 as placeholder until neural network is integrated
    return await this.stockfishMove(fen, 20);
}

/**
 * CHESSY 1.4 - Neural Network with Advanced Mate Detection
 * ~2700 ELO (GM level)
 * 
 * NOTE: Chessy 1.4 is a neural network TRAINED by Stockfish, not using Stockfish directly.
 * Stockfish is the trainer, Chessy is the trainee.
 */
async chessy14(fen) {
    // Step 1: Check for mate-in-1 or mate-in-2 using Stockfish (safety check)
    const mate1 = await this.checkForMate(fen, 1);
    if (mate1) {
        console.log('Chessy 1.4: Found mate-in-1!');
        return mate1;
    }
    
    const mate2 = await this.checkForMate(fen, 2);
    if (mate2) {
        console.log('Chessy 1.4: Found mate-in-2!');
        return mate2;
    }
    
    // Step 2: Use neural network (placeholder - will integrate Python model)
    // TODO: Call neural-ai/chess_engine_quiescence.py
    // For now, use Stockfish depth 25 as fallback
    return await this.stockfishMove(fen, 25);
}

/**
 * Check for forced mate using Stockfish
 */
async checkForMate(fen, mateDepth) {
    return new Promise((resolve) => {
        const stockfish = spawn(this.stockfishPath);
        let bestMove = null;
        
        stockfish.stdin.write('uci\n');
        stockfish.stdin.write(`position fen ${fen}\n`);
        stockfish.stdin.write(`go mate ${mateDepth}\n`);
        
        stockfish.stdout.on('data', (data) => {
            const output = data.toString();
            
            // Look for mate found
            if (output.includes('score mate')) {
                const match = output.match(/bestmove ([a-h][1-8][a-h][1-8][qrbn]?)/);
                if (match) {
                    bestMove = match[1];
                }
            }
            
            if (output.includes('bestmove')) {
                stockfish.kill();
                resolve(bestMove);
            }
        });
        
        // Timeout after 5 seconds
        setTimeout(() => {
            stockfish.kill();
            resolve(null);
        }, 5000);
    });
}
```

**Algorithm:**
1. **Mate Check First:** Before using neural network, check for forced mates using Stockfish
2. **Chessy 1.3:** Checks mate-in-1 using Stockfish, then uses neural network
3. **Chessy 1.4:** Checks mate-in-1 and mate-in-2 using Stockfish, then uses neural network
4. **Neural Network:** Chessy 1.3/1.4 are neural networks TRAINED by Stockfish (Stockfish = trainer, Chessy = trainee)
5. **Temporary Placeholder:** Until neural networks are integrated, using Stockfish depth 20/25 as placeholder
6. **Fast Execution:** Mate search limited to 5 seconds max

### 3. Puzzle System

**File:** `repository_folder_1/puzzle-engine.js` (new)

**Data Structure:**

```javascript
const PUZZLE_DATABASE = [
    {
        id: "puzzle_001",
        fen: "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4",
        theme: "Fork",
        difficulty: 800,
        solution: ["Nxe5"],  // Just the winning move(s)
        description: "White to move. Win material with a knight fork.",
        hint: "Look for a knight move that attacks two pieces at once."
    },
    {
        id: "puzzle_002",
        fen: "r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/3P1N2/PPP2PPP/RNBQK2R w KQkq - 0 5",
        theme: "Pin",
        difficulty: 900,
        solution: ["Bxf7+"],
        description: "White to move. Win material with a pin.",
        hint: "The black king and knight are on the same diagonal."
    }
    // ... more puzzles
];
```

**Components:**

```javascript
class PuzzleEngine {
    constructor() {
        this.currentPuzzle = null;
        this.moveIndex = 0;
        this.attempts = 0;
    }
    
    loadPuzzle(puzzleId) {
        this.currentPuzzle = PUZZLE_DATABASE.find(p => p.id === puzzleId);
        this.moveIndex = 0;
        this.attempts = 0;
        return this.currentPuzzle;
    }
    
    validateMove(move) {
        const expectedMove = this.currentPuzzle.solution[this.moveIndex];
        
        if (move === expectedMove) {
            this.moveIndex++;
            return {
                correct: true,
                complete: this.moveIndex >= this.currentPuzzle.solution.length,
                message: "Correct! Great move!"
            };
        } else {
            this.attempts++;
            return {
                correct: false,
                complete: false,
                message: "Not quite. Try again!"
            };
        }
    }
    
    getHint() {
        return this.currentPuzzle.hint;
    }
    
    showSolution() {
        return {
            moves: this.currentPuzzle.solution,
            explanation: this.currentPuzzle.description
        };
    }
}
```

**UI Integration:**
- Display puzzle board in "Puzzles" view
- Show theme, difficulty, and description
- Provide "Hint" and "Show Solution" buttons
- Track attempts and time taken
- Update puzzle rating after completion

### 4. Lesson System

**File:** `repository_folder_1/lesson-engine.js` (new)

**Data Structure:**

```javascript
const LESSON_DATABASE = [
    {
        id: "lesson_001",
        title: "How the Pieces Move",
        level: "beginner",
        sections: [
            {
                type: "text",
                content: "In chess, each piece moves in a unique way. Let's start with the pawn."
            },
            {
                type: "diagram",
                fen: "8/8/8/8/3P4/8/8/8 w - - 0 1",
                caption: "The pawn moves forward one square (or two on its first move)."
            },
            {
                type: "practice",
                fen: "8/8/8/8/8/8/4P3/8 w - - 0 1",
                task: "Move the pawn forward two squares",
                solution: ["e4"],
                feedback: "Perfect! Pawns can move two squares on their first move."
            }
        ]
    }
    // ... more lessons
];
```

**Components:**

```javascript
class LessonEngine {
    constructor() {
        this.currentLesson = null;
        this.sectionIndex = 0;
    }
    
    loadLesson(lessonId) {
        this.currentLesson = LESSON_DATABASE.find(l => l.id === lessonId);
        this.sectionIndex = 0;
        return this.currentLesson;
    }
    
    getCurrentSection() {
        return this.currentLesson.sections[this.sectionIndex];
    }
    
    nextSection() {
        this.sectionIndex++;
        return this.sectionIndex < this.currentLesson.sections.length;
    }
    
    validatePractice(move) {
        const section = this.getCurrentSection();
        if (section.type !== 'practice') return null;
        
        return section.solution.includes(move);
    }
    
    markComplete() {
        // Save to localStorage
        const progress = JSON.parse(localStorage.getItem('chessLessons')) || {};
        progress[this.currentLesson.id] = {
            completed: true,
            completedAt: new Date().toISOString()
        };
        localStorage.setItem('chessLessons', JSON.stringify(progress));
    }
}
```

**UI Integration:**
- Display lesson content in "Learn" view
- Render text, diagrams, and practice positions
- Allow user to progress through sections
- Mark lessons as complete
- Show progress indicator

### 5. Draw Conditions Detection

**File:** `repository_folder_1/script.js` (existing - add to game logic)

**Purpose:** Detect and declare draws according to official chess rules

**Implementation Approach:**

```javascript
class DrawDetector {
    constructor() {
        this.positionHistory = [];  // Store FEN positions
        this.movesSinceProgress = 0;  // For 50-move rule
    }
    
    /**
     * Check for threefold repetition
     */
    checkThreefoldRepetition(currentFen) {
        // Simplify FEN (ignore move counters)
        const simplifiedFen = currentFen.split(' ').slice(0, 4).join(' ');
        
        // Count occurrences
        const count = this.positionHistory.filter(fen => {
            const simplified = fen.split(' ').slice(0, 4).join(' ');
            return simplified === simplifiedFen;
        }).length;
        
        return count >= 3;
    }
    
    /**
     * Check for 50-move rule
     */
    checkFiftyMoveRule() {
        return this.movesSinceProgress >= 100;  // 100 half-moves = 50 full moves
    }
    
    /**
     * Check for stalemate
     */
    checkStalemate(game) {
        // No legal moves and not in check
        return game.moves().length === 0 && !game.inCheck();
    }
    
    /**
     * Check for insufficient material
     */
    checkInsufficientMaterial(game) {
        const board = game.board();
        const pieces = [];
        
        // Collect all pieces
        for (let row of board) {
            for (let square of row) {
                if (square) {
                    pieces.push(square.type);
                }
            }
        }
        
        // King vs King
        if (pieces.length === 2) return true;
        
        // King + Bishop vs King or King + Knight vs King
        if (pieces.length === 3) {
            return pieces.includes('b') || pieces.includes('n');
        }
        
        // King + Bishop vs King + Bishop (same color bishops)
        // TODO: Implement same-color bishop check
        
        return false;
    }
    
    /**
     * Update position history
     */
    addPosition(fen, isPawnMoveOrCapture) {
        this.positionHistory.push(fen);
        
        if (isPawnMoveOrCapture) {
            this.movesSinceProgress = 0;
        } else {
            this.movesSinceProgress++;
        }
    }
    
    /**
     * Check all draw conditions
     */
    checkForDraw(game, currentFen) {
        if (this.checkThreefoldRepetition(currentFen)) {
            return { isDraw: true, reason: 'threefold-repetition' };
        }
        
        if (this.checkFiftyMoveRule()) {
            return { isDraw: true, reason: 'fifty-move-rule' };
        }
        
        if (this.checkStalemate(game)) {
            return { isDraw: true, reason: 'stalemate' };
        }
        
        if (this.checkInsufficientMaterial(game)) {
            return { isDraw: true, reason: 'insufficient-material' };
        }
        
        return { isDraw: false };
    }
}
```

**Integration:**
- Initialize DrawDetector when game starts
- Call `addPosition()` after each move
- Call `checkForDraw()` after each move
- Display draw message if detected

### 6. Progress Tracking

**File:** `repository_folder_1/progress-tracker.js` (new)

**LocalStorage Schema:**

```javascript
{
    puzzles: {
        solved: ["puzzle_001", "puzzle_002"],
        rating: 1000,
        streak: 3,
        lastSolved: "2025-11-10",
        totalAttempts: 15,
        correctFirstTry: 8
    },
    lessons: {
        completed: ["lesson_001"],
        currentLesson: "lesson_002",
        totalLessons: 15,
        progress: 0.067  // 1/15 = 6.7%
    },
    achievements: [
        { id: "first_puzzle", name: "First Steps", unlocked: true, date: "2025-11-10" },
        { id: "puzzle_streak_3", name: "On a Roll", unlocked: true, date: "2025-11-10" }
    ]
}
```

**Rating Algorithm:**

```javascript
function updatePuzzleRating(currentRating, puzzleDifficulty, correct, attempts) {
    const K = 32;  // Rating change factor
    const expectedScore = 1 / (1 + Math.pow(10, (puzzleDifficulty - currentRating) / 400));
    const actualScore = correct ? (attempts === 1 ? 1 : 0.5) : 0;
    const ratingChange = K * (actualScore - expectedScore);
    
    return Math.round(currentRating + ratingChange);
}
```

**Achievement System:**

```javascript
const ACHIEVEMENTS = [
    { id: "first_puzzle", name: "First Steps", condition: (stats) => stats.solved.length >= 1 },
    { id: "puzzle_10", name: "Tactician", condition: (stats) => stats.solved.length >= 10 },
    { id: "puzzle_50", name: "Master Tactician", condition: (stats) => stats.solved.length >= 50 },
    { id: "streak_3", name: "On a Roll", condition: (stats) => stats.streak >= 3 },
    { id: "streak_7", name: "Unstoppable", condition: (stats) => stats.streak >= 7 },
    { id: "first_lesson", name: "Student", condition: (stats) => stats.completed.length >= 1 },
    { id: "lesson_5", name: "Scholar", condition: (stats) => stats.completed.length >= 5 }
];
```

## Data Models

### Puzzle Model

```javascript
class Puzzle {
    constructor(data) {
        this.id = data.id;
        this.fen = data.fen;
        this.theme = data.theme;
        this.difficulty = data.difficulty;
        this.solution = data.solution;
        this.description = data.description;
        this.hint = data.hint;
    }
}
```

### Lesson Model

```javascript
class Lesson {
    constructor(data) {
        this.id = data.id;
        this.title = data.title;
        this.level = data.level;
        this.sections = data.sections;
    }
}
```

## Error Handling

### AI Move Generation Errors

- **Mate Search Timeout:** If Stockfish mate search takes >5 seconds, skip and use neural network
- **Stockfish Crash:** Catch spawn errors, fall back to random legal move
- **Invalid Position:** Validate FEN before sending to Stockfish

### Puzzle System Errors

- **Invalid Move:** Show "Try again" message, increment attempts
- **Missing Puzzle:** Show error, load next available puzzle
- **Storage Full:** Clear old puzzle history (keep last 50)

### Lesson System Errors

- **Missing Content:** Show placeholder text, log error
- **Invalid Practice Position:** Skip practice, move to next section
- **Save Failure:** Retry once, show warning if still fails

## Testing Strategy

### Manual Testing Priority

1. **Noob AI Testing**
   - Play 5 games against Noob AI
   - Verify it's beatable for beginners
   - Confirm 70% moves feel random

2. **Chessy 1.3/1.4 Mate Detection**
   - Set up mate-in-1 positions
   - Verify Chessy 1.3 and 1.4 find checkmate
   - Test mate-in-2 for Chessy 1.4

3. **Puzzle Flow**
   - Solve 5 puzzles
   - Test hint system
   - Verify rating updates

4. **Lesson Flow**
   - Complete 2 lessons
   - Test practice positions
   - Verify progress saves

## Implementation Phases

### Phase 1: Noob AI Fix (Priority: CRITICAL)
- Modify `noob()` function in simple-ai.js
- Test against beginners
- Verify ELO ~100-300

### Phase 2: Mate Detection (Priority: HIGH)
- Implement `checkForMate()` function
- Update `chessy13()` and `chessy14()` functions
- Test with mate-in-1 and mate-in-2 positions

### Phase 3: Puzzle System (Priority: HIGH)
- Create puzzle-engine.js
- Add 20 starter puzzles
- Implement puzzle UI
- Add progress tracking

### Phase 4: Lesson System (Priority: MEDIUM)
- Create lesson-engine.js
- Create 5 beginner lessons
- Implement lesson UI
- Add progress tracking

### Phase 5: Polish (Priority: LOW)
- Add more puzzles (50 total)
- Add more lessons (15 total)
- Implement achievement system
- UI/UX improvements
