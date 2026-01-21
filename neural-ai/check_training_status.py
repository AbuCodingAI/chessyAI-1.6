"""
Quick script to check what's training and their status
"""

import os
import json
from datetime import datetime

print("=" * 70)
print("♔ CHESSY TRAINING STATUS CHECK")
print("=" * 70)

# Check for model files
models = {
    'Chessy 1.0 Initial': 'chess_model_basic.h5',
    'Chessy 1.0 Self-Play Gen 25': 'chess_model_selfplay_gen25.h5',
    'Chessy 1.0 Self-Play Gen 50': 'chess_model_selfplay_gen50.h5',
    'Chessy 1.0 Self-Play Gen 75': 'chess_model_selfplay_gen75.h5',
    'Chessy 1.0 Self-Play Final': 'chess_model_selfplay_final.h5',
    'Chessy 1.1 Magnus': 'chess_model_magnus_basic.h5',
    'Chessy 1.2 Stockfish': 'chess_model_stockfish_deep.h5',
}

print("\n📦 MODEL FILES:")
print("-" * 70)

for name, filename in models.items():
    if os.path.exists(filename):
        size_mb = os.path.getsize(filename) / (1024 * 1024)
        mod_time = datetime.fromtimestamp(os.path.getmtime(filename))
        print(f"✅ {name}")
        print(f"   File: {filename}")
        print(f"   Size: {size_mb:.2f} MB")
        print(f"   M