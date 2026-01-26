# 🚀 Chessy 1.6 - C++ Neural Chess Engine

## Vision
Build a production-grade chess engine in C++ with:
- **Proper chess rules enforcement** (move validation, castling, en passant, promotion)
- **Stockfish training framework** (5% blunder injection for learning)
- **Neural network evaluation** (trained on Stockfish positions)
- **Self-play improvement** (learns from its own games)
- **Blunder detection** (learns to punish mistakes)

---

## 🎯 Architecture

### Core Components

```
chessy-1.6/
├── src/
│   ├── chess/
│   │   ├── board.cpp/h          ← Board representation (bitboards)
│   │   ├── moves.cpp/h          ← Move generation & validation
│   │   ├── rules.cpp/h          ← Chess rules (castling, en passant, etc)
│   │   └── position.cpp/h       ← Position evaluation
│   ├── engine/
│   │   ├── evaluator.cpp/h      ← Neural network evaluation
│   │   ├── search.cpp/h         ← Alpha-beta search
│   │   └── transposition.cpp/h  ← Transposition table
│   ├── training/
│   │   ├── trainer.cpp/h        ← Training loop
│   │   ├── stockfish_interface.cpp/h  ← Stockfish communication
│   │   └── blunder_injector.cpp/h     ← 5% blunder injection
│   ├── neural/
│   │   ├── network.cpp/h        ← Neural network (forward pass)
│   │   └── weights.cpp/h        ← Weight management
│   └── main.cpp                 ← Entry point
├── models/
│   └── chessy_1.6_weights.bin   ← Trained weights
├── training_data/
│   ├── stockfish_positions.bin  ← Training dataset
│   └── self_play_games.pgn      ← Self-play games
├── CMakeLists.txt               ← Build configuration
└── requirements.txt             ← Dependencies
```

---

## 📊 Training Pipeline

### Phase 1: Data Generation (2-3 hours)
1. **Stockfish generates positions** (10,000 games)
   - Depth 25 analysis
   - Clean evaluations
   - ~100,000 training examples

2. **Blunder injection** (5% of positions)
   - Stockfish throws intentionally
   - AI learns to punish mistakes
   - Realistic game scenarios

3. **Filter throw positions**
   - Detect blunder positions
   - Mark as "blunder" in dataset
   - Separate training/validation

### Phase 2: Neural Network Training (4-6 hours)
1. **Network architecture**
   - Input: 768 features (8x8x12 piece placement)
   - Hidden: 512 → 256 → 128 neurons
   - Output: Single evaluation (-1 to +1)

2. **Training process**
   - 100 epochs
   - Batch size: 32
   - Learning rate: 0.001 (adaptive)
   - Loss: Mean squared error

3. **Validation**
   - 20% validation set
   - Early stopping if overfitting
   - Save best weights

### Phase 3: Self-Play Improvement (6-8 hours)
1. **Self-play games** (100 games)
   - Chessy 1.6 vs Chessy 1.6
   - Time control: 5 seconds per move
   - Discover new strategies

2. **Fine-tuning** (20 epochs)
   - Learn from self-play games
   - Adapt to own style
   - Improve weak positions

### Phase 4: Rigorous Testing (8-10 hours)
1. **vs Stockfish** (200 games)
   - Depth 10: Measure strength
   - Depth 15: Challenge level
   - Depth 20: Maximum difficulty

2. **ELO calculation**
   - Win rate → ELO rating
   - Expected: 2600-2800 ELO
   - Compare with Chessy 1.5

3. **Blunder analysis**
   - How often does it punish blunders?
   - Does it make blunders?
   - Improvement metrics

---

## 🔧 Key Features

### 1. Proper Chess Rules
```cpp
// Castling validation
bool isValidCastling(Position& pos, Move move) {
    // Check: king/rook not moved
    // Check: no pieces between
    // Check: king not in check
    // Check: king doesn't pass through check
}

// En passant
bool isValidEnPassant(Position& pos, Move move) {
    // Check: pawn moved 2 squares last turn
    // Check: capturing pawn is on correct rank
}

// Promotion
Move handlePromotion(Position& pos, Move move) {
    // Pawn reaches 8th/1st rank
    // Choose piece: Q, R, B, N
}
```

### 2. Stockfish Integration
```cpp
class StockfishInterface {
    // Start Stockfish process
    void initialize(string path);
    
    // Get best move
    Move getBestMove(Position& pos, int depth);
    
    // Get evaluation
    float getEvaluation(Position& pos, int depth);
    
    // 5% blunder injection
    Move getBlunderMove(Position& pos);
};
```

### 3. Neural Network Evaluation
```cpp
class NeuralEvaluator {
    // Load trained weights
    void loadWeights(string path);
    
    // Forward pass
    float evaluate(Position& pos);
    
    // Feature extraction
    vector<float> extractFeatures(Position& pos);
};
```

