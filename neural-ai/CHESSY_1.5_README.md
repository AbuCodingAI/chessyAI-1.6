# Chessy 1.5 - Self-Play & Stockfish Training

## Overview

Chessy 1.5 combines two powerful training approaches:
1. **Stockfish-generated data** - Learn from high-quality positions
2. **Self-play** - Improve through playing against itself
3. **Rigorous testing** - 60 games vs Stockfish to measure strength

## Training Pipeline

### Method 1: Full Pipeline (Recommended)
```bash
START_CHESSY_1.5_FULL_TRAINING.bat
```

This runs everything automatically:
- ✅ Generate 100 games of Stockfish vs Stockfish (with noise)
- ✅ Collect ~5000 positions with clean evaluations
- ✅ Train neural network (50 epochs)
- ✅ Self-play testing (40 games)
- ✅ Stockfish testing (60 games)
- ✅ Calculate ELO rating

**Time:** 4-6 hours

### Method 2: Step-by-Step

#### Step 1: Generate Training Data
```bash
cd neural-ai
python GENERATE_TRAINING_DATA_STOCKFISH.py
```

**What it does:**
- Stockfish (depth 20) plays against Stockfish (depth 20 + noise)
- Black side has 15% chance to play suboptimal moves
- All positions re-evaluated with Stockfish depth 25 for clean labels
- Saves to `training_data/stockfish_positions.json`

**Output:** ~5000 positions from 100 games

#### Step 2: Train Neural Network
```bash
python TRAIN_CHESSY_1.5_FROM_STOCKFISH.py
```

**What it does:**
- Loads Stockfish-generated positions
- Trains neural network (50 epochs)
- Uses early stopping and learning rate reduction
- Saves to `models/chessy_1.5_stockfish_model.h5`

**Time:** 30-60 minutes

#### Step 3: Self-Play & Testing
```bash
python TRAIN_CHESSY_1.5_SELF_PLAY.py
```

**What it does:**
- Self-play: 40 games (Chessy vs Chessy)
- Learns from self-play games
- Tests: 60 games vs Stockfish (depth 10 ≈ 2400 ELO)
- Calculates final ELO rating
- Saves to `results/chessy_1.5_results.json`

**Time:** 2-3 hours

#### Step 4: View Results
```bash
python view_chessy_1.5_results.py
```

## Key Features

### Stockfish Data Generation
- **Clean positions:** All positions evaluated at depth 25
- **Blunder injection:** 15% of Black's moves hang pieces (intentional mistakes)
- **Tactical training:** Teaches Chessy to punish opponent errors
- **High quality:** Positions from strong play (depth 20) with realistic mistakes
- **Large dataset:** ~85 positions per game × 100 games = ~8500 positions

### Neural Network Architecture
```
Input: 768 features (64 squares × 12 piece types)
  ↓
Dense(512) + BatchNorm + Dropout(0.3)
  ↓
Dense(256) + BatchNorm + Dropout(0.3)
  ↓
Dense(128) + BatchNorm + Dropout(0.2)
  ↓
Dense(64) + Dropout(0.2)
  ↓
Output: 1 (position evaluation -1 to 1)
```

### Testing Protocol
1. **Self-play (40 games):**
   - Tests consistency
   - Identifies weaknesses
   - Generates more training data

2. **vs Stockfish (60 games):**
   - Alternates colors (30 white, 30 black)
   - Stockfish depth 10 (≈ 2400 ELO)
   - Calculates win rate and ELO

## Expected Results

### Target Performance
- **ELO:** 2400-2600 (IM to GM level)
- **vs Stockfish depth 10:** 40-50% win rate
- **Improvement over 1.4:** +0 to +100 ELO

### Success Criteria
- ✅ **Excellent:** 50%+ win rate vs Stockfish
- ✅ **Good:** 40-50% win rate
- ⚠️ **Needs work:** <40% win rate

## Files Generated

```
neural-ai/
├── training_data/
│   └── stockfish_positions.json    # Training dataset
├── models/
│   ├── chessy_1.5_stockfish_model.h5  # Trained from Stockfish
│   └── chessy_1.5_model.h5            # After self-play
└── results/
    └── chessy_1.5_results.json     # Test results & ELO
```

## Backup

Chessy 1.4 backed up to:
```
backups/chessy-1.4/
├── chess_engine_quiescence.py
└── CHESSY_1.4_GM_PLAN.md
```

## Advantages of This Approach

### vs Pure Self-Play
- ✅ Starts with strong foundation (Stockfish knowledge)
- ✅ Faster convergence
- ✅ Avoids learning bad habits

### vs Pure Supervised Learning
- ✅ Adapts to own playing style
- ✅ Discovers novel strategies
- ✅ More robust

### Combined Approach
- ✅ Best of both worlds
- ✅ Strong baseline + self-improvement
- ✅ Rigorous testing protocol

## Troubleshooting

### "Stockfish not found"
- Check path in scripts: `STOCKFISH_PATH`
- Should point to: `../stockfish/stockfish-windows-x86-64-avx2.exe`

### "Out of memory"
- Reduce `BATCH_SIZE` in training script
- Reduce `NUM_GAMES` in data generation

### "Training too slow"
- Reduce `EPOCHS` (try 20-30)
- Reduce `CLEAN_DEPTH` (try 20 instead of 25)
- Use GPU if available

## Next Steps

After training completes:
1. View results: `python view_chessy_1.5_results.py`
2. Compare with previous versions
3. If ELO > 2700: Deploy as Chessy 1.5
4. If ELO < 2700: Retrain with more data or adjust architecture

## Version Comparison

| Version | ELO  | Method |
|---------|------|--------|
| Chessy 1.0 | 1600 | Basic NN |
| Chessy 1.1 | 1800 | Enhanced eval |
| Chessy 1.2 | 2200 | Magnus training |
| Chessy 1.3 | 2500 | Deep search |
| Chessy 1.4 | 2700 | Quiescence search |
| **Chessy 1.5** | **?** | **Stockfish + Self-play** |

Goal: 2400-2600 ELO (IM to GM level)
