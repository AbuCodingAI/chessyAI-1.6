# Chessy 1.0 - Backup

**Date:** November 9, 2025
**Status:** First working version with self-play training

## What's in this backup

### Core Files
- `chess_ai_server.py` - Flask server with neural network evaluation
- `Chessy1-0.html` - Web interface
- `Chessy1-0.js` - Frontend logic
- `Chessy1-0.css` - Styling

### Training Scripts
- `train_chess_ai.py` - Basic training (random positions + material eval)
- `self_play_training.py` - Self-play with game review
- `advanced_self_play.py` - MCTS-based advanced training

### Models
- `chess_model_basic.h5` - Initial trained model
- `chess_model_selfplay_*.h5` - Self-play checkpoints (if generated)

## Training Results

### Initial Training (Without Stockfish)
- Training positions: 10,000
- Method: Random positions with enhanced material evaluation
- Final loss: 0.0018
- Final MAE: 0.0311
- Validation loss: 0.0037
- Validation MAE: 0.0435

### Self-Play Training
- Started: November 9, 2025
- Games played: In progress...
- Method: AI vs AI with game review

## Estimated Strength
- Initial model: ~800-1000 ELO
- After self-play: ~1200-1400 ELO (estimated)

## How to Use This Backup

1. Copy files back to `neural-ai/` folder
2. Run server: `python chess_ai_server.py`
3. Open `Chessy1-0.html` in browser
4. Continue training: `python self_play_training.py`

## Next Version (Chessy 1.1)
- Will use Magnus Carlsen games for training
- Expected strength: ~1500-1800 ELO
- Better opening knowledge
- Improved tactical awareness
