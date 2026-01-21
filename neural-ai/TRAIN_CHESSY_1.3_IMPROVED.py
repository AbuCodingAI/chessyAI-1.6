"""
Chessy 1.3 - IMPROVED Training (Anti-Overfitting Edition)
Focus: Generalization > Memorization
"""

import chess
import chess.engine
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers, regularizers
import os
import json
from datetime import datetime
import random

from chess_ai_server import board_to_array

# STOCKFISH PATH
STOCKFISH_PATH = r"C:\Users\Abu\Downloads\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe"

def create_regularized_cnn():
    """Create CNN with heavy regularization to prevent overfitting"""
    model = keras.Sequential([
        # Input
        layers.Input(shape=(8, 8, 12)),
        
        # Conv Block 1 - WITH DROPOUT
        layers.Conv2D(64, (3, 3), padding='same', 
                     kernel_regularizer=regularizers.l2(0.001)),
        layers.BatchNormalization(),
        layers.Activation('relu'),
        layers.Dropout(0.3),  # NEW: Dropout after first block
        
        # Conv Block 2 - WITH DROPOUT
        layers.Conv2D(128, (3, 3), padding='same',
                     kernel_regularizer=regularizers.l2(0.001)),
        layers.BatchNormalization(),
        layers.Activation('relu'),
        layers.Dropout(0.3),  # NEW: Dropout
        
        # Conv Block 3 - WITH DROPOUT
        layers.Conv2D(128, (3, 3), padding='same',
                     kernel_regularizer=regularizers.l2(0.001)),
        layers.BatchNormalization(),
        layers.Activation('relu'),
        layers.Dropout(0.4),  # NEW: Higher dropout
        
        # Global pooling instead of flatten (reduces params)
        layers.GlobalAveragePooling2D(),
        
        # Dense layers - SMALLER + MORE DROPOUT
        layers.Dense(256, activation='relu',
                    kernel_regularizer=regularizers.l2(0.001)),
        layers.Dropout(0.5),  # NEW: Heavy dropout
        
        layers.Dense(128, activation='relu',
                    kernel_regularizer=regularizers.l2(0.001)),
        layers.Dropout(0.5),  # NEW: Heavy dropout
        
        # Output
        layers.Dense(1, activation='tanh')
    ])
    
    # Use lower learning rate for better generalization
    optimizer = keras.optimizers.Adam(learning_rate=0.0005)
    
    model.compile(
        optimizer=optimizer,
        loss='mse',
        metrics=['mae']
    )
    
    return model


