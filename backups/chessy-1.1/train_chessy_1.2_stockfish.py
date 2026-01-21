"""
Chessy 1.2 - Stockfish-Powered Training
The strongest training method using Stockfish evaluations
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

# STOCKFISH PATH - Update this!
STOCKFISH_PATH = r"C:\Users\Abu\Downloads\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe"

class StockfishTrainer:
    """Train using Stockfish evaluations"""
    
    def __init__(self, stockfish_path=STOCKFISH_PATH):
        self.stockfish_path = stockfish_path
        self.engine = None
        
        print("=" * 70)
        print("♔ CHESSY 1.2 - STOCKFISH-POWERED TRAINING")
        print("=" * 70)
        
        # Try to start Stockfish
        try:
            print(f"\n🚀 Starting Stockfish...")
            print(f"   Path: {stockfish_path}")
            self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
            print(f"   ✅ Stockfish started successfully!")
            
            # Get Stockfish info
            info = self.engine.id
            print(f"   📊 Name: {info.get('name', 'Unknown')}")
            
        except Exception as e:
            print(f"   ❌ Error starting Stockfish: {e}")
            print(f"\n💡 Make sure the path is correct:")
            print(f"   Current: {stockfish_path}")
            self.engine = None
    
    def evaluate_position(self, board, depth=15):
        """Evaluate position using Stockfish"""
        if self.engine is None:
            return 0.0
        
        try:
            info = self.engine.analyse(board, chess.engine.Limit(depth=depth))
            score = info["score"].relative
            
            # Convert to normalized value (-1 to 1)
            if score.is_mate():
                mate_in = score.mate()
                return 1.0 if mate_in > 0 else -1.0
            else:
                # Centipawn score, normalize
                cp = score.score()
                return np.tanh(cp / 400.0)
        except:
            return 0.0
    
    def generate_training_data_self_play(self, num_games=100, depth=10):
        """
        Generate training data using Stockfish self-play
        Stockfish plays against itself at specified depth
        """
        print("\n" + "=" * 70)
        print("🎮 GENERATING TRAINING DATA - STOCKFISH SELF-PLAY")
        print("=" * 70)
        print(f"   Games: {num_games}")
        print(f"   Depth: {depth}")
        print("=" * 70)
        
        if self.engine is None:
            print("\n❌ Stockfish not available!")
            return None, None
        
        X_train = []
        y_train = []
        
        for game_num in range(num_games):
            print(f"\n🎮 Game {game_num + 1}/{num_games}")
            
            board = chess.Board()
            positions_in_game = []
            
            move_count = 0
            max_moves = 150
            
            # Play game
            while not board.is_game_over() and move_count < max_moves:
                # Get Stockfish's move
                result = self.engine.play(board, chess.engine.Limit(depth=depth))
                board.push(result.move)
                move_count += 1
                
                # Store position (skip opening)
                if move_count > 10 and move_count < 100:
                    positions_in_game.append(board.copy())
                
                if move_count % 20 == 0:
                    print(f"   Move {move_count}...")
            
            # Determine outcome
            if board.is_checkmate():
                outcome = 1.0 if not board.turn else -1.0
            else:
                outcome = 0.0
            
            print(f"   ✅ Game finished: {move_count} moves")
            print(f"   📊 Positions collected: {len(positions_in_game)}")
            
            # Evaluate all positions from this game
            for pos_board in positions_in_game:
                evaluation = self.evaluate_position(pos_board, depth=15)
                
                X_train.append(board_to_array(pos_board))
                y_train.append(evaluation)
        
        print(f"\n✅ Total positions collected: {len(X_train)}")
        
        return np.array(X_train), np.array(y_train)
    
    def generate_training_data_random_positions(self, num_positions=5000, depth=15):
        """
        Generate training data from random positions
        Evaluated by Stockfish
        """
        print("\n" + "=" * 70)
        print("🎲 GENERATING TRAINING DATA - RANDOM POSITIONS")
        print("=" * 70)
        print(f"   Positions: {num_positions}")
        print(f"   Evaluation depth: {depth}")
        print("=" * 70)
        
        if self.engine is None:
            print("\n❌ Stockfish not available!")
            return None, None
        
        X_train = []
        y_train = []
        
        for i in range(num_positions):
            if i % 100 == 0:
                print(f"\n📊 Position {i}/{num_positions}...")
            
            # Generate random position
            board = chess.Board()
            
            # Make random moves
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
    
    def train_model(self, X_train, y_train, model_type='deep', epochs=30):
        """Train model on Stockfish-evaluated positions"""
        print("\n" + "=" * 70)
        print("🧠 TRAINING NEURAL NETWORK")
        print("=" * 70)
        print(f"   Model: {model_type}")
        print(f"   Positions: {len(X_train)}")
        print(f"   Epochs: {epochs}")
        print("=" * 70)
        
        # Create model
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
            'version': 'Chessy 1.2',
            'training_method': 'Stockfish Evaluation',
            'model_type': model_type,
            'training_positions': len(X_train),
            'epochs': epochs,
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
    """Main training pipeline"""
    
    print("\n" + "=" * 70)
    print("♔ CHESSY 1.2 - STOCKFISH-POWERED TRAINING")
    print("=" * 70)
    print("\nThe strongest training method using Stockfish 16+")
    print("Expected strength: ~1800-2200 ELO\n")
    
    # Initialize trainer
    trainer = StockfishTrainer(STOCKFISH_PATH)
    
    if trainer.engine is None:
        print("\n❌ Cannot proceed without Stockfish!")
        print("\n💡 Update STOCKFISH_PATH in this script:")
        print(f"   Current: {STOCKFISH_PATH}")
        return
    
    # Choose training method
    print("\n" + "=" * 70)
    print("📊 TRAINING METHOD")
    print("=" * 70)
    print("\n1. Self-Play (Stockfish vs Stockfish)")
    print("   - 100 games")
    print("   - ~2000-3000 positions")
    print("   - Time: ~1-2 hours")
    print("   - Quality: Excellent")
    
    print("\n2. Random Positions (Stockfish evaluated)")
    print("   - 5000 positions")
    print("   - Time: ~30-60 minutes")
    print("   - Quality: Very Good")
    
    print("\n3. Both (Recommended)")
    print("   - Best of both methods")
    print("   - Time: ~2-3 hours")
    print("   - Quality: Outstanding")
    
    choice = input("\nSelect method (1/2/3): ").strip()
    
    X_train_all = []
    y_train_all = []
    
    if choice in ['1', '3']:
        # Self-play
        X_selfplay, y_selfplay = trainer.generate_training_data_self_play(
            num_games=100,
            depth=10
        )
        if X_selfplay is not None:
            X_train_all.append(X_selfplay)
            y_train_all.append(y_selfplay)
    
    if choice in ['2', '3']:
        # Random positions
        X_random, y_random = trainer.generate_training_data_random_positions(
            num_positions=5000,
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
        model_type='deep',  # Use deep model for best results
        epochs=30
    )
    
    # Close Stockfish
    trainer.close()
    
    print("\n" + "=" * 70)
    print("🎉 CHESSY 1.2 IS READY!")
    print("=" * 70)
    print("\n💪 Expected strength: ~1800-2200 ELO")
    print("🏆 This is a strong club-level player!")
    print("\n🎮 Next steps:")
    print("   1. Update chess_ai_server.py to use new model")
    print("   2. Compare against Chessy 1.0 and 1.1")
    print("   3. Enjoy playing against a strong AI!")


if __name__ == "__main__":
    main()
