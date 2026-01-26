# 🚀 Chessy 1.6 - C++ Neural Chess Engine

A production-grade chess engine written in C++ with neural network evaluation, Stockfish training data, and 5% blunder injection for realistic gameplay.

## 🎯 Features

### Core Chess Engine
- **Proper Chess Rules**: Full implementation of all chess rules
  - Castling (kingside & queenside)
  - En passant captures
  - Pawn promotion
  - Check/checkmate/stalemate detection
  
- **Bitboard Representation**: Fast 64-bit board representation
  - Efficient move generation
  - Quick position evaluation
  - Transposition table support

- **Move Generation**: Complete legal move generation
  - Pseudo-legal move generation
  - Legal move filtering
  - Move validation

### Neural Network
- **Architecture**: 768 → 512 → 256 → 128 → 1
  - Input: 768 features (8x8x12 piece placement)
  - Hidden layers: ReLU activation
  - Output: Tanh activation (-1 to +1 evaluation)

- **Training**: Supervised learning from Stockfish
  - 100,000+ training examples
  - 80/20 train/validation split
  - Adaptive learning rate

### Training Framework
- **Stockfish Integration**: High-quality training data
  - Depth 25 analysis
  - Clean evaluations
  - Realistic positions

- **Blunder Injection**: 5% intentional mistakes
  - AI learns to punish blunders
  - Realistic game scenarios
  - Separate blunder detection

- **Self-Play**: Continuous improvement
  - 100+ self-play games
  - Fine-tuning on own games
  - Discover new strategies

### Search Algorithm
- **Alpha-Beta Search**: Efficient game tree search
  - Move ordering
  - Beta cutoffs
  - Transposition table

- **Quiescence Search**: Capture analysis
  - Avoid horizon effect
  - Accurate evaluations
  - Tactical awareness

## 📋 Requirements

### System Requirements
- **OS**: Windows, Linux, macOS
- **Compiler**: C++17 compatible (MSVC, GCC, Clang)
- **RAM**: 4GB minimum (8GB recommended)
- **Disk**: 2GB for training data and models

### Dependencies
- **Eigen3**: Linear algebra library
- **Boost**: Process management
- **nlohmann/json**: JSON serialization
- **Stockfish**: Chess engine (for training)

### Installation

#### Windows (vcpkg)
```bash
# Install vcpkg
git clone https://github.com/Microsoft/vcpkg.git
cd vcpkg
.\vcpkg\integrate install

# Install dependencies
.\vcpkg install eigen:x64-windows
.\vcpkg install boost:x64-windows
.\vcpkg install nlohmann-json:x64-windows

# Download Stockfish
# https://stockfishchess.org/download/
# Extract to: stockfish/stockfish-windows-x86-64-avx2.exe
```

#### Linux (apt)
```bash
sudo apt-get install libeigen3-dev libboost-all-dev nlohmann-json3-dev

# Download Stockfish
wget https://github.com/official-stockfish/Stockfish/releases/download/sf_15/stockfish_15_linux_x86-64.tar
tar -xf stockfish_15_linux_x86-64.tar
```

#### macOS (brew)
```bash
brew install eigen boost nlohmann-json

# Download Stockfish
brew install stockfish
```

## 🔨 Building

### Create Build Directory
```bash
mkdir build
cd build
```

### Configure with CMake
```bash
# Windows (MSVC)
cmake .. -G "Visual Studio 16 2019" -DCMAKE_TOOLCHAIN_FILE=C:\path\to\vcpkg\scripts\buildsystems\vcpkg.cmake

# Linux/macOS
cmake .. -DCMAKE_BUILD_TYPE=Release
```

### Build
```bash
# Windows
cmake --build . --config Release

# Linux/macOS
make -j4
```

### Output
```
bin/chessy-1.6  (executable)
```

## 🚀 Usage

### Interactive Play
```bash
./chessy-1.6 --play
```

Play against Chessy 1.6 with 6-ply search depth.

**Example:**
```
  a b c d e f g h
8 r n b q k b n r 8
7 p p p p p p p p 7
6 . . . . . . . . 6
5 . . . . . . . . 5
4 . . . . . . . . 4
3 . . . . . . . . 3
2 P P P P P P P P 2
1 R N B Q K B N R 1
  a b c d e f g h

Enter your move (e.g., e2e4): e2e4
Chessy 1.6 is thinking...
Chessy 1.6 plays: e7e5
```

### Generate Training Data
```bash
./chessy-1.6 --generate-data
```

Generates 10,000 games with Stockfish at depth 25.
- Creates: `training_data/stockfish_positions.bin`
- Time: 2-3 hours
- Size: ~500MB

### Train Neural Network
```bash
./chessy-1.6 --train
```

Full training pipeline:
1. Generate training data (if not exists)
2. Train neural network (100 epochs)
3. Self-play improvement (100 games)
4. Test vs Stockfish (200 games)
5. Calculate ELO rating

**Time**: 20-30 hours total
**Output**: `models/chessy_1.6_weights.bin`

### Test vs Stockfish
```bash
./chessy-1.6 --test
```

Play 200 games against Stockfish at depth 10.
- Measures true strength
- Calculates ELO rating
- Analyzes blunder punishment

## 📊 Training Pipeline

### Phase 1: Data Generation (2-3 hours)
```
Stockfish (depth 25) generates 10,000 games
↓
100,000+ training positions extracted
↓
5% blunder injection applied
↓
Positions filtered and normalized
```