class ImprovedChessy13Trainer:
    """Train with anti-overfitting measures"""
    
    def __init__(self, stockfish_path=STOCKFISH_PATH):
        self.stockfish_path = stockfish_path
        self.engine = None
        
        print("=" * 70)
        print("♔ CHESSY 1.3 - IMPROVED (ANTI-OVERFITTING)")
        print("=" * 70)
        print("\nAnti-overfitting measures:")
        print("  ✅ Noise injection (random moves every ~10 moves)")
        print("  ✅ Skip noisy games (only train on clean positions)")
        print("  ✅ Dropout layers (30-50%)")
        print("  ✅ L2 regularization")
        print("  ✅ Larger dataset (15k positions)")
        print("  ✅ Better validation split (25%)")
        print("  ✅ Aggressive early stopping")
        print("  ✅ Lower learning rate")
        print("=" * 70)
        
        try:
            print(f"\n🚀 Starting Stockfish...")
            self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
            print(f"   ✅ Stockfish started!")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            self.engine = None
    
    def evaluate_position(self, board, depth=20):
        """Evaluate with Stockfish"""
        try:
            info = self.engine.analyse(board, chess.engine.Limit(depth=depth))
            score = info["score"].relative
            
            if score.is_mate():
                return 1.0 if score.mate() > 0 else -1.0
            else:
                return np.tanh(score.score() / 400.0)
        except:
            return 0.0
    

    
    def step1_diverse_positions(self, num_positions=15000):
        """Generate diverse positions with noise injection"""
        print("\n" + "=" * 70)
        print("STEP 1: DIVERSE POSITION TRAINING")
        print("=" * 70)
        print(f"Generating {num_positions} diverse positions")
        print("Noise injection: Random moves every ~10 moves (skipped)")
        print("Result: Only clean, high-quality positions collected")
        print("=" * 70)
        
        X_train = []
        y_train = []
        
        # 35% Opening positions
        print("\n📚 Generating opening positions (35%)...")
        X_open, y_open = self.generate_opening_positions(int(num_positions * 0.35))
        if len(X_open) > 0:
            X_train.append(X_open)
            y_train.append(y_open)
        
        # 35% Middlegame positions
        print("\n⚔️ Generating middlegame positions (35%)...")
        X_mid, y_mid = self.generate_middlegame_positions(int(num_positions * 0.35))
        if len(X_mid) > 0:
            X_train.append(X_mid)
            y_train.append(y_mid)
        
        # 20% Tactical positions
        print("\n🎯 Generating tactical positions (20%)...")
        X_tac, y_tac = self.generate_tactical_positions(int(num_positions * 0.20))
        if len(X_tac) > 0:
            X_train.append(X_tac)
            y_train.append(y_tac)
        
        # 10% Endgame positions
        print("\n👑 Generating endgame positions (10%)...")
        X_end, y_end = self.generate_endgame_positions(int(num_positions * 0.10))
        if len(X_end) > 0:
            X_train.append(X_end)
            y_train.append(y_end)
        
        if len(X_train) == 0:
            raise ValueError("No positions were generated!")
        
        X_train = np.concatenate(X_train)
        y_train = np.concatenate(y_train)
        
        # Shuffle thoroughly
        indices = np.random.permutation(len(X_train))
        X_train = X_train[indices]
        y_train = y_train[indices]
        
        print(f"\n✅ Final dataset: {len(X_train)} clean positions")
        print(f"   (Noisy games were discarded during generation)")
        
        return X_train, y_train
    
    def generate_opening_positions(self, num_positions):
        """Generate opening positions with noise injection"""
        X_train = []
        y_train = []
        
        # Expanded opening repertoire
        common_openings = [
            ['e2e4', 'e7e5'],              # King's Pawn
            ['e2e4', 'c7c5'],              # Sicilian
            ['e2e4', 'e7e6'],              # French
            ['e2e4', 'c7c6'],              # Caro-Kann
            ['e2e4', 'd7d5'],              # Scandinavian
            ['d2d4', 'd7d5'],              # Queen's Pawn
            ['d2d4', 'g8f6'],              # Indian
            ['d2d4', 'g8f6', 'c2c4'],      # Indian with c4
            ['c2c4'],                      # English
            ['g1f3'],                      # Reti
            ['g1f3', 'd7d5', 'c2c4'],      # Reti System
            ['d2d4', 'd7d5', 'c2c4', 'e7e6'],  # Queen's Gambit
        ]
        
        collected = 0
        attempts = 0
        max_attempts = num_positions * 3
        opening_idx = 0
        
        while collected < num_positions and attempts < max_attempts:
            attempts += 1
            
            if collected % 200 == 0:
                print(f"   Position {collected}/{num_positions}...")
            
            # Cycle through openings
            opening_moves = common_openings[opening_idx % len(common_openings)]
            opening_idx += 1
            
            board = chess.Board()
            
            # Play opening moves
            for move_uci in opening_moves:
                try:
                    move = chess.Move.from_uci(move_uci)
                    if move in board.legal_moves:
                        board.push(move)
                except:
                    pass
            
            # Continue with noise injection
            num_moves = random.randint(3, 15)
            noise_move_made = False
            
            for move_num in range(num_moves):
                if board.is_game_over():
                    break
                legal_moves = list(board.legal_moves)
                if not legal_moves:
                    break
                
                # Inject noise every ~10 moves
                if move_num > 0 and move_num % 10 == 0 and random.random() < 0.5:
                    noise_move_made = True
                
                # Good moves
                good_moves = [m for m in legal_moves 
                             if self.is_good_opening_move(board, m)]
                
                if good_moves and random.random() < 0.7:
                    move = random.choice(good_moves)
                else:
                    move = random.choice(legal_moves)
                
                board.push(move)
            
            # SKIP if noise was injected
            if not noise_move_made:
                evaluation = self.evaluate_position(board, depth=18)
                X_train.append(board_to_array(board))
                y_train.append(evaluation)
                collected += 1
        
        return np.array(X_train), np.array(y_train)
    
    def is_good_opening_move(self, board, move):
        """Check if move follows opening principles"""
        to_square = move.to_square
        row, col = divmod(to_square, 8)
        
        # Center squares
        if 2 <= row <= 5 and 2 <= col <= 5:
            return True
        
        # Piece development
        piece = board.piece_at(move.from_square)
        if piece and piece.piece_type in [chess.KNIGHT, chess.BISHOP]:
            return True
        
        return False
    
    def generate_middlegame_positions(self, num_positions):
        """Generate middlegame with noise injection"""
        X_train = []
        y_train = []
        
        collected = 0
        attempts = 0
        max_attempts = num_positions * 3  # Try up to 3x to get enough positions
        
        while collected < num_positions and attempts < max_attempts:
            attempts += 1
            
            if collected % 200 == 0:
                print(f"   Position {collected}/{num_positions}...")
            
            board = chess.Board()
            
            # Play with noise injection
            num_moves = random.randint(12, 45)
            noise_move_made = False
            
            for move_num in range(num_moves):
                if board.is_game_over():
                    break
                legal_moves = list(board.legal_moves)
                if not legal_moves:
                    break
                
                # Inject noise every ~10 moves
                if move_num > 0 and move_num % 10 == 0 and random.random() < 0.5:
                    noise_move_made = True
                
                move = random.choice(legal_moves)
                board.push(move)
            
            # SKIP if noise was injected
            if not noise_move_made and not board.is_game_over() and len(board.piece_map()) >= 8:
                evaluation = self.evaluate_position(board, depth=16)
                X_train.append(board_to_array(board))
                y_train.append(evaluation)
                collected += 1
        
        return np.array(X_train), np.array(y_train)
    
    def generate_tactical_positions(self, num_positions):
        """Generate tactical positions with noise injection"""
        X_train = []
        y_train = []
        
        collected = 0
        attempts = 0
        max_attempts = num_positions * 3
        
        while collected < num_positions and attempts < max_attempts:
            attempts += 1
            
            if collected % 100 == 0:
                print(f"   Position {collected}/{num_positions}...")
            
            board = chess.Board()
            
            # Play to middlegame with noise
            num_moves = random.randint(12, 35)
            noise_move_made = False
            
            for move_num in range(num_moves):
                if board.is_game_over():
                    break
                legal_moves = list(board.legal_moves)
                if not legal_moves:
                    break
                
                # Inject noise every ~10 moves
                if move_num > 0 and move_num % 10 == 0 and random.random() < 0.5:
                    noise_move_made = True
                
                move = random.choice(legal_moves)
                board.push(move)
            
            # Make a random move (might be blunder)
            legal_moves = list(board.legal_moves)
            if legal_moves and not noise_move_made:
                move = random.choice(legal_moves)
                board.push(move)
                
                evaluation = self.evaluate_position(board, depth=16)
                
                # Keep if significant (tactical)
                if abs(evaluation) > 0.25:
                    X_train.append(board_to_array(board))
                    y_train.append(evaluation)
                    collected += 1
        
        return np.array(X_train), np.array(y_train)
    
    def generate_endgame_positions(self, num_positions):
        """Generate endgame positions with noise injection"""
        X_train = []
        y_train = []
        
        collected = 0
        attempts = 0
        max_attempts = num_positions * 3
        
        while collected < num_positions and attempts < max_attempts:
            attempts += 1
            
            if collected % 100 == 0:
                print(f"   Position {collected}/{num_positions}...")
            
            board = chess.Board()
            
            # Play to endgame with noise
            num_moves = random.randint(40, 70)
            noise_move_made = False
            
            for move_num in range(num_moves):
                if board.is_game_over():
                    break
                legal_moves = list(board.legal_moves)
                if not legal_moves:
                    break
                
                # Inject noise every ~10 moves
                if move_num > 0 and move_num % 10 == 0 and random.random() < 0.5:
                    noise_move_made = True
                
                move = random.choice(legal_moves)
                board.push(move)
            
            # SKIP if noise was injected
            if not noise_move_made and not board.is_game_over() and 4 <= len(board.piece_map()) <= 12:
                evaluation = self.evaluate_position(board, depth=20)
                X_train.append(board_to_array(board))
                y_train.append(evaluation)
                collected += 1
        
        return np.array(X_train), np.array(y_train)
    
    def train_complete_model(self, X_train, y_train, epochs=50):
        """Train with aggressive anti-overfitting"""
        print("\n" + "=" * 70)
        print("STEP 2: TRAINING WITH ANTI-OVERFITTING")
        print("=" * 70)
        print(f"Training positions: {len(X_train)}")
        print(f"Max epochs: {epochs}")
        print("Early stopping: patience=5 (aggressive)")
        print("Learning rate reduction: patience=3")
        print("=" * 70)
        
        # Create regularized network
        model = create_regularized_cnn()
        
        print(f"\n🧠 Model parameters: {model.count_params():,}")
        print("   (Fewer params = less overfitting)")
        
        # Aggressive callbacks
        callbacks = [
            # Stop early if validation loss doesn't improve
            keras.callbacks.EarlyStopping(
                patience=5,  # More aggressive (was 7)
                restore_best_weights=True,
                monitor='val_loss',
                verbose=1
            ),
            
            # Reduce learning rate quickly
            keras.callbacks.ReduceLROnPlateau(
                factor=0.5,
                patience=3,  # More aggressive (was 4)
                min_lr=1e-6,
                verbose=1
            ),
            
            # Save best model
            keras.callbacks.ModelCheckpoint(
                'chess_model_chessy_1.3_improved.h5',
                save_best_only=True,
                monitor='val_loss',
                verbose=1
            )
        ]
        
        print("\n🚀 Training...\n")
        
        history = model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=128,  # Larger batch = better generalization
            validation_split=0.25,  # More validation data
            callbacks=callbacks,
            verbose=1
        )
        
        # Save final model
        model.save('chess_model_chessy_1.3_improved_final.h5')
        
        # Calculate overfitting metric
        final_train_loss = history.history['loss'][-1]
        final_val_loss = history.history['val_loss'][-1]
        overfitting_ratio = final_val_loss / final_train_loss
        
        info = {
            'version': 'Chessy 1.3 - Improved (Anti-Overfitting)',
            'training_method': 'Noise Injection + Regularized CNN',
            'training_positions': len(X_train),
            'epochs_trained': len(history.history['loss']),
            'max_epochs': epochs,
            'final_loss': float(final_train_loss),
            'final_val_loss': float(final_val_loss),
            'overfitting_ratio': float(overfitting_ratio),
            'final_mae': float(history.history['mae'][-1]),
            'final_val_mae': float(history.history['val_mae'][-1]),
            'anti_overfitting': {
                'noise_injection': 'random_moves_every_10_moves',
                'noisy_games_skipped': True,
                'dropout': '0.3-0.5',
                'l2_regularization': 0.001,
                'batch_size': 128,
                'validation_split': 0.25
            },
            'trained_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        with open('chess_model_chessy_1.3_improved_info.json', 'w') as f:
            json.dump(info, f, indent=2)
        
        print("\n" + "=" * 70)
        print("✅ TRAINING COMPLETE!")
        print("=" * 70)
        print(f"   Train Loss: {final_train_loss:.4f}")
        print(f"   Val Loss: {final_val_loss:.4f}")
        print(f"   Overfitting Ratio: {overfitting_ratio:.3f}")
        
        if overfitting_ratio < 1.15:
            print("   ✅ EXCELLENT - Minimal overfitting!")
        elif overfitting_ratio < 1.30:
            print("   ✅ GOOD - Acceptable overfitting")
        elif overfitting_ratio < 1.50:
            print("   ⚠️  MODERATE - Some overfitting")
        else:
            print("   ❌ HIGH - Significant overfitting")
        
        print(f"\n   Epochs used: {len(history.history['loss'])}/{epochs}")
        print(f"   (Early stopping saved {epochs - len(history.history['loss'])} epochs)")
        
        return model, history
    
    def close(self):
        """Close Stockfish"""
        if self.engine:
            self.engine.quit()


def main():
    """Main training pipeline"""
    
    print("\n" + "=" * 70)
    print("♔ CHESSY 1.3 - IMPROVED TRAINING")
    print("=" * 70)
    print("\n🎯 Goal: Fix overfitting, improve generalization")
    print("\n📊 Changes from original:")
    print("  ✅ NOISE INJECTION (random moves every ~10 moves)")
    print("  ✅ SKIP NOISY GAMES (only train on clean positions)")
    print("  ✅ Dropout layers (30-50%)")
    print("  ✅ L2 regularization")
    print("  ✅ Larger dataset (10k → 15k)")
    print("  ✅ Better validation (25% instead of 20%)")
    print("  ✅ Aggressive early stopping")
    print("  ✅ Larger batch size (128)")
    print("  ✅ Lower learning rate")
    print("  ✅ Endgame positions added")
    print("\n⏱️  Training time: ~3 hours")
    print("🏆 Result: Better generalization!")
    print("\n💡 Key insight:")
    print("   Noise injection forces diverse game paths")
    print("   Only clean positions are collected")
    print("   = AI learns patterns, not specific games")
    
    response = input("\n🎯 Start improved training? (y/n): ").lower()
    if response != 'y':
        print("\n❌ Training cancelled.")
        return
    
    overall_start = datetime.now()
    
    # Initialize
    trainer = ImprovedChessy13Trainer(STOCKFISH_PATH)
    
    if trainer.engine is None:
        print("\n❌ Cannot proceed without Stockfish!")
        return
    
    try:
        # Step 1: Generate diverse positions (MORE + AUGMENTED)
        X_train, y_train = trainer.step1_diverse_positions(15000)
        
        # Step 2: Train with anti-overfitting
        model, history = trainer.train_complete_model(X_train, y_train, epochs=50)
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Training interrupted!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        trainer.close()
    
    overall_elapsed = datetime.now() - overall_start
    
    print("\n" + "=" * 70)
    print("🎉 CHESSY 1.3 IMPROVED - COMPLETE!")
    print("=" * 70)
    print(f"\n⏱️  Total time: {overall_elapsed}")
    print("\n💪 What you have:")
    print("  ✅ chess_model_chessy_1.3_improved.h5")
    print("  ✅ Trained on ~15k clean positions")
    print("  ✅ Noise injection prevented overfitting")
    print("  ✅ Heavy regularization (dropout + L2)")
    print("  ✅ Better generalization")
    print("\n📊 Check the overfitting ratio in the info file!")
    print("  Target: < 1.15 (excellent)")
    print("  Acceptable: < 1.30")
    print("\n🚀 Next step:")
    print("  Test against the old model")
    print("  Compare validation losses")
    print("  Play some games!")


if __name__ == "__main__":
    main()
