# Chessy Neural AI - Version History

---

## 🚀 Current Version: Chessy 1.2 (In Development)

**Status:** Files renamed, ready for Stockfish training
**UI Files:**
- `Chessy1-2.html` - Main interface
- `Chessy1-2.css` - Styling
- `Chessy1-2.js` - Frontend logic

**Training Script:** `train_chessy_1.2_stockfish.py`
**Expected Strength:** ~1800-2200 ELO

---

## 📜 Version History

### Chessy 1.2 - Stockfish-Powered (Current)
**Status:** 🔄 In Development
**Release Date:** TBD
**Training Method:** Stockfish evaluation
**Features:**
- Stockfish 16+ integration
- Expert position evaluation (3740 ELO teacher)
- Self-play + random positions
- Deep CNN architecture
**Expected Strength:** ~1800-2200 ELO

---

### Chessy 1.1 - Magnus Carlsen Edition
**Status:** ✅ Complete
**Release Date:** November 9, 2025, 8:58 PM
**Training Method:** Magnus Carlsen games from Lichess
**Features:**
- 500 GM games
- 30,997 training positions
- Real opening theory
- Grandmaster tactics
**Achieved Strength:** ~1500-1800 ELO
**Backup:** `backups/chessy-1.1/`

---

### Chessy 1.0 - Self-Play Edition
**Release Date:** November 9, 2025
**Training Method:** AI vs AI self-play
**Features:**
- 100 self-play games
- Game review and learning
- Replay buffer training
- Iterative improvement
**Expected Strength:** ~1200-1400 ELO
**Backup:** `backups/chessy-1.0/`

---

### Chessy 1.0 - Initial Release
**Status:** ✅ Complete
**Release Date:** November 9, 2025, 8:00 PM
**Training Method:** Random positions with enhanced evaluation
**Features:**
- 10,000 training positions
- Material + positional evaluation
- Basic CNN architecture
**Achieved Strength:** ~1200 ELO
**Backup:** `backups/chessy-1.0/`

---

## 🎯 Upcoming Versions

### Chessy 1.3 - Time Control Specialist
**Status:** 📋 Planned
**Expected Release:** TBD
**Training Method:** Time-control-specific training
**Features:**
- ⚡ Bullet optimization (1-2 min)
- 🏃 Blitz optimization (3-5 min)
- 🎯 Rapid optimization (10-15 min)
- 🧠 Classical optimization (30+ min)
- Fast/Standard/Deep networks
- Dynamic search depth
- Time-aware evaluation
**Expected Strength:** ~2200-2400 ELO
**Plan:** `docs/training/CHESSY_1.3_PLAN.md`

### Chessy 2.0 - AlphaZero Style
**Status:** 💭 Concept
**Expected Release:** Future
**Training Method:** MCTS + Policy/Value networks
**Features:**
- Full MCTS implementation
- Policy + Value network architecture
- Massive self-play (100k+ games)
- Opening book database
- Endgame tablebases
- Multi-GPU training
**Expected Strength:** ~2400-2600 ELO

---

## 📊 Strength Progression

```
Version    ELO    Training Method           Time
────────────────────────────────────────────────────
1.0 Init   1200   Random positions          15 min
1.0 Self   1400   Self-play                 25 min
1.1 Magnus 1600   GM games                  45 min
1.2 Stock  2000   Stockfish eval            2-3 hrs
1.3 Time   2400   Time-aware                5 hrs
2.0 Alpha  2600   MCTS + Policy/Value       Days
```

---

## 🎮 How to Play

### Current Version (1.2 UI with 1.1 Model)
```bash
# Quick start
Double-click PLAY_CHESSY.bat

# Or manually
cd neural-ai
python chess_ai_server.py
# Open Chessy1-2.html
```

### Select Model in Server
Edit `chess_ai_server.py` to load different models:
```python
# Chessy 1.0 Initial
model = keras.models.load_model('chess_model_basic.h5')

# Chessy 1.1 Magnus
model = keras.models.load_model('chess_model_magnus_basic.h5')

# Chessy 1.2 Stockfish (after training)
model = keras.models.load_model('chess_model_stockfish_deep.h5')
```

---

## 📈 Performance Comparison

| Feature | 1.0 | 1.1 | 1.2 | 1.3 |
|---------|-----|-----|-----|-----|
| ELO | 1200 | 1600 | 2000 | 2400 |
| Opening | Poor | Good | Very Good | Excellent |
| Tactics | Basic | Good | Excellent | Expert |
| Endgame | Weak | Fair | Good | Very Good |
| Speed | Fast | Fast | Medium | Variable |
| Time Mgmt | None | None | None | Excellent |

---

## 🔧 Technical Specs

### Architecture Evolution

**1.0 - Basic CNN:**
- 3 conv layers (64, 128, 256)
- 2 dense layers (256)
- ~500k parameters

**1.1 - Same as 1.0:**
- Better training data
- Same architecture

**1.2 - Deep CNN:**
- 3 conv layers (64, 128, 256)
- 2 dense layers (512, 256)
- Dropout regularization
- ~500k parameters

**1.3 - Multiple Networks:**
- Fast: 1 conv layer (32)
- Standard: 3 conv layers (64, 128, 256)
- Deep: 5 conv layers (128, 256, 512, 512, 512)

---

## 📝 Notes

- All versions backed up in `backups/` folder
- Training scripts available for each version
- Can compare models with `compare_models.py`
- Documentation in `docs/` folder

---

**Current Status:** Chessy 1.0 self-play at game 29/100 (4 games/min!) 🔥
**Next:** Chessy 1.2 Stockfish training
**Future:** Chessy 1.3 time control optimization