### 4. Training Framework
```cpp
class Trainer {
    // Generate training data
    void generateTrainingData(int numGames);
    
    // Train neural network
    void train(int epochs, float learningRate);
    
    // Self-play
    void selfPlay(int numGames);
    
    // Evaluate
    float evaluate(int numGames);
};
```

---

## 📈 Expected Performance

| Metric | Target | Notes |
|--------|--------|-------|
| ELO Rating | 2600-2800 | IM to GM level |
| vs Stockfish (depth 10) | 45-55% win rate | Competitive |
| vs Stockfish (depth 15) | 30-40% win rate | Challenging |
| Blunder punishment | 70%+ | Learns from mistakes |
| Training time | 20-30 hours | Full pipeline |

---

## 🛠️ Dependencies

### C++ Libraries
- **Eigen** - Linear algebra (neural network)
- **Boost** - Process management (Stockfish)
- **nlohmann/json** - Data serialization

### External Tools
- **Stockfish** - Chess engine (training data)
- **CMake** - Build system
- **Python** (optional) - Data analysis

### Installation
```bash
# Windows (vcpkg)
vcpkg install eigen:x64-windows
vcpkg install boost:x64-windows
vcpkg install nlohmann-json:x64-windows

# Or manual installation
# Download from: https://eigen.tuxfamily.org/
# Download from: https://www.boost.org/
```

---

## 🚀 Build & Run

### Build
```bash
mkdir build
cd build
cmake ..
cmake --build . --config Release
```

### Generate Training Data
```bash
./chessy-1.6 --generate-data --games 10000 --stockfish-depth 25
```

### Train Neural Network
```bash
./chessy-1.6 --train --epochs 100 --batch-size 32
```

### Self-Play
```bash
./chessy-1.6 --self-play --games 100 --time-per-move 5
```

### Test vs Stockfish
```bash
./chessy-1.6 --test --games 200 --stockfish-depth 10
```

### Play Interactive
```bash
./chessy-1.6 --play
```

---

## 📋 Implementation Phases

### Phase 1: Core Engine (Days 1-2)
- [ ] Board representation (bitboards)
- [ ] Move generation
- [ ] Chess rules validation
- [ ] Basic search (minimax)

### Phase 2: Stockfish Integration (Days 3-4)
- [ ] Stockfish interface
- [ ] Data generation
- [ ] Blunder injection (5%)
- [ ] Position filtering

### Phase 3: Neural Network (Days 5-6)
- [ ] Network architecture
- [ ] Feature extraction
- [ ] Training loop
- [ ] Weight serialization

### Phase 4: Training Pipeline (Days 7-8)
- [ ] Data generation script
- [ ] Training script
- [ ] Self-play script
- [ ] Testing framework

### Phase 5: Optimization & Testing (Days 9-10)
- [ ] Performance optimization
- [ ] Blunder analysis
- [ ] ELO calculation
- [ ] Documentation

---

## 🎯 Success Criteria

✅ **Must Have**
- Proper chess rules (all edge cases)
- Stockfish training data generation
- 5% blunder injection working
- Neural network training
- ELO > 2400

✅ **Should Have**
- Self-play improvement
- Blunder punishment analysis
- Performance optimization
- Comprehensive testing

✅ **Nice to Have**
- Opening book
- Endgame tablebase
- Web interface
- Real-time analysis

---

## 📚 References

- **Chess Programming Wiki**: https://www.chessprogramming.org/
- **Stockfish Source**: https://github.com/official-stockfish/Stockfish
- **Neural Networks**: https://www.deeplearningbook.org/
- **Bitboards**: https://www.chessprogramming.org/Bitboards

---

## 🎮 Next Steps

1. **Create project structure** (30 min)
2. **Implement board & moves** (4 hours)
3. **Add Stockfish interface** (2 hours)
4. **Build neural network** (3 hours)
5. **Create training pipeline** (2 hours)
6. **Run full training** (20-30 hours)
7. **Test & optimize** (4 hours)

**Total: ~35-40 hours of development + 20-30 hours of training**

---

## 💡 Key Insights

### Why C++?
- **Speed**: 10-100x faster than Python
- **Memory efficiency**: Critical for neural network
- **Production-ready**: Can be deployed anywhere
- **Real-time**: Suitable for interactive play

### Why Stockfish Training?
- **High-quality data**: Proven chess knowledge
- **Blunder injection**: Realistic scenarios
- **Measurable improvement**: Clear ELO gains
- **Reproducible**: Same data, same results

### Why 5% Blunders?
- **Realistic**: Humans make mistakes
- **Learning opportunity**: AI learns to punish
- **Robustness**: Handles imperfect opponents
- **Competitive**: More interesting games

---

Ready to build Chessy 1.6? Let's start! 🚀♟️