### Phase 2: Neural Network Training (4-6 hours)
```
Training data (80,000 positions)
↓
100 epochs of supervised learning
↓
Validation on 20,000 positions
↓
Best weights saved
```

### Phase 3: Self-Play (6-8 hours)
```
Chessy 1.6 vs Chessy 1.6 (100 games)
↓
Learn from own games
↓
Fine-tune weights (20 epochs)
↓
Discover new strategies
```

### Phase 4: Testing (8-10 hours)
```
vs Stockfish depth 10 (200 games)
↓
vs Stockfish depth 15 (100 games)
↓
vs Stockfish depth 20 (50 games)
↓
Calculate ELO rating
```

## 📈 Expected Performance

| Metric | Target | Notes |
|--------|--------|-------|
| ELO Rating | 2600-2800 | IM to GM level |
| vs Stockfish (depth 10) | 45-55% win rate | Competitive |
| vs Stockfish (depth 15) | 30-40% win rate | Challenging |
| vs Stockfish (depth 20) | 15-25% win rate | Very difficult |
| Blunder punishment | 70%+ | Learns from mistakes |
| Training time | 20-30 hours | Full pipeline |

## 🎯 Blunder Injection (5%)

### Why 5%?
- **Realistic**: Humans make mistakes
- **Learning**: AI learns to punish blunders
- **Robustness**: Handles imperfect opponents
- **Competitive**: More interesting games

### How It Works
1. Stockfish generates best move
2. 5% of the time: Select random move instead
3. Mark position as "blunder"
4. AI learns to recognize and punish

### Blunder Detection
- Evaluation drop > 2.0 (200 centipawns)
- Piece loss without compensation
- Tactical oversight
- Positional collapse

## 🔧 Configuration

### Training Config (src/main.cpp)
```cpp
TrainingConfig config;
config.numGamesGeneration = 10000;    // Games for data
config.stockfishDepth = 25;           // Analysis depth
config.blunderRate = 0.05f;           // 5% blunders
config.epochs = 100;                  // Training epochs
config.learningRate = 0.001f;         // Learning rate
config.batchSize = 32;                // Batch size
config.numSelfPlayGames = 100;        // Self-play games
config.numTestGames = 200;            // Test games
```

### Search Config (src/main.cpp)
```cpp
// Interactive play
Move move = search.findBestMove(board, 6);  // 6-ply depth

// Testing
Move move = search.findBestMove(board, 10); // 10-ply depth
```

## 📁 Project Structure

```
chessy-1.6/
├── src/
│   ├── chess/
│   │   ├── board.cpp/h          ← Board representation
│   │   ├── moves.cpp/h          ← Move generation
│   │   ├── rules.cpp/h          ← Chess rules
│   │   └── position.cpp/h       ← Position evaluation
│   ├── engine/
│   │   ├── evaluator.cpp/h      ← Neural evaluation
│   │   ├── search.cpp/h         ← Alpha-beta search
│   │   └── transposition.cpp/h  ← Transposition table
│   ├── training/
│   │   ├── trainer.cpp/h        ← Training loop
│   │   ├── stockfish_interface.cpp/h  ← Stockfish
│   │   └── blunder_injector.cpp/h     ← Blunder injection
│   ├── neural/
│   │   ├── network.cpp/h        ← Neural network
│   │   └── weights.cpp/h        ← Weight management
│   └── main.cpp                 ← Entry point
├── models/
│   └── chessy_1.6_weights.bin   ← Trained weights
├── training_data/
│   └── stockfish_positions.bin  ← Training dataset
├── CMakeLists.txt               ← Build configuration
└── README.md                    ← This file
```

## 🐛 Troubleshooting

### Build Errors

**"Eigen not found"**
```bash
# Windows (vcpkg)
cmake .. -DCMAKE_TOOLCHAIN_FILE=C:\path\to\vcpkg\scripts\buildsystems\vcpkg.cmake

# Linux
sudo apt-get install libeigen3-dev
```

**"Stockfish not found"**
```bash
# Download from: https://stockfishchess.org/download/
# Extract to: stockfish/stockfish-windows-x86-64-avx2.exe
```

### Runtime Errors

**"Out of memory during training"**
- Reduce `numGamesGeneration` in config
- Reduce `batchSize` in config
- Use 64-bit build

**"Training too slow"**
- Reduce `stockfishDepth` (20 instead of 25)
- Reduce `epochs` (50 instead of 100)
- Use Release build (not Debug)

**"Stockfish communication failed"**
- Check Stockfish path
- Verify Stockfish executable exists
- Check file permissions

## 📚 References

- **Chess Programming Wiki**: https://www.chessprogramming.org/
- **Stockfish Source**: https://github.com/official-stockfish/Stockfish
- **Eigen Documentation**: https://eigen.tuxfamily.org/
- **Neural Networks**: https://www.deeplearningbook.org/

## 🎮 Next Steps

1. **Build the project** (30 min)
2. **Test interactive play** (10 min)
3. **Generate training data** (2-3 hours)
4. **Train neural network** (4-6 hours)
5. **Run self-play** (6-8 hours)
6. **Test vs Stockfish** (8-10 hours)
7. **Analyze results** (1 hour)

**Total Development**: ~35-40 hours
**Total Training**: ~20-30 hours

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Opening book integration
- Endgame tablebase support
- Parallel search (multi-threading)
- GPU acceleration for neural network
- Web interface

## 📞 Support

For issues or questions:
1. Check troubleshooting section
2. Review Chess Programming Wiki
3. Check Stockfish documentation
4. Open an issue on GitHub

---

**Ready to build the strongest chess engine? Let's go! ♟️🚀**
