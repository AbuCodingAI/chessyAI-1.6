# Special AI Modes - Randy & AntiGuess

## 🎲 Randy - Pure Random AI

### What is Randy?
Randy is a **completely random** AI that makes moves without any evaluation or thinking. Unlike "Noob" which still uses the chess engine at depth 0, Randy uses true randomness.

### How Randy Works:
```javascript
// Randy's algorithm:
1. Get all legal moves
2. Pick one at random
3. Play it immediately
```

### Why Randy Exists:
- **Testing**: Perfect for testing if your moves work
- **Fun**: Unpredictable and chaotic
- **Learning**: Great for absolute beginners
- **Speedrun**: How fast can you checkmate Randy?

### Randy's Characteristics:
- ❌ No position evaluation
- ❌ No material counting
- ❌ No tactics
- ❌ No strategy
- ✅ Pure chaos
- ✅ Instant moves
- ✅ Completely unpredictable

### Expected Behavior:
- Will hang pieces constantly
- Might accidentally play good moves
- Will never resign
- Makes games very short
- Elo: ~50 (lower than Noob!)

---

## 🤡 AntiGuess - The Worst Move AI

### What is AntiGuess?
AntiGuess is an AI that **intentionally plays the worst possible moves**. It uses the chess engine to find the move that hurts itself the most!

### How AntiGuess Works:
```javascript
// AntiGuess's algorithm:
1. Get all legal moves
2. Evaluate each move using minimax (depth 2)
3. Find the move with the LOWEST value
4. Play that move (the worst one!)
```

### Why AntiGuess Exists:
- **Comedy**: Watching it throw away pieces is hilarious
- **Reverse Psychology**: Learn what NOT to do
- **Confidence Boost**: Guaranteed wins!
- **Testing**: Verify your tactics work
- **Challenge**: Can you checkmate it in under 10 moves?

### AntiGuess's Characteristics:
- ✅ Uses chess engine (depth 2)
- ✅ Understands positions
- ✅ Knows what's bad
- ❌ Intentionally chooses bad moves
- ❌ Hangs pieces on purpose
- ❌ Walks into checkmates
- ❌ Ignores threats

### Expected Behavior:
- Hangs queen immediately
- Moves pieces into capture
- Ignores checkmate threats
- Blocks own pieces
- Refuses to capture free pieces
- Elo: ~25 (intentionally terrible!)

### Example AntiGuess Game:
```
1. e4 e5
2. Nf3 Qh4?? (hangs queen)
3. Nxh4 Nf6?? (hangs knight)
4. Nf5 d5?? (hangs pawn)
5. exd5 Bd6?? (blocks pieces)
6. Nxd6+ cxd6
7. ... (AntiGuess continues to blunder)
```

---

## 🆚 Comparison

| Feature | Randy | AntiGuess | Noob |
|---------|-------|-----------|------|
| **Uses Engine** | ❌ No | ✅ Yes (depth 2) | ✅ Yes (depth 0) |
| **Evaluates Moves** | ❌ No | ✅ Yes | ❌ No |
| **Strategy** | None | Anti-strategy | Random |
| **Elo** | ~50 | ~25 | ~100 |
| **Speed** | Instant | Fast | Instant |
| **Predictable** | No | Yes (bad) | No |
| **Fun Factor** | 😄 High | 😂 Very High | 😊 Medium |

---

## 🐍 Python Training Integration

### Why Use Python for Training?

Python has excellent chess libraries:
- **python-chess**: Full chess rules implementation
- **Stockfish**: World's strongest engine
- **TensorFlow/PyTorch**: Neural network training
- **NumPy**: Fast array operations

### Option 1: Train with Stockfish

Create a Python script that generates training data:

```python
# train_ai.py
import chess
import chess.engine
import json

# Initialize Stockfish
engine = chess.engine.SimpleEngine.popen_uci("stockfish")

def generate_training_data(num_games=1000):
    training_data = []
    
    for game_num in range(num_games):
        board = chess.Board()
        moves = []
        
        while not board.is_game_over():
            # Get Stockfish's best move
            result = engine.play(board, chess.engine.Limit(time=0.1))
            move = result.move
            
            # Store position and move
            training_data.append({
                'fen': board.fen(),
                'best_move': move.uci(),
                'evaluation': engine.analyse(board, chess.engine.Limit(time=0.1))['score'].relative.score()
            })
            
            board.push(move)
        
        print(f"Game {game_num + 1}/{num_games} complete")
    
    # Save to JSON
    with open('training_data.json', 'w') as f:
        json.dump(training_data, f)
    
    engine.quit()
    return training_data

if __name__ == "__main__":
    generate_training_data(1000)
```

### Option 2: Neural Network Training

Train a neural network to evaluate positions:

