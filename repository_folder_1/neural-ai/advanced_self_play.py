"""
Advanced Self-Play with Full MCTS and Policy Network
More sophisticated version with move policy learning
"""

import chess
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import layers
import os
import json
from datetime import datetime
from collections import deque, defaultdict
import random
import math

from chess_ai_server import board_to_array

class PolicyValueNetwork:
    """
    Combined policy and value network (like AlphaZero)
    - Policy head: predicts move probabilities
    - Value head: predicts position evaluation
    """
    
    def __init__(self):
        self.model = self.create_model()
    
    def create_model(self):
        """Create policy-value network"""
        inputs = keras.Input(shape=(8, 8, 12))
        
        # Shared layers
        x = layers.Conv2D(128, 3, padding='same', activation='relu')(inputs)
        x = layers.Conv2D(128, 3, padding='same', activation='relu')(x)
        x = layers.Conv2D(128, 3, padding='same', activation='relu')(x)
        
        # Residual blocks
        for _ in range(5):
            residual = x
            x = layers.Conv2D(128, 3, padding='same', activation='relu')(x)
            x = layers.Conv2D(128, 3, padding='same')(x)
            x = layers.Add()([x, residual])
            x = layers.Activation('relu')(x)
        
        # Policy head (move probabilities)
        policy = layers.Conv2D(32, 1, activation='relu')(x)
        policy = layers.Flatten()(policy)
        policy = layers.Dense(4096, activation='softmax', name='policy')(policy)  # 64*64 possible moves
        
        # Value head (position evaluation)
        value = layers.Conv2D(32, 1, activation='relu')(x)
        value = layers.Flatten()(value)
        value = layers.Dense(128, activation='relu')(value)
        value = layers.Dense(1, activation='tanh', name='value')(value)
        
        model = keras.Model(inputs=inputs, outputs=[policy, value])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss={'policy': 'categorical_crossentropy', 'value': 'mse'},
            loss_weights={'policy': 1.0, 'value': 1.0}
        )
        
        return model
    
    def predict(self, board_array):
        """Predict policy and value"""
        board_array = np.expand_dims(board_array, axis=0)
        policy, value = self.model.predict(board_array, verbose=0)
        return policy[0], value[0][0]
    
    def save(self, path):
        """Save model"""
        self.model.save(path)
    
    def load(self, path):
        """Load model"""
        self.model = keras.models.load_model(path)


class MCTSNode:
    """Node in Monte Carlo Tree Search"""
    
    def __init__(self, board, parent=None, move=None, prior=0):
        self.board = board.copy()
        self.parent = parent
        self.move = move  # Move that led to this node
        self.prior = prior  # Prior probability from policy network
        
        self.children = {}
        self.visit_count = 0
        self.value_sum = 0
        self.is_expanded = False
    
    def value(self):
        """Average value of this node"""
        if self.visit_count == 0:
            return 0
        return self.value_sum / self.visit_count
    
    def uct_score(self, parent_visit_count, c_puct=1.5):
        """
        Upper Confidence Bound for Trees
        Balances exploitation (value) and exploration (prior * sqrt(parent_visits / visits))
        """
        if self.visit_count == 0:
            return float('inf')
        
        exploitation = self.value()
        exploration = c_puct * self.prior * math.sqrt(parent_visit_count) / (1 + self.visit_count)
        
        return exploitation + exploration
    
    def select_child(self, c_puct=1.5):
        """Select best child using UCT"""
        return max(self.children.values(), 
                   key=lambda child: child.uct_score(self.visit_count, c_puct))
    
    def expand(self, policy_network):
        """Expand node by adding children for all legal moves"""
        if self.is_expanded:
            return
        
        legal_moves = list(self.board.legal_moves)
        if not legal_moves:
            self.is_expanded = True
            return
        
        # Get policy predictions
        board_array = board_to_array(self.board)
        policy_probs, _ = policy_network.predict(board_array)
        
        # Create child nodes
        for move in legal_moves:
            # Convert move to policy index (simplified)
            move_idx = move.from_square * 64 + move.to_square
            prior = policy_probs[move_idx] if move_idx < len(policy_probs) else 0.001
            
            child_board = self.board.copy()
            child_board.push(move)
            
            self.children[move] = MCTSNode(child_board, parent=self, move=move, prior=prior)
        
        self.is_expanded = True
    
    def backup(self, value):
        """Backup value through tree"""
        self.visit_count += 1
        self.value_sum += value
        
        if self.parent:
            self.parent.backup(-value)  # Negate for opponent


