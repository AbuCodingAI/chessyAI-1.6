# Chess AI Training Guide

## Why Your AI Needs Training

Your chess AI currently has **no real training data**. It's generating random positions and using simple material counting, which doesn't teach it:
- Chess strategy
- Positional understanding
- Tactical patterns
- Opening principles
- Endgame technique

## Training Methods (Best to Worst)

### 1. ⭐ Stockfish-Evaluated Positions (BEST)
**Quality: Excellent**

Download Stockfish and use it to evaluate positions:
```bash
# 1. Download Stockfish
# Visit: https://stockfishchess.org/download/
# Download for Windows and extract stockfish.exe

# 2. Update path in train_chess_ai.py
STOCKFISH_PATH = "path/to/stockfish.exe"

# 3. Run training
python train_chess_ai.py
```

This generates positions and gets expert evaluations from Stockfish (3500+ ELO engine).

### 2. 🎮 Lichess Game Database (GOOD)
**Quality: Good**

Use real games from strong players:
```python
# Download games from lichess.org
# The script includes a function for this
# Games are from real players (1500-2500 ELO)
```

### 3. 🎲 Random Positions (POOR)
**Quality: Limited**

Current method - generates random positions with material evaluation only.
- No strategic understanding
- No tactical patterns
- Just piece counting

## Quick Start Training

### Option A: With Stockfish (Recommended)

1. **Download Stockfish:**
   - Go to https://stockfishchess.org/download/
   - Download Windows version
   - Extract `stockfish.exe`

2. **Update the training script:**
   ```python
   # In train_chess_ai.py, line 18:
   STOCKFISH_PATH = "C:/path/to/stockfish.exe"
   ```

3. **Configure training:**
   ```python
   TRAINING_POSITIONS = 10000  # More = better (but slower)
   EPOCHS = 20
   MODEL_TYPE = "basic"  # or "deep" or "residual"
   ```

4. **Run training:**
   ```bash
   python train_chess_ai.py
   ```

5. **Wait:** 10,000 positions takes ~30-60 minutes

### Option B: Without Stockfish (Quick but Limited)

1. **Run training with defaults:**
   ```bash
   python train_chess_ai.py
   ```

2. **It will use random positions** (not ideal but works)

## Training Configuration

### Number of Positions
```python
TRAINING_POSITIONS = 10000  # Recommended: 10,000-50,000
```
- 1,000: Very fast, poor quality
- 10,000: Good balance (30-60 min)
- 50,000: Better quality (2-4 hours)
- 100,000+: Best quality (many hours)

### Model Types
```python
MODEL_TYPE = "basic"  # Fast, decent
MODEL_TYPE = "deep"   # Slower, stronger
MODEL_TYPE = "residual"  # Slowest, strongest
```

### Epochs
```python
EPOCHS = 20  # Usually 15-30 is good
```

## After Training

1. **Model file created:** `chess_model_basic.h5`
2. **Info file created:** `chess_model_basic_info.json`
3. **Start server:** `python chess_ai_server.py`
4. **Play:** Open `Chessy1-0.html`

## Expected Results

### With Stockfish Training (10,000 positions):
- ✅ Understands piece values
- ✅ Basic positional play
- ✅ Some tactical awareness
- ✅ ~1200-1400 ELO strength

### With Random Training (10,000 positions):
- ⚠️ Understands piece values
- ❌ Poor positional play
- ❌ No tactical awareness
- ⚠️ ~800-1000 ELO strength

### With More Training (50,000+ positions + Stockfish):
- ✅ Good positional understanding
- ✅ Tactical patterns
- ✅ Opening principles
- ✅ ~1400-1600 ELO strength

## Advanced: Using Real Game Databases

For even better results, download PGN databases:

```python
# 1. Download from lichess.org/api
# 2. Parse PGN files
# 3. Extract positions
# 4. Evaluate with Stockfish
```

## Troubleshooting

### "Stockfish not found"
- Check the path in `STOCKFISH_PATH`
- Make sure it's `stockfish.exe` not `stockfish`
- Use absolute path: `C:/Users/YourName/stockfish.exe`

### "Out of memory"
- Reduce `TRAINING_POSITIONS`
- Reduce `BATCH_SIZE`
- Use "basic" model instead of "deep"

### "Training is slow"
- Normal! 10,000 positions takes 30-60 minutes
- Use fewer positions for testing
- Upgrade to GPU for faster training

### "AI still plays poorly"
- Need more training data (50,000+ positions)
- Use Stockfish for evaluations
- Train for more epochs
- Try "deep" or "residual" model

## Next Steps

1. Train with Stockfish (best results)
2. Increase training positions gradually
3. Try different model types
4. Experiment with hyperparameters
5. Consider using real game databases

Good luck training your chess AI! 🎮♔
