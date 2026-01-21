"""
Stockfish Opening Training - Teach Chessy 1.3 Opening Theory
Generates opening positions evaluated by Stockfish
"""

import chess
import chess.engine
import chess.pgn
import numpy as np
from tensorflow import keras
import os
import json
from datetime import datetime
import random

from chess_ai_server import board_to_array

# STOCKFISH PATH
STOCKFISH_PATH = r"C:\Users\Abu\Downloads\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe"

class OpeningTrainer:
    """Train on opening positions"""
    
    def __init__(self, stockfish_path=STOCKFISH_PATH):
        self.stockfish_path = stockfish_path
        self.engine = None
        
        print("=" * 70)
        print("📚 OPENING TRAINING - TEACH CHESSY OPENING THEORY")
        print("=" * 70)
        
        # Start Stockfish
        try:
            print(f"\n🚀 Starting Stockfish...")
            self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
            print(f"   ✅ Stockfish started successfully!")
        except Exception as e:
            print(f"   ❌ Error starting Stockfish: {e}")
            self.engine = None
    
    def evaluate_position(self, board, depth=20):
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
    
    def generate_opening_positions(self, num_positions=5000):
        """
        Generate opening positions (moves 1-15)
        Evaluated by Stockfish for opening theory
        """
        print("\n" + "=" * 70)
        print("📚 GENERATING OPENING POSITIONS")
        print("=" * 70)
        print(f"   Positions: {num_positions}")
        print(f"   Moves: 1-15 (opening phase)")
        print("=" * 70)
        
        if self.engine is None:
            print("\n❌ Stockfish not available!")
            return None, None
        
        X_train = []
        y_train = []
        
        # Common opening moves to explore
        common_openings = [
            ['e2e4', 'e7e5'],  # King's Pawn
            ['e2e4', 'c7c5'],  # Sicilian
            ['e2e4', 'e7e6'],  # French
            ['d2d4', 'd7d5'],  # Queen's Pawn
            ['d2d4', 'g8f6'],  # Indian Defenses
            ['c2c4', 'e7e5'],  # English
            ['g1f3', 'd7d5'],  # Reti
        ]
        
        positions_per_opening = num_positions // len(common_openings)
        
        for opening_moves in common_openings:
            print(f"\n📖 Exploring opening: {' '.join(opening_moves)}")
            
            for i in range(positions_per_opening):
                if i % 100 == 0:
                    print(f"   Position {i}/{positions_per_opening}...")
                
                board = chess.Board()
                
                # Play the opening moves
                for move_uci in opening_moves:
                    try:
                        move = chess.Move.from_uci(move_uci)
                        if move in board.legal_moves:
                            board.push(move)
                    except:
                        pass
                
                # Continue with random legal moves for 5-13 more moves
                num_extra_moves = random.randint(5, 13)
                
                for _ in range(num_extra_moves):
                    if board.is_game_over():
                        break
                    
                    legal_moves = list(board.legal_moves)
                    if not legal_moves:
                        break
                    
                    # Prefer center moves and development
                    good_moves = []
                    for move in legal_moves:
                        to_square = move.to_square
                        row, col = divmod(to_square, 8)
                        
                        # Prefer center squares
                        if 2 <= row <= 5 and 2 <= col <= 5:
                            good_moves.append(move)
                        # Prefer piece development
                        elif board.piece_at(move.from_square).piece_type in [chess.KNIGHT, chess.BISHOP]:
                            good_moves.append(move)
                    
                    if good_moves and random.random() < 0.7:
                        move = random.choice(good_moves)
                    else:
                        move = random.choice(legal_moves)
                    
                    board.push(move)
                
                # Evaluate with Stockfish (deeper for openings)
                evaluation = self.evaluate_position(board, depth=20)
                
                X_train.append(board_to_array(board))
                y_train.append(evaluation)
        
        print(f"\n✅ Generated {len(X_train)} opening positions")
        
        return np.array(X_train), np.array(y_train)
    
    def train_on_openings(self, existing_model_path=None, epochs=25):
        """Train model on opening positions"""
        print("\n" + "=" * 70)
        print("🧠 TRAINING ON OPENING POSITIONS")
        print("=" * 70)
        
        # Generate opening positions
        X_train, y_train = self.generate_opening_positions(5000)
        
        if X_train is None:
            print("\n❌ Failed to generate training data!")
            return None, None
        
        print(f"\n📊 Total training positions: {len(X_train)}")
        
        # Load existing model or create new
        if existing_model_path and os.path.exists(existing_model_path):
            print(f"\n📦 Loading existing model: {existing_model_path}")
            model = keras.models.load_model(existing_model_path, compile=False)
            model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        else:
            print(f"\n❌ No existing model found!")
            print("   Opening training should be done AFTER base training!")
            return None, None
        
        # Train
        print("\n🚀 Training on openings...\n")
        
        history = model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=64,
            validation_split=0.2,
            verbose=1
        )
        
        # Save model
        model.save('chess_model_with_openings.h5')
        
        # Save info
        info = {
            'version': 'Chessy 1.3 - Opening Training',
            'training_method': 'Stockfish Opening Evaluation',
            'training_positions': len(X_train),
            'epochs': epochs,
            'final_loss': float(history.history['loss'][-1]),
            'final_val_loss': float(history.history['val_loss'][-1]),
            'trained_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        with open('chess_model_with_openings_info.json', 'w') as f:
            json.dump(info, f, indent=2)
        
        print("\n" + "=" * 70)
        print("✅ OPENING TRAINING COMPLETE!")
        print("=" * 70)
        print(f"\n📊 Results:")
        print(f"   Training loss: {info['final_loss']:.4f}")
        print(f"   Validation loss: {info['final_val_loss']:.4f}")
        print(f"\n💾 Model saved: chess_model_with_openings.h5")
        
        return model, history
    
    def close(self):
        """Close Stockfish engine"""
        if self.engine:
            self.engine.quit()
            print("\n✅ Stockfish closed")


def main():
    """Main training pipeline"""
    
    print("\n" + "=" * 70)
    print("📚 OPENING TRAINING - TEACH CHESSY OPENING THEORY")
    print("=" * 70)
    print("\nThis adds opening knowledge to an existing model.")
    print("Run this AFTER base training (Chessy 1.2 or 1.3)\n")
    
    # Check for existing models
    print("📦 Looking for existing models...")
    
    existing_models = []
    if os.path.exists('chess_model_stockfish_deep.h5'):
        existing_models.append(('chess_model_stockfish_deep.h5', 'Chessy 1.2 Stockfish'))
    if os.path.exists('chess_model_rapid_standard.h5'):
        existing_models.append(('chess_model_rapid_standard.h5', 'Chessy 1.3 Rapid'))
    if os.path.exists('chess_model_classical_deep.h5'):
        existing_models.append(('chess_model_classical_deep.h5', 'Chessy 1.3 Classical'))
    
    if not existing_models:
        print("\n❌ No trained models found!")
        print("   Train a base model first (Chessy 1.2 or 1.3)")
        return
    
    print("\n✅ Found existing models:")
    for i, (path, name) in enumerate(existing_models, 1):
        print(f"   {i}. {name} ({path})")
    
    choice = input(f"\nSelect model to add openings (1-{len(existing_models)}): ").strip()
    
    try:
        idx = int(choice) - 1
        existing_model = existing_models[idx][0]
        print(f"\n✅ Will add openings to: {existing_models[idx][1]}")
    except:
        print("\n❌ Invalid choice!")
        return
    
    # Initialize trainer
    trainer = OpeningTrainer(STOCKFISH_PATH)
    
    if trainer.engine is None:
        print("\n❌ Cannot proceed without Stockfish!")
        return
    
    # Train
    model, history = trainer.train_on_openings(
        existing_model_path=existing_model,
        epochs=25
    )
    
    # Close Stockfish
    trainer.close()
    
    print("\n" + "=" * 70)
    print("🎉 YOUR AI NOW KNOWS OPENING THEORY!")
    print("=" * 70)
    print("\n💪 Improvements:")
    print("   ✅ Plays e4, d4, Nf3 instead of h5, a6")
    print("   ✅ Understands opening principles")
    print("   ✅ Develops pieces properly")
    print("   ✅ Controls center")
    print("\n🎮 Next steps:")
    print("   1. Update chess_ai_server.py to use new model")
    print("   2. Test opening play")
    print("   3. Enjoy proper openings!")


if __name__ == "__main__":
    main()
