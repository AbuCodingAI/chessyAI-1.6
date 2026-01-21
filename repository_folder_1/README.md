# Chessy - Multiplayer Chess with AI

A feature-rich chess platform with 17 AI personalities, multiplayer support, and neural network-powered chess engines.

## 🌟 Features

### 🎮 Game Modes
- **Local Multiplayer** - Play with a friend on the same device
- **Online Multiplayer** - Create rooms and play over local network
- **AI Opponents** - 17 different AI personalities from Noob (100 ELO) to Chessy 1.4 (2700+ ELO)

### 🤖 AI Personalities

#### Standard AIs (Stockfish-powered)
- 🐣 **Noob** (100 ELO) - Random moves
- 📚 **Beginner** (400 ELO) - Captures pieces
- ♟️ **Average** (1200 ELO) - Decent player
- ⚔️ **Good** (1500 ELO) - Club player
- 🏆 **Awesome** (1800 ELO) - Expert level
- 👑 **Master** (2000 ELO) - Master level
- 🎖️ **IM** (2500 ELO) - International Master
- 🌟 **GM** (2500 ELO) - Grandmaster
- 💎 **Super GM** (2700 ELO) - Super Grandmaster

#### Neural Network AIs
- 🎖️ **Chessy 1.3** (2500 ELO) - Neural network with deep search (depth 7)
- 🌟 **Chessy 1.4** (2700+ ELO) - Neural network with smart quiescence search (depth 10+)

#### Special/Troll AIs
- 🎲 **Random Guy** - Shows ELO 1, plays at 3400!
- 💬 **Trash Talker** - Shows 3400, plays at 100
- 🤡 **Chocker** - Ultimate disrespect AI (f3+Kf2 opening, mandatory en passant, rage mode)
- 🎲 **Randy** - Pure random moves
- 🤡 **AntiGuess** - Always plays worst moves
- ❓ **Mystery** - Random strength each move

### ⏱️ Time Controls
- Bullet (1, 2, 3 minutes)
- Blitz (3, 5 minutes)
- Rapid (10, 15 minutes)
- Classical (30, 60 minutes)
- Custom time controls

### 🎨 Customization
- Multiple board themes
- Different piece styles
- Sound effects
- Move hints
- Legal move highlighting

## 🚀 Quick Start

### Prerequisites
- Node.js (v14 or higher)
- Python 3.8+ (for neural network AIs)
- Stockfish chess engine

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/chessy.git
cd chessy
```

2. **Install Node.js dependencies**
```bash
npm install
```

3. **Install Python dependencies** (for neural network AIs)
```bash
pip install tensorflow numpy python-chess flask flask-cors
```

4. **Download Stockfish**
   - Download from [stockfishchess.org](https://stockfishchess.org/download/)
   - Place in `stockfish/` folder
   - Update path in `simple-ai.js` if needed

### Running the Server

**Option 1: Using batch file (Windows)**
```bash
START_CHESSY_1.4.bat
```

**Option 2: Manual start**
```bash
node server.js
```

Then open your browser to: **http://localhost:3000**

## 📁 Project Structure

```
chessy/
├── index.html              # Main game interface
├── script.js               # Game logic and UI
├── style.css               # Styling
├── server.js               # Node.js server
├── simple-ai.js            # AI personality handler
├── package.json            # Node dependencies
│
├── neural-ai/              # Neural network chess engines
│   ├── chessy_1.4.py                    # Chessy 1.4 CLI
│   ├── chess_engine_quiescence.py       # GM-level engine
│   ├── chess_engine_deep_search.py      # IM-level engine
│   ├── chess_ai_server.py               # Neural network server
│   ├── TRAIN_CHESSY_1.3_IMPROVED.py     # Training script
│   └── test_quiescence.py               # Test suite
│
├── docs/                   # Documentation
│   ├── CHESSY_1.4_READY.md
│   ├── CHESSY_1.4_GM_PLAN.md
│   ├── HOW_TO_PLAY_CHESSY_1.4.md
│   └── QUICK_START.md
│
├── stockfish/              # Stockfish engine (not included)
│   └── stockfish-windows-x86-64-avx2.exe
│
└── batch files/            # Quick launch scripts
    └── open-site.bat
