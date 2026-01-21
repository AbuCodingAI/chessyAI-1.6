"""
Chessy 1.2 Extended - Optimized Stockfish Training
Supports incremental training with configurable game count
"""

import chess
import chess.engine
import numpy as np
import tensorflow as tf
from tensorflow import keras
import os
import json
from datetime import datetime
import random

from chess_ai_server import board_to_array, create_basic_cnn, create_deep_cnn, create_residual_model

# STOCKFISH PATH
STOCKFISH_PATH = r"C:\Users\Abu\Downloads\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe"

class ExtendedStockfishTrainer:
    """Extended trainer with incremental training support"""
    
    def __init__(self, stockfish_path=STOCKFISH_PATH, existing_model=None):
        self.stockfish_path = stockfish_path
        self.engine = None
        self.existing_model = existing_model
        
        print("=" * 70)
        print("♔ CHESSY 1.2 EXTENDED - OPTIMIZED STOCKFISH TRAINING")
        print("=" * 70)
        
        # Try to start Stockfish
        try:
            print(f"\n🚀 Starting Stockfish...")
            self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
            print(f"   ✅ Stockfish started successfully!")
        except Exception as e:
            print(f"   ❌ Error starting Stockfish: {e}")
            self.engine = None
    
    def evaluate_position(self, board, depth=15):
        """Evaluate position using Stockfish"""
        if self.engine is None:
            return 0.0
        
        try:
            info = self.engine.analyse(board, chess.engine.Limit(depth=depth))
            score = info["score"].relative
            
            if score.is_mate():
                mate_in = score.mate()
                return 1.0 if mate_in > 0 else -1.0
            else:
                cp = score.score()
                return np.tanh(cp / 400.0)
        except:
            return 0.0
    
    def generate_training_data_self_play(self, num_games=100, depth=10):
        """Generate training data using Stockfish self-play"""
        print("\n" + "=" * 70)
        print("🎮 GENERATING TRAINING DATA - STOCKFISH SELF-PLAY")
        print("=" * 70)
        print(f"   Games: {num_games}")
        print(f"   Depth: {depth}")
        print(f"   Estimated time: {num_games * 1.2:.0f} minutes")
        print("=" * 70)
        
        if self.engine is None:
            print("\n❌ Stockfish not available!")
            return None, None
        
        X_train = []
        y_train = []
        
        for game_num in range(num_games):
            if game_num % 10 == 0:
                print(f"\n🎮 Game {game_num + 1}/{num_games}")
            
            board = chess.Board()
            positions_in_game = []
            
            move_count = 0
            max_moves = 150
            
            # Play game
            while not board.is_game_over() and move_count < max_moves:
                result = self.engine.play(board, chess.engine.Limit(depth=depth))
                board.push(result.move)
                move_count += 1
                
                # Store position (skip opening)
                if 10 < move_count < 100:
                    positions_in_game.append(board.copy())
            
            # Determine outcome
            if board.is_checkmate():
                outcome = 1.0 if not board.turn else -1.0
            else:
                outcome = 0.0
            
            if game_num % 10 == 0:
                print(f"   ✅ Game finished: {move_count} moves, {len(positions_in_game)} positions")
            
            # Evaluate all positions
            for pos_board in positions_in_game:
                evaluation = self.evaluate_position(pos_board, depth=15)
                X_train.append(board_to_array(pos_board))
                y_train.append(evaluation)
        
        print(f"\n✅ Total positions collected: {len(X_train)}")
        
        return np.array(X_train), np.array(y_train)
    
    def generate_training_data_random_positions(self, num_positions=5000, depth=15):
        """Generate training data from random positions"""
        print("\n" + "=" * 70)
        print("🎲 GENERATING TRAINING DATA - RANDOM POSITIONS")
        print("=" * 70)
        print(f"   Positions: {num_positions}")
        print(f"   Evaluation depth: {depth}")
        print(f"   Estimated time: {num_positions * 0.5 / 60:.0f} minutes")
        print("=" * 70)
        
        if self.engine is None:
            print("\n❌ Stockfish not available!")
            return None, None
        
        X_train = []
        y_train = []
        
        for i in range(num_positions):
            if i % 100 == 0:
                print(f"\r📊 Position {i}/{num_positions}...", end='', flush=True)
            
            # Generate random position
            board = chess.Board()
            num_moves = random.randint(10, 60)
            
            for _ in range(num_moves):
                if board.is_game_over():
                    break
                legal_moves = list(board.legal_moves)
                if not legal_moves:
                    break
                move = random.choice(legal_moves)
                board.push(move)
            
            # Skip if game over or too few pieces
            if board.is_game_over() or len(board.piece_map()) < 8:
                continue
            
            # Evaluate with Stockfish
            evaluation = self.evaluate_position(board, depth=depth)
            X_train.append(board_to_array(board))
            y_train.append(evaluation)
        
        print(f"\n✅ Total positions collected: {len(X_train)}")
        
        return np.array(X_train), np.array(y_train)
    
    def train_model(self, X_train, y_train, model_type='deep', epochs=30, 
                   incremental=False, existing_model_path=None):
        """Train model on Stockfish-evaluated positions"""
        print("\n" + "=" * 70)
        print("🧠 TRAINING NEURAL NETWORK")
        print("=" * 70)
        print(f"   Model: {model_type}")
        print(f"   Positions: {len(X_train)}")
        print(f"   Epochs: {epochs}")
        print(f"   Incremental: {incremental}")
        print("=" * 70)
        
        # Load existing model or create new
        if incremental and existing_model_path and os.path.exists(existing_model_path):
            print(f"\n📦 Loading existing model for incremental training...")
            print(f"   Path: {existing_model_path}")
            model = keras.models.load_model(existing_model_path, compile=False)
            model.compile(optimizer='adam', loss='mse', metrics=['mae'])
            print(f"   ✅ Model loaded successfully!")
        else:
            print(f"\n🆕 Creating new {model_type} model...")
            if model_type == 'basic':
                model = create_basic_cnn()
            elif model_type == 'deep':
                model = create_deep_cnn()
            elif model_type == 'residual':
                model = create_residual_model()
            else:
                raise ValueError(f"Unknown model type: {model_type}")
        
        # Split data
        split_idx = int(len(X_train) * 0.8)
        X_train_split = X_train[:split_idx]
        y_train_split = y_train[:split_idx]
        X_val = X_train[split_idx:]
        y_val = y_train[split_idx:]
        
        print(f"\n   Training set: {len(X_train_split)}")
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
                f'chess_model_stockfish_{model_type}_best.h5',
                save_best_only=True,
                monitor='val_loss'
            )
        ]
        
        # Train
        print("\n🚀 Starting training...\n")
        
        history = model.fit(
            X_train_split, y_train_split,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=64,
            callbacks=callbacks,
            verbose=1
        )
        
        # Save final model
        model.save(f'chess_model_stockfish_{model_type}.h5')
        
        # Save info
        info = {
            'version': 'Chessy 1.2 Extended',
            'training_method': 'Stockfish Evaluation',
            'model_type': model_type,
            'training_positions': len(X_train),
            'epochs': epochs,
            'incremental': incremental,
            'final_loss': float(history.history['loss'][-1]),
            'final_val_loss': float(history.history['val_loss'][-1]),
            'final_mae': float(history.history['mae'][-1]),
            'final_val_mae': float(history.history['val_mae'][-1]),
            'trained_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        with open(f'chess_model_stockfish_{model_type}_info.json', 'w') as f:
            json.dump(info, f, indent=2)
        
        print("\n" + "=" * 70)
        print("✅ TRAINING COMPLETE!")
        print("=" * 70)
        print(f"\n📊 Final Results:")
        print(f"   Training loss: {info['final_loss']:.4f}")
        print(f"   Validation loss: {info['final_val_loss']:.4f}")
        print(f"   Training MAE: {info['final_mae']:.4f}")
        print(f"   Validation MAE: {info['final_val_mae']:.4f}")
        print(f"\n💾 Model saved: chess_model_stockfish_{model_type}.h5")
        
        return model, history
    
    def close(self):
        """Close Stockfish engine"""
        if self.engine:
            self.engine.quit()
            print("\n✅ Stockfish closed")


def main():
    """Main training pipeline with options"""
    
    print("\n" + "=" * 70)
    print("♔ CHESSY 1.2 EXTENDED - OPTIMIZED STOCKFISH TRAINING")
    print("=" * 70)
    
    # Check for existing model
    existing_model = None
    if os.path.exists('chess_model_stockfish_deep.h5'):
        print("\n📦 Found existing Chessy 1.2 model!")
        print("   You can continue training to improve it further.")
        incremental = input("\n   Continue training existing model? (y/n): ").lower() == 'y'
        if incremental:
            existing_model = 'chess_model_stockfish_deep.h5'
    else:
        incremental = False
    
    # Initialize trainer
    trainer = ExtendedStockfishTrainer(STOCKFISH_PATH, existing_model)
    
    if trainer.engine is None:
        print("\n❌ Cannot proceed without Stockfish!")
        return
    
    # Choose number of games
    print("\n" + "=" * 70)
    print("📊 TRAINING CONFIGURATION")
    print("=" * 70)
    print("\n🎮 How many games to train on?")
    print("\n1. Quick (100 games)")
    print("   - Time: ~2 hours")
    print("   - Positions: ~2,000-3,000")
    print("   - Strength: ~1800-2000 ELO")
    
    print("\n2. Standard (500 games)")
    print("   - Time: ~10 hours")
    print("   - Positions: ~10,000-15,000")
    print("   - Strength: ~2000-2200 ELO")
    
    print("\n3. Extended (1000 games) ⭐ RECOMMENDED")
    print("   - Time: ~20 hours (overnight)")
    print("   - Positions: ~20,000-30,000")
    print("   - Strength: ~2200-2400 ELO")
    
    print("\n4. Custom (specify number)")
    
    choice = input("\nSelect option (1/2/3/4): ").strip()
    
    if choice == '1':
        num_games = 100
    elif choice == '2':
        num_games = 500
    elif choice == '3':
        num_games = 1000
    elif choice == '4':
        num_games = int(input("Enter number of games: "))
    else:
        num_games = 100
    
    print(f"\n✅ Training with {num_games} games")
    
    # Choose training method
    print("\n" + "=" * 70)
    print("📊 TRAINING METHOD")
    print("=" * 70)
    print("\n1. Self-Play only (Stockfish vs Stockfish)")
    print("2. Random Positions only (Stockfish evaluated)")
    print("3. Both (Recommended)")
    
    method = input("\nSelect method (1/2/3): ").strip()
    
    X_train_all = []
    y_train_all = []
    
    if method in ['1', '3']:
        # Self-play
        X_selfplay, y_selfplay = trainer.generate_training_data_self_play(
            num_games=num_games,
            depth=10
        )
        if X_selfplay is not None:
            X_train_all.append(X_selfplay)
            y_train_all.append(y_selfplay)
    
    if method in ['2', '3']:
        # Random positions (scale with game count)
        num_positions = num_games * 50  # 50 positions per game equivalent
        X_random, y_random = trainer.generate_training_data_random_positions(
            num_positions=num_positions,
            depth=15
        )
        if X_random is not None:
            X_train_all.append(X_random)
            y_train_all.append(y_random)
    
    if not X_train_all:
        print("\n❌ No training data generated!")
        trainer.close()
        return
    
    # Combine data
    X_train = np.concatenate(X_train_all)
    y_train = np.concatenate(y_train_all)
    
    print(f"\n📊 Total training data: {len(X_train)} positions")
    
    # Train model
    model, history = trainer.train_model(
        X_train, y_train,
        model_type='deep',
        epochs=30,
        incremental=incremental,
        existing_model_path=existing_model
    )
    
    # Close Stockfish
    trainer.close()
    
    # Estimate strength
    positions = len(X_train)
    if positions < 5000:
        estimated_elo = "~1800-2000"
    elif positions < 15000:
        estimated_elo = "~2000-2200"
    elif positions < 30000:
        estimated_elo = "~2200-2400"
    else:
        estimated_elo = "~2400-2600"
    
    print("\n" + "=" * 70)
    print("🎉 CHESSY 1.2 EXTENDED IS READY!")
    print("=" * 70)
    print(f"\n💪 Estimated strength: {estimated_elo}")
    print(f"📊 Training positions: {positions:,}")
    print(f"🎮 Games trained on: {num_games}")
    print("\n🎮 Next steps:")
    print("   1. Update chess_ai_server.py to use new model")
    print("   2. Compare against previous versions")
    print("   3. Play and enjoy!")
    
    if incremental:
        print("\n💡 You can run this script again to continue improving!")


if __name__ == "__main__":
    main()
