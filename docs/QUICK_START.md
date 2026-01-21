# Chessy Quick Start Guide

Get up and running in 5 minutes!

---

## 🎮 Play Chess Now

1. Open `index.html` in your browser
2. Click "New Game"
3. Play!

**That's it!** No installation needed for basic chess.

---

## 🧠 Want AI Opponents?

### Option 1: Built-in AI (Easy)
Already works! Just select AI difficulty in the game.

### Option 2: Neural Network AI (Advanced)

**Quick Setup:**
```bash
cd neural-ai
pip install -r requirements.txt
python chess_ai_server.py
```

Open `neural-ai/Chessy1-0.html` and play!

**Full Guide:** [Neural AI Setup](neural-ai/NEURAL_AI_SETUP.md)

---

## 🎓 Train Your Own AI

### Currently Training (Check Status)
```bash
# See what's training right now
python neural-ai/training_monitor.py
```

**Status:** [Training Status](training/TRAINING_STATUS.md)

### Start New Training

**Chessy 1.0 - Self-Play**
```bash
python neural-ai/self_play_training.py
```
Time: 2-3 hours | Strength: ~1200-1400 ELO

**Chessy 1.1 - Magnus Games**
```bash
python neural-ai/train_magnus_games.py
```
Time: 30-60 min | Strength: ~1500-1800 ELO

**Chessy 1.2 - Stockfish** (Strongest!)
```bash
python neural-ai/train_chessy_1.2_stockfish.py
```
Time: 2-3 hours | Strength: ~1800-2200 ELO

**Full Guide:** [Training Guide](training/TRAINING_GUIDE.md)

---

## 📊 Compare Models

After training multiple versions:
```bash
python neural-ai/compare_models.py
```

See which AI is strongest!

---

## 🆘 Troubleshooting

### "Module not found"
```bash
pip install -r neural-ai/requirements.txt
```

### "Stockfish not found"
Update path in training script:
```python
STOCKFISH_PATH = r"C:\path\to\stockfish.exe"
```

### "Training is slow"
- Normal! Neural networks take time
- Check [Training Status](training/TRAINING_STATUS.md)
- Models save checkpoints automatically

### "AI plays poorly"
- Needs more training data
- Try Stockfish-powered training (Chessy 1.2)
- Or train on Magnus games (Chessy 1.1)

---

## 📚 More Help

- **Full Documentation:** [docs/README.md](README.md)
- **Quick Index:** [docs/INDEX.md](INDEX.md)
- **Training Status:** [training/TRAINING_STATUS.md](training/TRAINING_STATUS.md)
- **AI Features:** [AI_ENGINE.md](AI_ENGINE.md)

---

## 🎯 What's Training Right Now?

Check: [Training Status](training/TRAINING_STATUS.md)

Or run:
```bash
python neural-ai/training_monitor.py
```

---

**Need more help?** Check the [full documentation](README.md)!
