"""
CHESSY 1.5 - SELF-PLAY TRAINING
Train neural network through self-play, then test against Stockfish

Training Process:
1. Self-play: 40 games (Chessy vs Chessy)
2. Learn from games
3. Test: 60 games vs Stockfish
4. Track results and ELO estimation
"""

import chess
import chess.engine
import numpy as np
import tensorflow as tf
from tensorflow import keras
import random
import json
import os
from datetime import datetime

# Configuration
SELF_PLAY_GAMES = 40
STOCKFISH_TEST_GAMES = 60
STOCKFISH_PATH = "../stockfish/stockfish-windows-x86-64-avx2.exe"
MODEL_PATH = "models/chessy_1.5_model.h5"
RESULTS_PATH = "results/chessy_1.5_results.json"

class ChessyNeuralNetwork:
    """Neural network for chess position evaluation"""
    
    def __init__(self):
        self.model = self.build_model()
        
    def build_model(self):
        """Build neural network architecture"""
        model = keras.Sequential([
            keras.layers.Dense(512, activation='relu', input_shape=(768,)),
            keras.layers.Dropout(0.3),
            keras.layers.Dense(256, activation='relu'),
            keras.layers.Dropout(0.3),
            keras.layers.Dense(128, activation='relu'),
            keras.layers.Dense(64, activation='relu'),
            keras.layers.Dense(1, activation='tanh')  # Output: -1 to 1
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )
        
        return model
    
    def board_to_input(self, board):
        """Convert chess board to neural network input"""
        # 768 features: 64 squares * 12 piece types (6 white + 6 black)
        input_array = np.zeros(768)
        
        piece_map = {
            chess.PAWN: 0, chess.KNIGHT: 1, chess.BISHOP: 2,
            chess.ROOK: 3, chess.QUEEN: 4, chess.KING: 5
        }
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                piece_type = piece_map[piece.piece_type]
                offset = piece_type if piece.color == chess.WHITE else piece_type + 6
                input_array[square * 12 + offset] = 1
        
        return input_array
    
    def evaluate_position(self, board):
        """Evaluate position using neural network"""
        input_data = self.board_to_input(board).reshape(1, -1)
        evaluation = self.model.predict(input_data, verbose=0)[0][0]
        return float(evaluation)
    
    def get_best_move(self, board, depth=3):
        """Get best move using minimax with neural network evaluation"""
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None
        
        best_move = None
        best_eval = float('-inf') if board.turn == chess.WHITE else float('inf')
        
        for move in legal_moves:
            board.push(move)
            eval_score = self.minimax(board, depth - 1, float('-inf'), float('inf'), not board.turn)
            board.pop()
            
            if board.turn == chess.WHITE:
                if eval_score > best_eval:
                    best_eval = eval_score
                    best_move = move
            else:
                if eval_score < best_eval:
                    best_eval = eval_score
                    best_move = move
        
        return best_move
    
    def minimax(self, board, depth, alpha, beta, maximizing):
        """Minimax algorithm with alpha-beta pruning"""
        if depth == 0 or board.is_game_over():
            return self.evaluate_position(board)
        
        legal_moves = list(board.legal_moves)
        
        if maximizing:
            max_eval = float('-inf')
            for move in legal_moves:
                board.push(move)
                eval_score = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                board.push(move)
                eval_score = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval
    
    def save_model(self, path):
        """Save model to file"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.model.save(path)
        print(f"✅ Model saved to {path}")
    
    def load_model(self, path):
        """Load model from file"""
        if os.path.exists(path):
            self.model = keras.models.load_model(path)
            print(f"✅ Model loaded from {path}")
            return True
        return False


class SelfPlayTrainer:
    """Train Chessy through self-play"""
    
    def __init__(self):
        self.chessy = ChessyNeuralNetwork()
        self.training_data = []
        self.results = {
            'self_play': {'games': 0, 'white_wins': 0, 'black_wins': 0, 'draws': 0},
            'vs_stockfish': {'games': 0, 'wins': 0, 'losses': 0, 'draws': 0},
            'training_history': []
        }
    
    def play_self_play_game(self, game_num):
        """Play one game of Chessy vs Chessy"""
        board = chess.Board()
        moves = []
        positions = []
        
        print(f"\n🎮 Self-Play Game {game_num}/{SELF_PLAY_GAMES}")
        
        while not board.is_game_over() and len(moves) < 200:
            # Get move from neural network
            move = self.chessy.get_best_move(board, depth=2)
            if not move:
                break
            
            # Store position and evaluation
            positions.append({
                'board': self.chessy.board_to_input(board),
                'eval': self.chessy.evaluate_position(board)
            })
            
            board.push(move)
            moves.append(move)
        
        # Determine result
        result = board.result()
        if result == "1-0":
            self.results['self_play']['white_wins'] += 1
            outcome = "White wins"
        elif result == "0-1":
            self.results['self_play']['black_wins'] += 1
            outcome = "Black wins"
        else:
            self.results['self_play']['draws'] += 1
            outcome = "Draw"
        
        self.results['self_play']['games'] += 1
        
        print(f"   Result: {outcome} ({len(moves)} moves)")
        
        # Store training data
        self.training_data.extend(positions)
        
        return result
    
    def train_from_self_play(self):
        """Train neural network from self-play games"""
        print(f"\n🧠 Training from {len(self.training_data)} positions...")
        
        if len(self.training_data) < 100:
            print("⚠️ Not enough training data")
            return
        
        # Prepare training data
        X = np.array([pos['board'] for pos in self.training_data])
        y = np.array([pos['eval'] for pos in self.training_data])
        
        # Train model
        history = self.chessy.model.fit(
            X, y,
            epochs=10,
            batch_size=32,
            validation_split=0.2,
            verbose=1
        )
        
        self.results['training_history'].append({
            'timestamp': datetime.now().isoformat(),
            'positions': len(self.training_data),
            'loss': float(history.history['loss'][-1]),
            'val_loss': float(history.history['val_loss'][-1])
        })
        
        print("✅ Training complete!")
    
    def play_vs_stockfish(self, game_num, stockfish_depth=10):
        """Play one game against Stockfish"""
        board = chess.Board()
        
        # Chessy plays white, Stockfish plays black
        chessy_white = game_num % 2 == 0
        
        print(f"\n⚔️ Game {game_num}/{STOCKFISH_TEST_GAMES} vs Stockfish (Depth {stockfish_depth})")
        print(f"   Chessy: {'White' if chessy_white else 'Black'}")
        
        with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
            while not board.is_game_over() and board.fullmove_number < 100:
                if (board.turn == chess.WHITE and chessy_white) or \
                   (board.turn == chess.BLACK and not chessy_white):
                    # Chessy's turn
                    move = self.chessy.get_best_move(board, depth=3)
                else:
                    # Stockfish's turn
                    result = engine.play(board, chess.engine.Limit(depth=stockfish_depth))
                    move = result.move
                
                if not move:
                    break
                
                board.push(move)
        
        # Determine result
        result = board.result()
        
        if result == "1-0":
            if chessy_white:
                self.results['vs_stockfish']['wins'] += 1
                outcome = "✅ Chessy wins!"
            else:
                self.results['vs_stockfish']['losses'] += 1
                outcome = "❌ Stockfish wins"
        elif result == "0-1":
            if not chessy_white:
                self.results['vs_stockfish']['wins'] += 1
                outcome = "✅ Chessy wins!"
            else:
                self.results['vs_stockfish']['losses'] += 1
                outcome = "❌ Stockfish wins"
        else:
            self.results['vs_stockfish']['draws'] += 1
            outcome = "🤝 Draw"
        
        self.results['vs_stockfish']['games'] += 1
        
        print(f"   Result: {outcome} ({board.fullmove_number} moves)")
        
        return result
    
    def calculate_elo(self):
        """Estimate ELO based on Stockfish results"""
        wins = self.results['vs_stockfish']['wins']
        losses = self.results['vs_stockfish']['losses']
        draws = self.results['vs_stockfish']['draws']
        total = wins + losses + draws
        
        if total == 0:
            return 0
        
        # Score: 1 for win, 0.5 for draw, 0 for loss
        score = (wins + 0.5 * draws) / total
        
        # Stockfish depth 10 ≈ 2400 ELO
        stockfish_elo = 2400
        
        # ELO difference formula: score = 1 / (1 + 10^(diff/400))
        # Solve for diff: diff = -400 * log10((1/score) - 1)
        if score > 0 and score < 1:
            elo_diff = -400 * np.log10((1/score) - 1)
            estimated_elo = stockfish_elo + elo_diff
        elif score == 1:
            estimated_elo = stockfish_elo + 200  # Dominated
        else:
            estimated_elo = stockfish_elo - 200  # Dominated
        
        return int(estimated_elo)
    
    def save_results(self):
        """Save results to JSON file"""
        os.makedirs(os.path.dirname(RESULTS_PATH), exist_ok=True)
        
        # Calculate ELO
        estimated_elo = self.calculate_elo()
        self.results['estimated_elo'] = estimated_elo
        self.results['timestamp'] = datetime.now().isoformat()
        
        with open(RESULTS_PATH, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n✅ Results saved to {RESULTS_PATH}")
    
    def print_summary(self):
        """Print training and testing summary"""
        print("\n" + "="*60)
        print("🏆 CHESSY 1.5 TRAINING COMPLETE")
        print("="*60)
        
        print("\n📊 Self-Play Results:")
        sp = self.results['self_play']
        print(f"   Games: {sp['games']}")
        print(f"   White wins: {sp['white_wins']}")
        print(f"   Black wins: {sp['black_wins']}")
        print(f"   Draws: {sp['draws']}")
        
        print("\n⚔️ vs Stockfish Results:")
        vs = self.results['vs_stockfish']
        print(f"   Games: {vs['games']}")
        print(f"   Wins: {vs['wins']}")
        print(f"   Losses: {vs['losses']}")
        print(f"   Draws: {vs['draws']}")
        
        if vs['games'] > 0:
            win_rate = (vs['wins'] + 0.5 * vs['draws']) / vs['games'] * 100
            print(f"   Win Rate: {win_rate:.1f}%")
        
        estimated_elo = self.calculate_elo()
        print(f"\n🎯 Estimated ELO: {estimated_elo}")
        
        print("\n" + "="*60)


def main():
    """Main training pipeline"""
    print("="*60)
    print("🚀 CHESSY 1.5 - SELF-PLAY TRAINING")
    print("="*60)
    
    trainer = SelfPlayTrainer()
    
    # Phase 1: Self-Play
    print(f"\n📍 PHASE 1: Self-Play Training ({SELF_PLAY_GAMES} games)")
    print("-"*60)
    
    for i in range(1, SELF_PLAY_GAMES + 1):
        trainer.play_self_play_game(i)
    
    # Phase 2: Train from self-play
    print(f"\n📍 PHASE 2: Learning from Self-Play")
    print("-"*60)
    trainer.train_from_self_play()
    
    # Save model after training
    trainer.chessy.save_model(MODEL_PATH)
    
    # Phase 3: Test against Stockfish
    print(f"\n📍 PHASE 3: Testing vs Stockfish ({STOCKFISH_TEST_GAMES} games)")
    print("-"*60)
    
    for i in range(1, STOCKFISH_TEST_GAMES + 1):
        try:
            trainer.play_vs_stockfish(i, stockfish_depth=10)
        except Exception as e:
            print(f"⚠️ Error in game {i}: {e}")
            continue
    
    # Save results
    trainer.save_results()
    
    # Print summary
    trainer.print_summary()
    
    print("\n✅ Training pipeline complete!")
    print(f"📁 Model saved to: {MODEL_PATH}")
    print(f"📁 Results saved to: {RESULTS_PATH}")


if __name__ == "__main__":
    main()
