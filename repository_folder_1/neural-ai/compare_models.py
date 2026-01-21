"""
Compare Chessy 1.0 vs Chessy 1.1
Play models against each other and track performance
"""

import chess
import numpy as np
import tensorflow as tf
from tensorflow import keras
import os
import json
from datetime import datetime

from chess_ai_server import board_to_array

class ModelComparison:
    """Compare two chess models"""
    
    def __init__(self, model1_path, model2_path, model1_name="Model 1", model2_name="Model 2"):
        print("=" * 70)
        print("♔ CHESS MODEL COMPARISON")
        print("=" * 70)
        
        # Load models
        print(f"\n📦 Loading {model1_name}...")
        try:
            self.model1 = keras.models.load_model(model1_path, compile=False)
            self.model1.compile(optimizer='adam', loss='mse', metrics=['mae'])
            print(f"   ✅ Loaded: {model1_path}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            self.model1 = None
        
        print(f"\n📦 Loading {model2_name}...")
        try:
            self.model2 = keras.models.load_model(model2_path, compile=False)
            self.model2.compile(optimizer='adam', loss='mse', metrics=['mae'])
            print(f"   ✅ Loaded: {model2_path}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            self.model2 = None
        
        self.model1_name = model1_name
        self.model2_name = model2_name
        
        self.results = {
            'model1_wins': 0,
            'model2_wins': 0,
            'draws': 0,
            'games': []
        }
    
    def evaluate_position(self, board, model):
        """Evaluate position using model"""
        board_array = board_to_array(board)
        board_array = np.expand_dims(board_array, axis=0)
        return float(model.predict(board_array, verbose=0)[0][0])
    
    def get_best_move(self, board, model, depth=1):
        """Get best move using model evaluation"""
        legal_moves = list(board.legal_moves)
        
        if not legal_moves:
            return None
        
        move_scores = []
        
        for move in legal_moves:
            board.push(move)
            
            # Check for immediate win/loss
            if board.is_checkmate():
                score = 10.0
            elif board.is_stalemate():
                score = 0.0
            else:
                score = -self.evaluate_position(board, model)
            
            board.pop()
            move_scores.append((move, score))
        
        # Select best move
        best_move = max(move_scores, key=lambda x: x[1])
        return best_move[0]
    
    def play_game(self, white_model, black_model, white_name, black_name, max_moves=200):
        """Play one game between two models"""
        board = chess.Board()
        move_count = 0
        
        print(f"\n🎮 Game: {white_name} (White) vs {black_name} (Black)")
        
        while not board.is_game_over() and move_count < max_moves:
            # Select model based on turn
            if board.turn == chess.WHITE:
                model = white_model
                player = white_name
            else:
                model = black_model
                player = black_name
            
            # Get move
            move = self.get_best_move(board, model)
            
            if move is None:
                break
            
            board.push(move)
            move_count += 1
            
            if move_count % 20 == 0:
                print(f"   Move {move_count}...")
        
        # Determine result
        if board.is_checkmate():
            winner = black_name if board.turn == chess.WHITE else white_name
            result = f"{winner} wins by checkmate"
            return winner, result, move_count
        elif board.is_stalemate():
            result = "Draw by stalemate"
            return "draw", result, move_count
        elif board.is_insufficient_material():
            result = "Draw by insufficient material"
            return "draw", result, move_count
        elif move_count >= max_moves:
            result = "Draw by move limit"
            return "draw", result, move_count
        else:
            result = "Draw"
            return "draw", result, move_count
    
    def run_match(self, num_games=10):
        """Run a match between the two models"""
        print("\n" + "=" * 70)
        print(f"🏆 MATCH: {self.model1_name} vs {self.model2_name}")
        print("=" * 70)
        print(f"   Games: {num_games}")
        print(f"   Format: Alternating colors")
        print("=" * 70)
        
        if self.model1 is None or self.model2 is None:
            print("\n❌ Cannot run match - models not loaded")
            return
        
        for game_num in range(num_games):
            print(f"\n--- Game {game_num + 1}/{num_games} ---")
            
            # Alternate colors
            if game_num % 2 == 0:
                white_model = self.model1
                black_model = self.model2
                white_name = self.model1_name
                black_name = self.model2_name
            else:
                white_model = self.model2
                black_model = self.model1
                white_name = self.model2_name
                black_name = self.model1_name
            
            # Play game
            winner, result, moves = self.play_game(
                white_model, black_model,
                white_name, black_name
            )
            
            print(f"   ✅ {result} after {moves} moves")
            
            # Update results
            if winner == self.model1_name:
                self.results['model1_wins'] += 1
            elif winner == self.model2_name:
                self.results['model2_wins'] += 1
            else:
                self.results['draws'] += 1
            
            self.results['games'].append({
                'game_num': game_num + 1,
                'white': white_name,
                'black': black_name,
                'winner': winner,
                'result': result,
                'moves': moves
            })
            
            # Print current score
            self.print_score()
        
        # Final results
        self.print_final_results()
        self.save_results()
    
    def print_score(self):
        """Print current score"""
        total = self.results['model1_wins'] + self.results['model2_wins'] + self.results['draws']
        
        print(f"\n   📊 Score after {total} games:")
        print(f"      {self.model1_name}: {self.results['model1_wins']}")
        print(f"      {self.model2_name}: {self.results['model2_wins']}")
        print(f"      Draws: {self.results['draws']}")
    
    def print_final_results(self):
        """Print final match results"""
        print("\n" + "=" * 70)
        print("🏆 FINAL RESULTS")
        print("=" * 70)
        
        total = len(self.results['games'])
        m1_wins = self.results['model1_wins']
        m2_wins = self.results['model2_wins']
        draws = self.results['draws']
        
        print(f"\n{self.model1_name}: {m1_wins}/{total} ({m1_wins/total*100:.1f}%)")
        print(f"{self.model2_name}: {m2_wins}/{total} ({m2_wins/total*100:.1f}%)")
        print(f"Draws: {draws}/{total} ({draws/total*100:.1f}%)")
        
        # Determine winner
        if m1_wins > m2_wins:
            print(f"\n🎉 {self.model1_name} WINS THE MATCH!")
            margin = m1_wins - m2_wins
            print(f"   Margin: +{margin} games")
        elif m2_wins > m1_wins:
            print(f"\n🎉 {self.model2_name} WINS THE MATCH!")
            margin = m2_wins - m1_wins
            print(f"   Margin: +{margin} games")
        else:
            print(f"\n🤝 MATCH TIED!")
        
        # Performance rating
        m1_score = m1_wins + draws * 0.5
        m2_score = m2_wins + draws * 0.5
        
        print(f"\n📈 Performance Score:")
        print(f"   {self.model1_name}: {m1_score}/{total} ({m1_score/total*100:.1f}%)")
        print(f"   {self.model2_name}: {m2_score}/{total} ({m2_score/total*100:.1f}%)")
    
    def save_results(self):
        """Save match results to file"""
        filename = f"match_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        results_data = {
            'model1': self.model1_name,
            'model2': self.model2_name,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'summary': {
                'model1_wins': self.results['model1_wins'],
                'model2_wins': self.results['model2_wins'],
                'draws': self.results['draws'],
                'total_games': len(self.results['games'])
            },
            'games': self.results['games']
        }
        
        with open(filename, 'w') as f:
            json.dump(results_data, f, indent=2)
        
        print(f"\n💾 Results saved: {filename}")


def main():
    """Main comparison function"""
    
    print("\n" + "=" * 70)
    print("♔ CHESSY 1.0 vs CHESSY 1.1 COMPARISON")
    print("=" * 70)
    
    # Check which models are available
    models_available = []
    
    if os.path.exists('chess_model_basic.h5'):
        models_available.append(('chess_model_basic.h5', 'Chessy 1.0 (Basic)'))
    
    if os.path.exists('chess_model_selfplay_final.h5'):
        models_available.append(('chess_model_selfplay_final.h5', 'Chessy 1.0 (Self-Play)'))
    
    if os.path.exists('chess_model_magnus_basic.h5'):
        models_available.append(('chess_model_magnus_basic.h5', 'Chessy 1.1 (Magnus)'))
    
    if os.path.exists('chess_model_magnus_deep.h5'):
        models_available.append(('chess_model_magnus_deep.h5', 'Chessy 1.1 (Magnus Deep)'))
    
    print("\n📦 Available models:")
    for i, (path, name) in enumerate(models_available, 1):
        print(f"   {i}. {name} ({path})")
    
    if len(models_available) < 2:
        print("\n⚠️ Need at least 2 models to compare!")
        print("   Train models first, then run this script.")
        return
    
    # For now, compare first two available models
    model1_path, model1_name = models_available[0]
    model2_path, model2_name = models_available[-1]  # Last one (likely Magnus)
    
    print(f"\n🎯 Comparing:")
    print(f"   Model 1: {model1_name}")
    print(f"   Model 2: {model2_name}")
    
    # Run comparison
    comparison = ModelComparison(model1_path, model2_path, model1_name, model2_name)
    comparison.run_match(num_games=10)


if __name__ == "__main__":
    main()