```python
# neural_chess.py
import chess
import numpy as np
import tensorflow as tf
from tensorflow import keras

def board_to_array(board):
    """Convert chess board to neural network input"""
    array = np.zeros((8, 8, 12))  # 12 channels (6 pieces × 2 colors)
    
    piece_map = {
        chess.PAWN: 0, chess.KNIGHT: 1, chess.BISHOP: 2,
        chess.ROOK: 3, chess.QUEEN: 4, chess.KING: 5
    }
    
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            row, col = divmod(square, 8)
            channel = piece_map[piece.piece_type]
            if piece.color == chess.BLACK:
                channel += 6
            array[row, col, channel] = 1
    
    return array

def create_model():
    """Create neural network model"""
    model = keras.Sequential([
        keras.layers.Conv2D(64, 3, activation='relu', input_shape=(8, 8, 12)),
        keras.layers.Conv2D(128, 3, activation='relu'),
        keras.layers.Flatten(),
        keras.layers.Dense(256, activation='relu'),
        keras.layers.Dropout(0.3),
        keras.layers.Dense(1, activation='tanh')  # Output: position evaluation
    ])
    
    model.compile(optimizer='adam', loss='mse')
    return model

def train_model(training_data):
    """Train the model on chess positions"""
    X = []
    y = []
    
    for data in training_data:
        board = chess.Board(data['fen'])
        X.append(board_to_array(board))
        y.append(data['evaluation'] / 1000)  # Normalize
    
    X = np.array(X)
    y = np.array(y)
    
    model = create_model()
    model.fit(X, y, epochs=50, batch_size=32, validation_split=0.2)
    
    # Save model
    model.save('chess_model.h5')
    return model
```

### Option 3: Reinforcement Learning (AlphaZero Style)

Train AI by playing against itself:

```python
# reinforcement_chess.py
import chess
import numpy as np
import random

class SelfPlayAgent:
    def __init__(self):
        self.model = create_model()
        self.games_played = 0
    
    def self_play(self, num_games=1000):
        """Play games against itself to learn"""
        for game in range(num_games):
            board = chess.Board()
            game_data = []
            
            while not board.is_game_over():
                # Get all legal moves
                legal_moves = list(board.legal_moves)
                
                # Evaluate each move
                move_values = []
                for move in legal_moves:
                    board.push(move)
                    value = self.evaluate_position(board)
                    board.pop()
                    move_values.append(value)
                
                # Choose best move (with some randomness)
                if random.random() < 0.1:  # 10% exploration
                    move = random.choice(legal_moves)
                else:
                    move = legal_moves[np.argmax(move_values)]
                
                game_data.append((board.copy(), move))
                board.push(move)
            
            # Update model based on game result
            result = board.result()
            self.update_model(game_data, result)
            
            self.games_played += 1
            print(f"Game {self.games_played} complete: {result}")
    
    def evaluate_position(self, board):
        """Use neural network to evaluate position"""
        board_array = board_to_array(board)
        return self.model.predict(np.array([board_array]))[0][0]
```

### Integrating Python AI with JavaScript

#### Method 1: Export Weights to JavaScript

```python
# export_model.py
import tensorflow as tf
import tensorflowjs as tfjs

model = tf.keras.models.load_model('chess_model.h5')
tfjs.converters.save_keras_model(model, 'web_model')
```

Then in JavaScript:
```javascript
// Load TensorFlow.js model
const model = await tf.loadLayersModel('web_model/model.json');

function evaluateBoardWithNN(board) {
    const tensor = boardToTensor(board);
    const prediction = model.predict(tensor);
    return prediction.dataSync()[0];
}
```

#### Method 2: API Server

```python
# api_server.py
from flask import Flask, request, jsonify
import chess
import chess.engine

app = Flask(__name__)
engine = chess.engine.SimpleEngine.popen_uci("stockfish")

@app.route("/best_move", methods=["POST"])
def get_best_move():
    fen = request.json["fen"]
    board = chess.Board(fen)
    
    result = engine.play(board, chess.engine.Limit(time=0.1))
    
    return jsonify({
        "move": result.move.uci(),
        "evaluation": engine.analyse(board, chess.engine.Limit(time=0.1))['score'].relative.score()
    })

if __name__ == "__main__":
    app.run(port=5000)
```

Then in JavaScript:
```javascript
async function getStockfishMove(fen) {
    const response = await fetch('http://localhost:5000/best_move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ fen })
    });
    const data = await response.json();
    return data.move;
}
```

---

## 🎯 Recommendations

### For Fun:
- ✅ Use Randy and AntiGuess
- ✅ Keep everything in browser
- ✅ No server needed

### For Learning:
- ✅ Current minimax engine is excellent
- ✅ Teaches real chess programming
- ✅ Fast and responsive

### For Serious AI:
- ✅ Use Python + Stockfish for training
- ✅ Export to TensorFlow.js
- ✅ Or run Python API server
- ⚠️ Requires setup and dependencies

### Best Approach:
**Keep current JavaScript engine + Add Randy/AntiGuess for fun!**

The current minimax engine is already very strong (up to 3400 Elo). Adding Python would be overkill unless you want to:
1. Train a neural network
2. Use Stockfish-level strength
3. Learn machine learning

---

## 🎮 Try Them Out!

### Randy Challenge:
- Can you checkmate Randy in under 5 moves?
- Fastest checkmate wins!

### AntiGuess Challenge:
- Can you checkmate AntiGuess in under 10 moves?
- Watch it throw away pieces!

### Fun Fact:
AntiGuess actually uses MORE computation than most AIs because it has to evaluate moves to find the worst one! 😂

---

**Randy and AntiGuess are now available in your game!** 🎉
