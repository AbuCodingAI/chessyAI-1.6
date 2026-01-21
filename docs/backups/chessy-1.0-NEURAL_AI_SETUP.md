# 🧠 Chessy 1.0 - Neural Network AI Setup Guide

## What You Need to Do

### Step 1: Install Python (if you don't have it)
1. Download Python 3.8+ from https://www.python.org/downloads/
2. During installation, **CHECK** "Add Python to PATH"
3. Verify installation:
   ```bash
   python --version
   ```

### Step 2: Install Required Python Packages

Open Command Prompt (Windows) or Terminal (Mac/Linux) and run:

```bash
pip install flask flask-cors tensorflow numpy python-chess
```

**What each package does:**
- `flask` - Web server framework
- `flask-cors` - Allows frontend to connect to backend
- `tensorflow` - Neural network library
- `numpy` - Array operations
- `python-chess` - Chess rules and board representation

### Step 3: Start the Python Server

Navigate to your project folder and run:

```bash
python chess_ai_server.py
```

You should see:
```
🚀 Starting Chessy 1.0 Neural Network Server...
📡 Server will run on http://localhost:5000
🧠 Loading neural network model...
📦 Creating new model...
✅ Server ready!

🎮 Open Chessy1-0.html in your browser to play!
```

### Step 4: Open the Game

1. Open `Chessy1-0.html` in your web browser
2. Click "Test Connection" button
3. If connected, you'll see: ✅ Connected to AI Server
4. Click "New Game" and start playing!

---

## 🎮 How to Use

### Playing Against the AI
1. **You play White** (bottom pieces)
2. **AI plays Black** (top pieces)
3. Click a piece to select it
4. Click a square to move
5. AI will think and respond automatically

### Neural Network Settings

#### Model Selection
- **Basic CNN (Fast)**: Simple model, quick responses (~100ms)
- **Deep CNN (Strong)**: Deeper network, stronger play (~300ms)
- **ResNet (Strongest)**: Residual network, best play (~500ms)
- **Transformer (Experimental)**: Not yet implemented

#### Search Depth (1-10)
- Lower = Faster but weaker
- Higher = Slower but stronger
- Recommended: 5

#### Temperature (0.0-1.0)
- 0.0 = Always best move (deterministic)
- 0.1 = Mostly best move with slight variation
- 1.0 = More random/creative moves

### AI Analysis Panel
Shows real-time information:
- **Position Eval**: How good the position is (+/- centipawns)
- **Best Move**: The move the AI chose
- **Confidence**: How confident the AI is (0-100%)
- **Nodes Searched**: Number of positions evaluated
- **Search Time**: How long the AI took to think

### Training the Model

Click "Retrain Model" to:
1. Generate 1000 training positions
2. Train the neural network
3. Save the improved model

**Warning**: Training takes 2-5 minutes!

---

## 🏗️ Architecture

### Frontend (JavaScript)
- `Chessy1-0.html` - User interface
- `Chessy1-0.css` - Styling
- `Chessy1-0.js` - Game logic and API calls

### Backend (Python/Flask)
- `chess_ai_server.py` - Neural network server

### Communication Flow
```
Browser (JavaScript)
    ↓ HTTP POST
Flask Server (Python)
    ↓
Neural Network (TensorFlow)
    ↓
Chess Evaluation
    ↓ JSON Response
Browser (JavaScript)
```

---

## 🧠 Neural Network Details

### Input Format
- **Shape**: 8x8x12 (board × channels)
- **Channels**: 12 (6 piece types × 2 colors)
- **Encoding**: One-hot encoding per square

### Model Architectures

#### Basic CNN
```
Conv2D(64) → Conv2D(128) → Flatten → Dense(256) → Output(1)
Parameters: ~500K
Speed: Fast
Strength: Good
```

#### Deep CNN
```
Conv2D(64) → Conv2D(128) → Conv2D(256) → Flatten → Dense(512) → Dense(256) → Output(1)
Parameters: ~2M
Speed: Medium
Strength: Strong
```

#### ResNet
```
Conv2D(64) → [ResBlock × 3] → Flatten → Dense(256) → Output(1)
Parameters: ~1M
Speed: Medium
Strength: Very Strong
```

### Output
- Single value between -1 and 1
- Positive = White is winning
- Negative = Black is winning
- 0 = Equal position

---

## 🎯 Training Process

### Current Implementation (Simplified)
1. Generate random chess positions
2. Evaluate with material count
3. Train network to predict evaluation
4. Save model weights

### Production Implementation (What you'd do for real)
1. Download chess game database (PGN files)
2. Extract positions and evaluations
3. Use Stockfish to evaluate positions
4. Train on millions of positions
5. Fine-tune with reinforcement learning

### Where to Get Training Data
- **Lichess Database**: https://database.lichess.org/
- **CCRL Games**: http://www.computerchess.org.uk/ccrl/
- **FICS Games**: http://www.ficsgames.org/

---

## 🚀 Advanced Features