```

## 🧠 Chessy 1.4 - Neural Network AI

### What Makes It Special?

**Smart Quiescence Search**
- Depth 10 normal search
- Extends search after captures/checks
- Continues until position is quiet
- "Eye of hurricane" verification (searches 1 more move after quiet)
- Only 5-10% quiescence nodes (super efficient!)

**Strength**
- ~2700+ ELO (Grandmaster level)
- Never stops mid-tactic (no horizon effect)
- Sees entire capture sequ Finds all tactical combinations

### Training Chessy 1.4

```bash
cd neural-ai
python TRAIN_CHESSY_1.3_IMPROVED.py
```

Training features:
- Noise injection (random moves every ~10 moves)
- Skips noisy positions (only trains on clean games)
- Dropout layers (30-50%)
- L2 regularization
- Data augmentation
- ~3 hours training time

## 🎮 How to Play

### Against AI
1. Open http://localhost:3000
2. Select "Game Mode" dropdown
3. Choose an AI opponent (e.g., "AI - Chessy 1.4")
4. Click "Start Game"
5. Make your moves!

### Multiplayer
1. Click "Create Room"
2. Share the room code with your friend
3. They enter the code and join
4. Play together!

### Local 2-Player
1. Select "Local 2 Player" mode
2. Click "Start Game"
3. Take turns making moves

## 🤡 Special Feature: Chocker AI

The ultimate disrespect chess AI with:
- **ULTIMATE DISRESPECT Opening** (f3 + Kf2)
- **Mandatory En Passant** (never misses it)
- **Stalemate Forcing** (tries to stalemate when losing)
- **Advantage Throwing** (gives away pieces when winning)
- **RAGE MODE** (activates when you don't take en passant)

See `HOW_TO_PLAY_CHOCKER.md` for full details.

## 📊 Technical Details

### Technologies Used
- **Frontend:** HTML5, CSS3, JavaScript
- **Backend:** Node.js, Express, Socket.io
- **AI:** Stockfish, TensorFlow, Python
- **Chess Logic:** chess.js library

### Neural Nchitecture
- Deep Convolutional Neural Network (CNN)
- Input: 8x8x12 board representation
- Multiple conv layers with dropout
- L2 regularization
- Output: Position evaluation (-1 to +1)

### Search Algorithm
- Minimax with alpha-beta pruning
- Quiescence search for tactical positions
- Transposition table caching
- Move ordering (MVV-LVA)
- Iterative deepening

## 🐛 Troubleshooting

### Server won't start
```bash
# Install dependencies
npm install

# Check Node.js version
node --version  # Should be v14+
```

### AI not responding
- Make sure Stockfish is in the `stockfish/` folder
- Check the path in `simple-ai.js`
- Verify Stockfish executable has correct permissions

### Neural network AI not working
```bash
# Install Python dependencies
pip install tensorflow numpy python-chess

# Test the engine
cd neural-ai
python test_quiescence.py
```

### Board not updating
- Hard refresh the page (Ctrl+F5)
- Clear browser cache
- Check browser console for errors

## 📝 License

MIT License - feel free to use, modify, and distribute!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

## 🎯 Roadmap

### Chessy 1.5 (Future)
- Opening book (GM games database)
- Endgame tablebases (Syzygy)
- Better evaluation network (train on GM games)
- Self-play training (AlphaZero style)
- Target: 2800+ ELO (Super GM level)

See `neural-ai/CHESSY_1.4_GM_PLAN.md` for full roadmap.

## ⭐ Star This Project!

If you enjoy Chessy, please give it a star on GitHub! ⭐

---

**Made with ♟️ by [Abu The Coder]**

**Play now at http://localhost:3000** 🚀
