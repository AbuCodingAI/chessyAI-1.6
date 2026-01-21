"""
Self-Play Training with Game Review
AI plays against itself and learns from its games
"""

import chess
import numpy as np
import tensorflow as tf
from tensorflow import keras
import os
import json
from datetime import datetime
from collections import deque
import random

from chess_ai_server import board_to_array, create_basic_cnn, material_evaluation

class SelfPlayTrainer:
    def __init__(self, model_path=None):
        """Initialize self-play trainer"""
        if model_path and os.path.exists(model_path):
            print(f"📦 Loading existing model: {model_path}")
            try:
                self.model = keras.models.load_model(model_path, compile=False)
                # Recompile with correct settings
                self.model.compile(optimizer='adam', loss='mse', metrics=['mae'])
                print("✅ Model loaded and recompiled successfully")
            except Exception as e:
                print(f"⚠️ Could not load model: {e}")
                print("🆕 Creating new model instead")
                self.model = create_basic_cnn()
        else:
            print("🆕 Creating new model")
            self.model = create_basic_cnn()
        
        self.replay_buffer = deque(maxlen=50000)  # Store game positions
        self.games_played = 0
        self.training_iterations = 0
        
    def evaluate_position(self, board):
        """Evaluate position using current model"""
        board_array = board_to_array(board)
        board_array = np.expand_dims(board_array, axis=0)
        return float(self.model.predict(board_array, verbose=0)[0][0])
    
    def select_move_mcts_lite(self, board, temperature=1.0, simulations=50):
        """
        Select move using simplified MCTS (Monte Carlo Tree Search)
        temperature: higher = more exploration
        """
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None
        
        move_scores = []
        
        for move in legal_moves:
            # Simulate move
            board.push(move)
            
            # Quick evaluation
            if board.is_checkmate():
                score = 10.0  # Winning move
            elif board.is_stalemate():
                score = 0.0
            else:
                # Run mini simulations
                total_score = 0
                for _ in range(simulations):
                    sim_score = self.simulate_random_playout(board.copy(), depth=10)
                    total_score += sim_score
                score = -total_score / simulations  # Negative because opponent's turn
            
            board.pop()
            move_scores.append((move, score))
        
        # Apply temperature for exploration
        if temperature > 0:
            scores = np.array([s for _, s in move_scores])
            scores = scores / temperature
            # Softmax
            exp_scores = np.exp(scores - np.max(scores))
            probs = exp_scores / np.sum(exp_scores)
            
            move_idx = np.random.choice(len(move_scores), p=probs)
            return move_scores[move_idx][0], probs
        else:
            # Greedy selection
            best_move = max(move_scores, key=lambda x: x[1])
            return best_move[0], None
    
    def simulate_random_playout(self, board, depth=10):
        """Simulate random game to evaluate position"""
        for _ in range(depth):
            if board.is_game_over():
                break
            
            legal_moves = list(board.legal_moves)
            if not legal_moves:
                break
            
            move = random.choice(legal_moves)
            board.push(move)
        
        # Evaluate final position
        return self.evaluate_position(board)
    
    def play_game(self, temperature_schedule=None):
        """
        Play one game against itself
        temperature_schedule: dict mapping move_number -> temperature
        """
        board = chess.Board()
        game_positions = []  # Store (board_state, move_probs, player)
        move_number = 0
        
        print(f"\n🎮 Playing game {self.games_played + 1}...")
        
        while not board.is_game_over() and move_number < 200:
            # Determine temperature (more exploration early, less later)
            if temperature_schedule:
                temp = temperature_schedule.get(move_number, 0.1)
            else:
                if move_number < 10:
                    temp = 1.5  # High exploration in opening
                elif move_number < 30:
                    temp = 1.0  # Medium exploration in middlegame
                else:
                    temp = 0.5  # Low exploration in endgame
            
            # Select move
            move, probs = self.select_move_mcts_lite(board, temperature=temp, simulations=30)
            
            if move is None:
                break
            
            # Store position before move
            game_positions.append({
                'board': board.copy(),
                'move': move,
                'player': board.turn,
                'move_number': move_number
            })
            
            # Make move
            board.push(move)
            move_number += 1
            
            if move_number % 10 == 0:
                print(f"  Move {move_number}...")
        
        # Game over - determine outcome
        if board.is_checkmate():
            winner = not board.turn  # Previous player won
            result = 1.0 if winner == chess.WHITE else -1.0
            outcome = "Checkmate"
        elif board.is_stalemate():
            result = 0.0
            outcome = "Stalemate"
        elif board.is_insufficient_material():
            result = 0.0
            outcome = "Insufficient Material"
        else:
            result = 0.0
            outcome = "Draw"
        
        print(f"  ✅ Game finished: {outcome} after {move_number} moves")
        
        # Review game and assign values to positions
        self.review_game(game_positions, result)
        
        self.games_played += 1
        return result, move_number, outcome
    
    def review_game(self, game_positions, final_result):
        """
        Review game and assign values to each position
        Uses outcome + position evaluation
        """
        print(f"  📊 Reviewing game...")
        
        for i, pos_data in enumerate(game_positions):
            board = pos_data['board']
            player = pos_data['player']
            move_number = pos_data['move_number']
            
            # Value from game outcome (discounted by moves to end)
            moves_to_end = len(game_positions) - i
            discount = 0.99 ** moves_to_end
            outcome_value = final_result * discount
            
            # Adjust for player perspective
            if player == chess.BLACK:
                outcome_value = -outcome_value
            
            # Blend outcome with current model evaluation
            current_eval = self.evaluate_position(board)
            blended_value = 0.7 * outcome_value + 0.3 * current_eval
            
            # Store in replay buffer
            self.replay_buffer.append({
                'board_array': board_to_array(board),
                'value': blended_value,
                'move_number': move_number
            })
        
        print(f"  💾 Added {len(game_positions)} positions to replay buffer")
    
    def train_on_replay_buffer(self, batch_size=64, epochs=5):
        """Train model on collected game data"""
        if len(self.replay_buffer) < batch_size:
            print(f"⚠️ Not enough data in replay buffer ({len(self.replay_buffer)} < {batch_size})")
            return
        
        print(f"\n🧠 Training on replay buffer ({len(self.replay_buffer)} positions)...")
        
        # Sample from replay buffer
        sample_size = min(len(self.replay_buffer), 10000)
        samples = random.sample(list(self.replay_buffer), sample_size)
        
        X_train = np.array([s['board_array'] for s in samples])
        y_train = np.array([s['value'] for s in samples])
        
        # Train
        history = self.model.fit(
            X_train, y_train,
            batch_size=batch_size,
            epochs=epochs,
            validation_split=0.2,
            verbose=1
        )
        
        self.training_iterations += 1
        
        print(f"  ✅ Training iteration {self.training_iterations} complete")
        print(f"     Loss: {history.history['loss'][-1]:.4f}")
        print(f"     Val Loss: {history.history['val_loss'][-1]:.4f}")
        
        return history
    
    def save_model(self, path="chess_model_selfplay.h5"):
        """Save current model"""
        self.model.save(path)
        
        # Save training info
        info = {
            'games_played': self.games_played,
            'training_iterations': self.training_iterations,
            'replay_buffer_size': len(self.replay_buffer),
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        info_path = path.replace('.h5', '_info.json')
        with open(info_path, 'w') as f:
            json.dump(info, f, indent=2)
        
        print(f"\n💾 Model saved: {path}")
        print(f"   Info saved: {info_path}")
    
    def run_training_loop(self, num_games=100, train_every=10, save_every=25):
        """
        Main training loop
        num_games: total games to play
        train_every: train model every N games
        save_every: save model every N games
        """
        print("=" * 70)
        print("♔ SELF-PLAY TRAINING WITH GAME REVIEW")
        print("=" * 70)
        print(f"Games to play: {num_games}")
        print(f"Train every: {train_every} games")
        print(f"Save every: {save_every} games")
        print("=" * 70)
        
        results = []
        
        for game_num in range(num_games):
            # Play game
            result, moves, outcome = self.play_game()
            results.append({'result': result, 'moves': moves, 'outcome': outcome})
            
            # Train periodically
            if (game_num + 1) % train_every == 0:
                self.train_on_replay_buffer(batch_size=64, epochs=3)
            
            # Save periodically
            if (game_num + 1) % save_every == 0:
                self.save_model(f"chess_model_selfplay_gen{game_num + 1}.h5")
                self.print_statistics(results)
        
        # Final save
        self.save_model("chess_model_selfplay_final.h5")
        
        print("\n" + "=" * 70)
        print("🎉 TRAINING COMPLETE!")
        print("=" * 70)
        self.print_statistics(results)
    
    def print_statistics(self, results):
        """Print training statistics"""
        white_wins = sum(1 for r in results if r['result'] > 0.5)
        black_wins = sum(1 for r in results if r['result'] < -0.5)
        draws = sum(1 for r in results if abs(r['result']) <= 0.5)
        avg_moves = np.mean([r['moves'] for r in results])
        
        print(f"\n📊 Statistics (last {len(results)} games):")
        print(f"   White wins: {white_wins} ({white_wins/len(results)*100:.1f}%)")
        print(f"   Black wins: {black_wins} ({black_wins/len(results)*100:.1f}%)")
        print(f"   Draws: {draws} ({draws/len(results)*100:.1f}%)")
        print(f"   Avg moves: {avg_moves:.1f}")
        print(f"   Replay buffer: {len(self.replay_buffer)} positions")


def main():
    """Main training function"""
    
    # Configuration
    NUM_GAMES = 100  # Start with 100 games
    TRAIN_EVERY = 5  # Train every 5 games
    SAVE_EVERY = 25  # Save every 25 games
    
    # Load existing model or start fresh
    if os.path.exists('chess_model_basic.h5'):
        print("📦 Loading your trained model as starting point...")
        trainer = SelfPlayTrainer('chess_model_basic.h5')
    else:
        print("🆕 Starting with fresh model...")
        trainer = SelfPlayTrainer()
    
    # Run training
    trainer.run_training_loop(
        num_games=NUM_GAMES,
        train_every=TRAIN_EVERY,
        save_every=SAVE_EVERY
    )
    
    print("\n🎮 Your AI is now trained through self-play!")
    print("📁 Use chess_model_selfplay_final.h5 in your server")


if __name__ == "__main__":
    main()