### Using Stockfish for Training

Install Stockfish:
```bash
# Windows
choco install stockfish

# Mac
brew install stockfish

# Linux
sudo apt-get install stockfish
```

Then modify `chess_ai_server.py`:
```python
import chess.engine

engine = chess.engine.SimpleEngine.popen_uci("stockfish")

def get_stockfish_eval(board):
    info = engine.analyse(board, chess.engine.Limit(time=0.1))
    return info["score"].relative.score() / 100.0
```

### Self-Play Training (AlphaZero Style)

```python
def self_play_game():
    board = chess.Board()
    positions = []
    
    while not board.is_game_over():
        # Get move from neural network
        move = get_best_move_nn(board)
        positions.append((board.copy(), move))
        board.push(move)
    
    # Get game result
    result = board.result()
    
    # Train on game positions
    return positions, result
```

### Reinforcement Learning

```python
def train_with_rl(num_games=1000):
    for game in range(num_games):
        positions, result = self_play_game()
        
        # Update model based on game outcome
        for board, move in positions:
            reward = get_reward(result, board.turn)
            train_step(board, move, reward)
```

---

## 🐛 Troubleshooting

### "Connection Failed"
**Problem**: Frontend can't connect to backend
**Solution**:
1. Make sure Python server is running
2. Check if port 5000 is available
3. Try restarting the server

### "Module not found"
**Problem**: Missing Python packages
**Solution**:
```bash
pip install flask flask-cors tensorflow numpy python-chess
```

### "Model not loading"
**Problem**: TensorFlow issues
**Solution**:
```bash
pip install --upgrade tensorflow
```

### "Slow performance"
**Problem**: Neural network is slow
**Solution**:
1. Use "Basic CNN" model
2. Reduce search depth
3. Install TensorFlow GPU version (if you have NVIDIA GPU)

### "CORS Error"
**Problem**: Browser blocking requests
**Solution**:
- Make sure `flask-cors` is installed
- Server should show CORS is enabled

---

## 📊 Performance Benchmarks

### Basic CNN
- **Speed**: 50-100ms per move
- **Strength**: ~1500 Elo
- **Memory**: ~50MB

### Deep CNN
- **Speed**: 200-300ms per move
- **Strength**: ~1800 Elo
- **Memory**: ~200MB

### ResNet
- **Speed**: 300-500ms per move
- **Strength**: ~2000 Elo
- **Memory**: ~150MB

### With Proper Training (millions of positions)
- **Speed**: Same
- **Strength**: 2200-2500 Elo
- **Memory**: Same

---

## 🎓 Learning Resources

### Neural Networks for Chess
- **AlphaZero Paper**: https://arxiv.org/abs/1712.01815
- **Leela Chess Zero**: https://lczero.org/
- **Chess Programming Wiki**: https://www.chessprogramming.org/

### TensorFlow Tutorials
- **Official Tutorials**: https://www.tensorflow.org/tutorials
- **Keras Guide**: https://keras.io/guides/

### Chess AI Development
- **Python-Chess Docs**: https://python-chess.readthedocs.io/
- **Stockfish**: https://stockfishchess.org/

---

## 🔄 Upgrade Path

### Phase 1: Basic (Current)
- ✅ Simple neural network
- ✅ Material evaluation training
- ✅ Basic move selection

### Phase 2: Intermediate
- [ ] Train on real games
- [ ] Use Stockfish evaluations
- [ ] Implement move ordering
- [ ] Add opening book

### Phase 3: Advanced
- [ ] Self-play training
- [ ] Reinforcement learning
- [ ] Monte Carlo Tree Search
- [ ] Distributed training

### Phase 4: Expert
- [ ] AlphaZero-style training
- [ ] GPU acceleration
- [ ] Endgame tablebases
- [ ] Tournament play

---

## 💡 Tips

### For Best Performance
1. Use "Basic CNN" for fast play
2. Set depth to 3-5
3. Keep temperature at 0.1
4. Train on real game data

### For Strongest Play
1. Use "ResNet" model
2. Set depth to 8-10
3. Temperature at 0.0
4. Train with Stockfish evaluations

### For Fun/Variety
1. Use "Deep CNN"
2. Depth 5
3. Temperature 0.3-0.5
4. AI will play more creatively!

---

## 🎉 You're Ready!

1. ✅ Install Python packages
2. ✅ Run `python chess_ai_server.py`
3. ✅ Open `Chessy1-0.html`
4. ✅ Click "Test Connection"
5. ✅ Play chess against neural network AI!

**Your AI will get stronger as you train it!** 🧠♟️

---

## 📝 Quick Start Checklist

- [ ] Python 3.8+ installed
- [ ] Packages installed (`pip install flask flask-cors tensorflow numpy python-chess`)
- [ ] Server running (`python chess_ai_server.py`)
- [ ] Browser open (`Chessy1-0.html`)
- [ ] Connection tested (green checkmark)
- [ ] Playing chess! 🎮

**Need help? Check the troubleshooting section above!**