class AdvancedSelfPlayTrainer:
    """Advanced self-play trainer with full MCTS"""
    
    def __init__(self, model_path=None):
        if model_path and os.path.exists(model_path):
            print(f"📦 Loading model: {model_path}")
            self.network = PolicyValueNetwork()
            self.network.load(model_path)
        else:
            print("🆕 Creating new policy-value network")
            self.network = PolicyValueNetwork()
        
        self.replay_buffer = deque(maxlen=100000)
        self.games_played = 0
    
    def mcts_search(self, board, num_simulations=200):
        """
        Run MCTS to find best move
        Returns: move probabilities based on visit counts
        """
        root = MCTSNode(board)
        root.expand(self.network)
        
        # Run simulations
        for _ in range(num_simulations):
            node = root
            search_path = [node]
            
            # Selection: traverse tree using UCT
            while node.is_expanded and node.children:
                node = node.select_child()
                search_path.append(node)
            
            # Expansion
            if not node.board.is_game_over():
                node.expand(self.network)
                if node.children:
                    node = random.choice(list(node.children.values()))
                    search_path.append(node)
            
            # Evaluation
            board_array = board_to_array(node.board)
            _, value = self.network.predict(board_array)
            
            # Backup
            for node in reversed(search_path):
                node.backup(value)
                value = -value  # Flip for opponent
        
        # Return move probabilities based on visit counts
        move_probs = {}
        total_visits = sum(child.visit_count for child in root.children.values())
        
        for move, child in root.children.items():
            move_probs[move] = child.visit_count / total_visits if total_visits > 0 else 0
        
        return move_probs
    
    def play_game(self, num_simulations=100):
        """Play one game using MCTS"""
        board = chess.Board()
        game_data = []
        move_number = 0
        
        print(f"\n🎮 Playing game {self.games_played + 1} with MCTS...")
        
        while not board.is_game_over() and move_number < 200:
            # Run MCTS
            move_probs = self.mcts_search(board, num_simulations)
            
            if not move_probs:
                break
            
            # Store training data
            game_data.append({
                'board': board_to_array(board),
                'policy': self.move_probs_to_array(move_probs),
                'player': board.turn
            })
            
            # Select move (with temperature for exploration)
            temperature = 1.0 if move_number < 30 else 0.1
            move = self.select_move_with_temperature(move_probs, temperature)
            
            board.push(move)
            move_number += 1
            
            if move_number % 20 == 0:
                print(f"  Move {move_number}...")
        
        # Determine outcome
        if board.is_checkmate():
            result = 1.0 if not board.turn else -1.0
        else:
            result = 0.0
        
        print(f"  ✅ Game finished after {move_number} moves")
        
        # Add outcome to all positions
        for data in game_data:
            data['value'] = result if data['player'] == chess.WHITE else -result
            self.replay_buffer.append(data)
        
        self.games_played += 1
        return result, move_number
    
    def move_probs_to_array(self, move_probs):
        """Convert move probabilities dict to array"""
        policy_array = np.zeros(4096)
        for move, prob in move_probs.items():
            idx = move.from_square * 64 + move.to_square
            if idx < 4096:
                policy_array[idx] = prob
        return policy_array
    
    def select_move_with_temperature(self, move_probs, temperature):
        """Select move using temperature"""
        moves = list(move_probs.keys())
        probs = np.array([move_probs[m] for m in moves])
        
        if temperature == 0:
            return moves[np.argmax(probs)]
        
        probs = probs ** (1 / temperature)
        probs = probs / np.sum(probs)
        
        return np.random.choice(moves, p=probs)
    
    def train(self, batch_size=64, epochs=5):
        """Train network on replay buffer"""
        if len(self.replay_buffer) < batch_size:
            return
        
        print(f"\n🧠 Training on {len(self.replay_buffer)} positions...")
        
        samples = random.sample(list(self.replay_buffer), min(len(self.replay_buffer), 10000))
        
        X = np.array([s['board'] for s in samples])
        y_policy = np.array([s['policy'] for s in samples])
        y_value = np.array([s['value'] for s in samples])
        
        history = self.network.model.fit(
            X, {'policy': y_policy, 'value': y_value},
            batch_size=batch_size,
            epochs=epochs,
            validation_split=0.2,
            verbose=1
        )
        
        print(f"  ✅ Training complete")
        return history
    
    def run_training(self, num_games=50, train_every=5):
        """Run advanced training loop"""
        print("=" * 70)
        print("♔ ADVANCED SELF-PLAY WITH MCTS")
        print("=" * 70)
        
        for game_num in range(num_games):
            self.play_game(num_simulations=100)
            
            if (game_num + 1) % train_every == 0:
                self.train(batch_size=64, epochs=3)
                self.network.save(f"chess_model_advanced_gen{game_num + 1}.h5")
        
        self.network.save("chess_model_advanced_final.h5")
        print("\n🎉 Advanced training complete!")


def main():
    """Run advanced training"""
    trainer = AdvancedSelfPlayTrainer()
    trainer.run_training(num_games=50, train_every=5)


if __name__ == "__main__":
    main()
