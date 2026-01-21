# Chessy 1.2 Training Guide

Complete guide for training Chessy 1.2 with Stockfish.

---

## Prerequisites

✅ Stockfish downloaded and path configured
✅ Chessy 1.0 and 1.1 backed up
✅ Python environment ready
✅ 2-3 hours available for training

---

## Step-by-Step Training

### Step 1: Verify Setup

**Check Stockfish:**
```bash
# Test if Stockfish works
C:\Users\Abu\Downloads\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe
```

Should open Stockfish console. Type `quit` to exit.

**Check Python packages:**
```bash
pip list | findstr "tensorflow chess"
```

Should show tensorflow and python-chess installed.

### Step 2: Start Training

```bash
cd neural-ai
python train_chessy_1.2_stockfish.py
```

### Step 3: Choose Training Method

You'll see:
```
1. Self-Play (Stockfish vs Stockfish)
2. Random Positions (Stockfish evaluated)
3. Both (Recommended)

Select method (1/2/3):
```

**Recommendation:** Choose `3` for best results

### Step 4: Monitor Progress

Training will show:
```
🎮 Playing game 1/100
   Move 20...
   Move 40...
   ✅ Game finished: Checkmate after 45 moves
   📊 Positions collected: 35

🎮 Playing game 2/100
   ...
```

### Step 5: Wait for Completion

**Timeline:**
- Self-play: ~1-2 hours (100 games)
- Random positions: ~30-60 min (5000 positions)
- Neural network training: ~30 min
- **Total: ~2-3 hours**

### Step 6: Review Results

After training completes:
```
✅ TRAINING COMPLETE!

📊 Final Results:
   Training loss: 0.0234
   Validation loss: 0.0289
   Training MAE: 0.1123
   Validation MAE: 0.1456

💾 Model saved: chess_model_stockfish_deep.h5
```

---

## Training Options Explained

### Option 1: Self-Play Only
**Pros:**
- High-quality game positions
- Natural position distribution
- Learns from complete games

**Cons:**
- Slower (1-2 hours)
- Fewer total positions (~2000-3000)

**Best for:** Learning game flow and strategy

### Option 2: Random Positions Only
**Pros:**
- Faster (30-60 min)
- More positions (5000)
- Diverse position types

**Cons:**
- Less natural positions
- No game context

**Best for:** Quick training, broad coverage

### Option 3: Both (Recommended)
**Pros:**
- Best of both worlds
- Maximum training quality
- Diverse + natural positions

**Cons:**
- Longest time (2-3 hours)

**Best for:** Maximum strength

---

## What to Expect During Training

### Phase 1: Data Generation (1-2 hours)
```
📥 Generating training data...
🎮 Playing game 1/100
🎮 Playing game 2/100
...
🎲 Generating random positions...
📊 Position 100/5000
...
✅ Total positions collected: 7000
```

### Phase 2: Neural Network Training (30 min)
```
🧠 Training neural network...
Epoch 1/30
████████████████ 100% - loss: 0.234 - val_loss: 0.289
Epoch 2/30
████████████████ 100% - loss: 0.156 - val_loss: 0.198
...
```

### Phase 3: Completion
```
✅ TRAINING COMPLETE!
💾 Model saved
📊 Results logged
```

---

## Monitoring Training

### In Same Terminal
Watch the output - it updates automatically

### In Another Terminal
```bash
python training_monitor.py
```

Shows real-time status of all training sessions.

### Check Files
```bash
dir *.h5
```

Shows created model files and their sizes.

---

## Troubleshooting

### Training Stops Unexpectedly

**Check:**
1. Stockfish still running? (Task Manager)
2. Enough disk space? (Need ~500MB)
3. Python still running? (Check terminal)

**Solution:**
- Training saves checkpoints
- Can resume from last checkpoint
- Or restart training (won't lose everything)

### "Stockfish not responding"

**Symptoms:**
- Training hangs
- No progress updates
- CPU usage drops to 0%

**Solution:**
```bash
# Kill Stockfish processes
taskkill /F /IM stockfish*.exe

# Restart training
python train_chessy_1.2_stockfish.py
```

### "Out of memory"

**Symptoms:**
- Python crashes
- "MemoryError" message

**Solution:**
1. Close other applications
2. Reduce training positions:
   ```python
   # In train_chessy_1.2_stockfish.py
   num_games=50  # Instead of 100
   num_positions=2500  # Instead of 5000
   ```
3. Use 'basic' model instead of 'deep'

### Training is Very Slow

**Normal speeds:**
- Self-play: 1-2 minutes per game
- Random positions: 1-2 seconds per position

**If slower:**
- Check CPU usage (should be 80-100%)
- Close background applications
- Check Stockfish depth setting (lower = faster)

---

## After Training Completes

### 1. Verify Model Created
```bash
dir chess_model_stockfish_deep.h5
```

Should show file size ~10-20 MB.

### 2. Check Training Info
```bash
type chess_model_stockfish_deep_info.json
```

Shows training statistics.

### 3. Compare Models
```bash
python compare_models.py
```

Plays Chessy 1.2 vs 1.1 vs 1.0.

### 4. Update Server
Edit `chess_ai_server.py`:
```python
# Around line 200, change:
model = keras.models.load_model('chess_model_stockfish_deep.h5')
```

### 5. Test It!
```bash
python chess_ai_server.py
```

Open `Chessy1-0.html` and play!

---

## Expected Performance

### Strength Comparison
| Version | ELO | Training Time | Quality |
|---------|-----|---------------|---------|
| 1.0 | 1200 | 2-3 hours | Good |
| 1.1 | 1600 | 30-60 min | Very Good |
| 1.2 | 2000 | 2-3 hours | Excellent |

### Win Rates (Expected)
- Chessy 1.2 vs 1.1: ~70-80% wins
- Chessy 1.2 vs 1.0: ~90-95% wins
- Chessy 1.2 vs Average Player: ~99% wins

---

## Tips for Best Results

### 1. Use Option 3 (Both Methods)
Combines self-play and random positions for maximum quality.

### 2. Let It Run Overnight
2-3 hours is a long time. Start before bed!

### 3. Don't Interrupt Training
Let it complete fully for best results.

### 4. Save Checkpoints
Training saves automatically every epoch.

### 5. Compare Results
Use `compare_models.py` to verify improvement.

---

## Ready to Start?

```bash
cd neural-ai
python train_chessy_1.2_stockfish.py
```

**Choose option 3 when prompted!**

Good luck! 🚀
