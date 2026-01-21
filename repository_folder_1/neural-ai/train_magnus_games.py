"""
Chessy 1.1 - Train on Magnus Carlsen Games
Download and train on real grandmaster games
"""

import chess
import chess.pgn
import numpy as np
import tensorflow as tf
from tensorflow import keras
import requests
import io
import os
import json
from datetime import datetime
from collections import defaultdict

from chess_ai_server import board_to_array, create_basic_cnn, create_deep_cnn

class MagnusGameTrainer:
    """Train on Magnus Carlsen games"""
    
    def __init__(self):
        self.games = []
        self.positions = []
        self.labels = []
        
    def download_magnus_games_lichess(self, max_games=500):
        """
        Download Magnus Carlsen games from Lichess
        Username: DrNykterstein (Magnus's lichess account)
        """
        print("=" * 70)
        print("♔ DOWNLOADING MAGNUS CARLSEN GAMES")
        print("=" * 70)
        
        username = "DrNykterstein"  # Magnus on Lichess
        
        print(f"\n📥 Downloading games from lichess.org/@/{username}")
        print(f"   Target: {max_games} games")
        print(f"   This may take a few minutes...\n")
        
        # Lichess API endpoint
        url = f"https://lichess.org/api/games/user/{username}"
        
        params = {
            'max': max_games,
            'rated': 'true',
            'perfType': 'blitz,rapid,classical',  # Exclude bullet for quality
            'opening': 'true',
            'clocks': 'false',
            'evals': 'false',
            'pgnInJson': 'false'
        }
        
        headers = {
            'Accept': 'application/x-chess-pgn'
        }
        
        try:
            response = requests.get(url, params=params, headers=headers, stream=True)
            
            if response.status_code == 200:
                pgn_text = response.text
                print(f"✅ Downloaded successfully!")
                return pgn_text
            else:
                print(f"❌ Error: HTTP {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error downloading: {e}")
            return None
    
    def parse_pgn_games(self, pgn_text):
        """Parse PGN text into game objects"""
        print("\n📖 Parsing PGN games...")
        
        games = []
        pgn_io = io.StringIO(pgn_text)
        
        game_count = 0
        while True:
            game = chess.pgn.read_game(pgn_io)
            if game is None:
                break
            
            games.append(game)
            game_count += 1
            
            if game_count % 50 == 0:
                print(f"   Parsed {game_count} games...")
        
        print(f"✅ Parsed {len(games)} games total")
        self.games = games
        return games
    
    def extract_positions_from_games(self, min_moves=10, max_moves=80):
        """
        Extract positions from games with outcome labels
        """
        print("\n🎯 Extracting positions from games...")
        print(f"   Filtering: {min_moves}-{max_moves} moves per game")
        
        positions = []
        labels = []
        
        stats = defaultdict(int)
        
        for game_idx, game in enumerate(self.games):
            if game_idx % 50 == 0:
                print(f"   Processing game {game_idx}/{len(self.games)}...")
            
            # Get game result
            result = game.headers.get('Result', '*')
            
            if result == '1-0':
                outcome = 1.0  # White wins
            elif result == '0-1':
                outcome = -1.0  # Black wins
            elif result == '1/2-1/2':
                outcome = 0.0  # Draw
            else:
                continue  # Skip unfinished games
            
            stats[result] += 1
            
            # Get Magnus's color
            white_player = game.headers.get('White', '')
            black_player = game.headers.get('Black', '')
            
            magnus_is_white = 'DrNykterstein' in white_player or 'Carlsen' in white_player
            magnus_is_black = 'DrNykterstein' in black_player or 'Carlsen' in black_player
            
            # Extract positions
            board = game.board()
            move_count = 0
            
            for move in game.mainline_moves():
                board.push(move)
                move_count += 1
                
                # Skip opening (first 10 moves) and very long games
                if move_count < min_moves or move_count > max_moves:
                    continue
                
                # Skip positions with too few pieces (endgame)
                if len(board.piece_map()) < 10:
                    continue
                
                # Store position
                board_array = board_to_array(board)
                
                # Adjust outcome based on whose turn it is
                # We want evaluation from current player's perspective
                position_value = outcome
                if board.turn == chess.BLACK:
                    position_value = -outcome
                
                # Discount value based on how far from end
                moves_from_end = max_moves - move_count
                discount = 0.95 ** (moves_from_end / 10)
                position_value *= discount
                
                positions.append(board_array)
                labels.append(position_value)
        
        print(f"\n✅ Extracted {len(positions)} positions")
        print(f"\n📊 Game outcomes:")
        print(f"   White wins: {stats['1-0']}")
        print(f"   Black wins: {stats['0-1']}")
        print(f"   Draws: {stats['1/2-1/2']}")
        
        self.positions = np.array(positions)
        self.labels = np.array(labels)
        
        return self.positions, self.labels
    
    def train_model(self, model_type='basic', epochs=30, batch_size=64):
        """Train model on Magnus games"""
        print("\n" + "=" * 70)
        print("🧠 TRAINING ON MAGNUS CARLSEN GAMES")
        print("=" * 70)
        
        if len(self.positions) == 0:
            print("❌ No training data! Run extract_positions_from_games first.")
            return None
        
        print(f"\n📊 Training Configuration:")
        print(f"   Model: {model_type}")
        print(f"   Positions: {len(self.positions)}")
        print(f"   Epochs: {epochs}")
        print(f"   Batch size: {batch_size}")
        
        # Create model
        if model_type == 'basic':
            model = create_basic_cnn()
        elif model_type == 'deep':
            model = create_deep_cnn()
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        # Split data
        split_idx = int(len(self.positions) * 0.8)
        X_train = self.positions[:split_idx]
        y_train = self.labels[:split_idx]
        X_val = self.positions[split_idx:]
        y_val = self.labels[split_idx:]
        
        print(f"\n   Training set: {len(X_train)}")
        print(f"   Validation set: {len(X_val)}")
        
        # Callbacks
        callbacks = [
            keras.callbacks.EarlyStopping(
                patience=5,
                restore_best_weights=True,
                monitor='val_loss'
            ),
            keras.callbacks.ReduceLROnPlateau(
                factor=0.5,
                patience=3,
                monitor='val_loss'
            ),
            keras.callbacks.ModelCheckpoint(
                f'chess_model_magnus_{model_type}_best.h5',
                save_best_only=True,
                monitor='val_loss'
            )
        ]
        
        # Train
        print("\n🚀 Starting training...\n")
        
        history = model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=1
        )
        
        # Save final model
        model.save(f'chess_model_magnus_{model_type}.h5')
        
        # Save info
        info = {
            'version': 'Chessy 1.1',
            'training_method': 'Magnus Carlsen Games',
            'model_type': model_type,
            'training_positions': len(self.positions),
            'games_used': len(self.games),
            'epochs': epochs,
            'final_loss': float(history.history['loss'][-1]),
            'final_val_loss': float(history.history['val_loss'][-1]),
            'final_mae': float(history.history['mae'][-1]),
            'final_val_mae': float(history.history['val_mae'][-1]),
            'trained_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        with open(f'chess_model_magnus_{model_type}_info.json', 'w') as f:
            json.dump(info, f, indent=2)
        
        print("\n" + "=" * 70)
        print("✅ TRAINING COMPLETE!")
        print("=" * 70)
        print(f"\n📊 Final Results:")
        print(f"   Training loss: {info['final_loss']:.4f}")
        print(f"   Validation loss: {info['final_val_loss']:.4f}")
        print(f"   Training MAE: {info['final_mae']:.4f}")
        print(f"   Validation MAE: {info['final_val_mae']:.4f}")
        print(f"\n💾 Model saved: chess_model_magnus_{model_type}.h5")
        print(f"💾 Info saved: chess_model_magnus_{model_type}_info.json")
        
        return model, history


def main():
    """Main training pipeline"""
    
    print("=" * 70)
    print("♔ CHESSY 1.1 - MAGNUS CARLSEN EDITION")
    print("=" * 70)
    print("\nTraining on real grandmaster games for superior play!\n")
    
    trainer = MagnusGameTrainer()
    
    # Step 1: Download games
    pgn_text = trainer.download_magnus_games_lichess(max_games=500)
    
    if pgn_text is None:
        print("\n❌ Could not download games. Check your internet connection.")
        print("\n💡 Alternative: Download PGN manually from:")
        print("   https://lichess.org/@/DrNykterstein")
        print("   Save as 'magnus_games.pgn' and modify script to load it.")
        return
    
    # Step 2: Parse games
    games = trainer.parse_pgn_games(pgn_text)
    
    if len(games) == 0:
        print("\n❌ No games parsed!")
        return
    
    # Step 3: Extract positions
    positions, labels = trainer.extract_positions_from_games(
        min_moves=10,
        max_moves=80
    )
    
    if len(positions) == 0:
        print("\n❌ No positions extracted!")
        return
    
    # Step 4: Train model
    model, history = trainer.train_model(
        model_type='basic',  # or 'deep' for stronger model
        epochs=30,
        batch_size=64
    )
    
    print("\n" + "=" * 70)
    print("🎉 CHESSY 1.1 IS READY!")
    print("=" * 70)
    print("\n🎮 Next steps:")
    print("   1. Update chess_ai_server.py to use new model")
    print("   2. Start server: python chess_ai_server.py")
    print("   3. Play against Magnus-trained AI!")
    print("\n💪 Expected strength: ~1500-1800 ELO")


if __name__ == "__main__":
    main()
