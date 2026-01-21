"""
Blunder Training - Teach AI to Recognize and Punish Mistakes
Addresses the weakness of training only on perfect play
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

from chess_ai_server import board_to_array, create_deep_cnn

# STOCKFISH PATH
STOCKFISH_PATH = r"C:\Users\Abu\Downloads\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe"

class BlunderTrainer:
    """Train AI to recognize and exploit blunders"""
    
    def __init__(self, stockfish_path=STOCKFISH_PATH):
        self.stockfish_path = stockfish_path
        self.engine = None
        
        print("=" * 70)
        print("⚠️ BLUNDER TRAINING - TEACH AI TO PUNISH MISTAKES")
        print("=" * 70)
        
        # Start Stockfish
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
    
    def generate_blunder_positions(self, num_positions=2000, blunder_severity='mixed'):
        """
        Generate positions where one side made a blunder
        
        blunder_severity:
        - 'mild': Small mistakes (-1 to -3 pawns)
        - 'moderate': Medium mistakes (-3 to -5 pawns)
        - 'severe': Big mistakes (-5+ pawns, hanging pieces)
        - 'mixed': All types
        """
        print("\n" + "=" * 70)
        print("⚠️ GENERATING BLUNDER POSITIONS")
        print("=" * 70)
        print(f"   Positions: {num_positions}")
        print(f"   Severity: {blunder_severity}")
        print("=" * 70)
        
        if self.engine is None:
            print("\n❌ Stockfish not available!")
            return None, None
        
        X_train = []
        y_train = []
        
        blunder_types = {
            'mild': (100, 300),      # 1-3 pawns
            'moderate': (300, 500),  # 3-5 pawns
            'severe': (500, 900)     # 5-9 pawns (piece)
        }
        
        for i in range(num_positions):
            if i % 100 == 0:
                print(f"\r⚠️ Position {i}/{num_positions}...", end='', flush=True)
            
            # Generate a reasonable position
            board = self.generate_reasonable_position()
            
            # Get current evaluation
            eval_before = self.evaluate_position(board, depth=10)
            
            # Make a blunder
            blunder_move = self.generate_blunder_move(board, blunder_severity, blunder_types)
            
            if blunder_move:
                board.push(blunder_move)
                
                # Evaluate after blunder
                eval_after = self.evaluate_position(board, depth=15)
                
                # Only keep if it's actually a significant blunder
                eval_change = abs(eval_after - eval_before)
                if eval_change > 0.3:  # Significant change
                    X_train.append(board_to_array(board))
                    y_train.append(eval_after)
        
        print(f"\n✅ Generated {len(X_train)} blunder positions")
        
        return np.array(X_train), np.array(y_train)
    
    def generate_reasonable_position(self):
        """Generate a reasonable middlegame position"""
        board = chess.Board()
        
        # Play 10-25 random but legal moves
        num_moves = random.randint(10, 25)
        
        for _ in range(num_moves):
            if board.is_game_over():
                board = chess.Board()  # Start over
                continue
            
            legal_moves = list(board.legal_moves)
            if not legal_moves:
                break
            
            # Prefer captures and checks (more interesting)
            captures = [m for m in legal_moves if board.is_capture(m)]
            checks = [m for m in legal_moves if board.gives_check(m)]
            
            if captures and random.random() < 0.3:
                move = random.choice(captures)
            elif checks and random.random() < 0.2:
                move = random.choice(checks)
            else:
                move = random.choice(legal_moves)
            
            board.push(move)
        
        return board
    
    def generate_blunder_move(self, board, severity, blunder_types):
        """Generate a blunder move of specified severity"""
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None
        
        # Get best move from Stockfish
        best_move_result = self.engine.play(board, chess.engine.Limit(depth=10))
        best_move = best_move_result.move
        
        # Evaluate best move
        board.push(best_move)
        best_eval = self.evaluate_position(board, depth=10)
        board.pop()
        
        # Find moves that are worse
        blunder_candidates = []
        
        for move in legal_moves:
            if move == best_move:
                continue
            
            board.push(move)
            move_eval = self.evaluate_position(board, depth=10)
            board.pop()
            
            # Calculate how bad this move is
            eval_loss = abs(move_eval - best_eval)
            
            # Check if it matches severity
            if severity == 'mixed':
                if eval_loss > 0.2:  # Any significant mistake
                    blunder_candidates.append((move, eval_loss))
            elif severity in blunder_types:
                min_loss, max_loss = blunder_types[severity]
                min_loss_norm = min_loss / 400.0
                max_loss_norm = max_loss / 400.0
                if min_loss_norm < eval_loss < max_loss_norm:
                    blunder_candidates.append((move, eval_loss))
        
        if blunder_candidates:
            # Pick a random blunder from candidates
            return random.choice(blunder_candidates)[0]
        else:
            # If no good blunder found, just pick a random bad move
            return random.choice(legal_moves)
    
    def generate_hanging_piece_positions(self, num_positions=500):
        """Generate positions where a piece is hanging (undefended)"""
        print("\n" + "=" * 70)
        print("🎯 GENERATING HANGING PIECE POSITIONS")
        print("=" * 70)
        print(f"   Positions: {num_positions}")
        print("=" * 70)
        
        X_train = []
        y_train = []
        
        for i in range(num_positions):
            if i % 50 == 0:
                print(f"\r🎯 Position {i}/{num_positions}...", end='', flush=True)
            
            # Generate position
            board = self.generate_reasonable_position()
            
            # Try to create a hanging piece
            legal_moves = list(board.legal_moves)
            
            for move in legal_moves:
                board.push(move)
                
                # Check if this move hangs a piece
                if self.is_piece_hanging(board):
                    eval_after = self.evaluate_position(board, depth=15)
                    
                    X_train.append(board_to_array(board))
                    y_train.append(eval_after)
                    board.pop()
                    break
                
                board.pop()
        
        print(f"\n✅ Generated {len(X_train)} hanging piece positions")
        
        return np.array(X_train), np.array(y_train)
    
    def is_piece_hanging(self, board):
        """Check if any piece is hanging (undefended and attacked)"""
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and piece.color == board.turn:
                # Check if piece is attacked
                if board.is_attacked_by(not board.turn, square):
                    # Check if piece is defended
                    if not board.is_attacked_by(board.turn, square):
                        # Piece is hanging!
                        if piece.piece_type != chess.PAWN:  # Ignore pawns
                            return True
        return False
    
    def generate_tactical_blunders(self, num_positions=500):
        """Generate positions with tactical blunders (forks, pins, skewers)"""
        print("\n" + "=" * 70)
        print("⚔️ GENERATING TACTICAL BLUNDER POSITIONS")
        print("=" * 70)
        print(f"   Positions: {num_positions}")
        print("=" * 70)
        
        X_train = []
        y_train = []
        
        for i in range(num_positions):
            if i % 50 == 0:
                print(f"\r⚔️ Position {i}/{num_positions}...", end='', flush=True)
            
            # Generate position
            board = self.generate_reasonable_position()
            
            # Make a random move that might create tactical issues
            legal_moves = list(board.legal_moves)
            move = random.choice(legal_moves)
            board.push(move)
            
            # Check if opponent has a strong tactical response
            opponent_moves = list(board.legal_moves)
            
            for opp_move in opponent_moves:
                board.push(opp_move)
                
                # Check if this creates a big advantage
                eval_after = self.evaluate_position(board, depth=12)
                
                if abs(eval_after) > 0.5:  # Significant tactical advantage
                    X_train.append(board_to_array(board))
                    y_train.append(eval_after)
                    board.pop()
                    break
                
                board.pop()
        
        print(f"\n✅ Generated {len(X_train)} tactical positions")
        
        return np.array(X_train), np.array(y_train)
    
    def train_on_blunders(self, existing_model_path=None, epochs=20):
        """Train model on blunder positions"""
        print("\n" + "=" * 70)
        print("🧠 TRAINING ON BLUNDER POSITIONS")
        print("=" * 70)
        
        # Generate all types of blunder positions
        print("\n1️⃣ Generating general blunders...")
        X_blunders, y_blunders = self.generate_blunder_positions(2000, 'mixed')
        
        print("\n2️⃣ Generating hanging pieces...")
        X_hanging, y_hanging = self.generate_hanging_piece_positions(500)
        
        print("\n3️⃣ Generating tactical blunders...")
        X_tactical, y_tactical = self.generate_tactical_blunders(500)
        
        # Combine all data
        X_train = np.concatenate([X_blunders, X_hanging, X_tactical])
        y_train = np.concatenate([y_blunders, y_hanging, y_tactical])
        
        print(f"\n📊 Total training positions: {len(X_train)}")
        
        # Load existing model or create new
        if existing_model_path and os.path.exists(existing_model_path):
            print(f"\n📦 Loading existing model: {existing_model_path}")
            model = keras.models.load_model(existing_model_path, compile=False)
            model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        else:
            print(f"\n🆕 Creating new model")
            model = create_deep_cnn()
        
        # Train
        print("\n🚀 Training...\n")
        
        history = model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=64,
            validation_split=0.2,
            verbose=1
        )
        
        # Save model
        model.save('chess_model_blunder_trained.h5')
        
        # Save info
        info = {
            'version': 'Chessy Blunder Training',
            'training_method': 'Blunder Recognition',
            'training_positions': len(X_train),
            'blunder_positions': len(X_blunders),
            'hanging_positions': len(X_hanging),
            'tactical_positions': len(X_tactical),
            'epochs': epochs,
            'final_loss': float(history.history['loss'][-1]),
            'final_val_loss': float(history.history['val_loss'][-1]),
            'trained_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        with open('chess_model_blunder_trained_info.json', 'w') as f:
            json.dump(info, f, indent=2)
        
        print("\n" + "=" * 70)
        print("✅ BLUNDER TRAINING COMPLETE!")
        print("=" * 70)
        print(f"\n📊 Results:")
        print(f"   Training loss: {info['final_loss']:.4f}")
        print(f"   Validation loss: {info['final_val_loss']:.4f}")
        print(f"\n💾 Model saved: chess_model_blunder_trained.h5")
        
        return model, history
    
    def close(self):
        """Close Stockfish engine"""
        if self.engine:
            self.engine.quit()
            print("\n✅ Stockfish closed")


def main():
    """Main training pipeline"""
    
    print("\n" + "=" * 70)
    print("⚠️ BLUNDER TRAINING - TEACH AI TO PUNISH MISTAKES")
    print("=" * 70)
    print("\nThis training addresses the weakness of training only on perfect play.")
    print("Your AI will learn to recognize and exploit blunders!\n")
    
    # Check for existing model
    print("📦 Looking for existing models...")
    
    existing_models = []
    if os.path.exists('chess_model_stockfish_deep.h5'):
        existing_models.append(('chess_model_stockfish_deep.h5', 'Chessy 1.2 Stockfish'))
    if os.path.exists('chess_model_magnus_basic.h5'):
        existing_models.append(('chess_model_magnus_basic.h5', 'Chessy 1.1 Magnus'))
    if os.path.exists('chess_model_basic.h5'):
        existing_models.append(('chess_model_basic.h5', 'Chessy 1.0 Basic'))
    
    if existing_models:
        print("\n✅ Found existing models:")
        for i, (path, name) in enumerate(existing_models, 1):
            print(f"   {i}. {name} ({path})")
        
        print("\n   0. Train from scratch (new model)")
        
        choice = input("\nSelect model to improve (0-{}): ".format(len(existing_models))).strip()
        
        if choice == '0':
            existing_model = None
        else:
            try:
                idx = int(choice) - 1
                existing_model = existing_models[idx][0]
                print(f"\n✅ Will improve: {existing_models[idx][1]}")
            except:
                existing_model = None
    else:
        existing_model = None
        print("\n⚠️ No existing models found, will train from scratch")
    
    # Initialize trainer
    trainer = BlunderTrainer(STOCKFISH_PATH)
    
    if trainer.engine is None:
        print("\n❌ Cannot proceed without Stockfish!")
        return
    
    # Train
    model, history = trainer.train_on_blunders(
        existing_model_path=existing_model,
        epochs=20
    )
    
    # Close Stockfish
    trainer.close()
    
    print("\n" + "=" * 70)
    print("🎉 YOUR AI CAN NOW PUNISH BLUNDERS!")
    print("=" * 70)
    print("\n💪 Improvements:")
    print("   ✅ Recognizes hanging pieces")
    print("   ✅ Exploits tactical mistakes")
    print("   ✅ Punishes blunders aggressively")
    print("   ✅ Better against weak players")
    print("\n🎮 Next steps:")
    print("   1. Update chess_ai_server.py to use new model")
    print("   2. Test against weak opponents")
    print("   3. Enjoy crushing blunders!")


if __name__ == "__main__":
    main()
