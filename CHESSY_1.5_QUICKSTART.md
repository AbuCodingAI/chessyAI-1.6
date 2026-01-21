# Chessy 1.5 Quick Start Guide

## 🚀 One-Click Training

```bash
START_CHESSY_1.5_FULL_TRAINING.bat
```

That's it! The script will:
1. ✅ Generate training data (Stockfish vs Stockfish)
2. ✅ Train neural network
3. ✅ Test with self-play (40 games)
4. ✅ Test vs Stockfish (60 games)
5. ✅ Calculate ELO rating

**Time:** 4-6 hours  
**Output:** Trained model + ELO rating

---

## 📊 View Results

```bash
cd neural-ai
python view_chessy_1.5_results.py
```

Shows:
- Self-play statistics
- vs Stockfish win rate
- Estimated ELO
- Comparison with previous versions

---

## 🎯 What Makes Chessy 1.5 Special?

### Training Method
1. **Stockfish generates data** (100 games)
   - High-quality positions
   - Clean evaluations (depth 25)
   - ~5000 training examples

2. **Neural network learns** (50 epochs)
   - Learns from Stockfish's knowledge
   - Fast convergence
   - Strong baseline

3. **Self-play improvement** (40 games)
   - Adapts to own style
   - Discovers new strategies
   - Refines evaluation

4. **Rigorous testing** (60 games vs Stockfish)
   - Measures true strength
   - Calculates accurate ELO
   - Validates improvements

### Expected Performance
- **Target ELO:** 2400-2600 (IM to GM level)
- **vs Stockfish depth 10:** 40-50% win rate
- **Improvement:** Should match or exceed Chessy 1.4 (2700 ELO)

---

## 📁 Files Created

After training completes:

```
training_data/stockfish_positions.json  ← Training dataset
models/chessy_1.5_model.h5              ← Trained model
results/chessy_1.5_results.json         ← Test results
```

---

## ⚡ Quick Commands

### Generate data only:
```bash
cd neural-ai
python GENERATE_TRAINING_DATA_STOCKFISH.py
```

### Train only:
```bash
cd neural-ai
python TRAIN_CHESSY_1.5_FROM_STOCKFISH.py
```

### Test only:
```bash
cd neural-ai
python TRAIN_CHESSY_1.5_SELF_PLAY.py
```

---

## 🎮 Play Against Chessy 1.5

After training, add to `simple-ai.js`:

```javascript
case 'chessy15':
    return await this.chessy15(fen);
```

And implement:
```javascript
async chessy15(fen) {
    // TODO: Integrate neural-ai/models/chessy_1.5_model.h5
    // For now, use Stockfish depth 25 as placeholder
    return await this.stockfishMove(fen, 25);
}
```

---

## 🔧 Troubleshooting

**"Stockfish not found"**
- Check: `stockfish/stockfish-windows-x86-64-avx2.exe` exists

**"Out of memory"**
- Reduce games: Edit `NUM_GAMES = 50` in scripts

**"Too slow"**
- Reduce epochs: Edit `EPOCHS = 20` in training script

---

## 📈 Success Metrics

After training, check:
- ✅ **ELO > 2400:** Success! Deploy as Chessy 1.5
- ⚠️ **ELO 2200-2400:** Good, but needs more training
- ❌ **ELO < 2200:** Retrain with more data

---

## 🏆 Version History

| Version | ELO | Method |
|---------|-----|--------|
| 1.0 | 1600 | Basic |
| 1.1 | 1800 | Enhanced |
| 1.2 | 2200 | Magnus |
| 1.3 | 2500 | Deep search |
| 1.4 | 2700 | Quiescence |
| **1.5** | **?** | **Stockfish + Self-play** |

**Goal:** Beat or match Chessy 1.4 (2700 ELO)
