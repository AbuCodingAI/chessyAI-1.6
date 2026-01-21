"""
STOCKFISH VS STOCKFISH WITH BLUNDERS
Generate high-quality training data by having Stockfish play against itself with intentional blunders

Process:
1. White: Stockfish (depth 20) - always plays perfectly
2. Black: Stockfish (depth 20) - but 15% of moves are BLUNDERS (hangs pieces)
3. Collect ONLY clean positions (before blunders)
4. Re-evaluate all positions with Stockfish (depth 25) for accurate labels
5. Save positions and evaluations for training

This teaches Chessy to:
- Punish opponent mistakes
- Exploit hanging pieces
- Convert advantages into wins
- Play like a strong tactical player

The blunders create realistic training scenarios where the opponent makes mistakes.
"""

import chess
import chess.engine
import numpy as np
import json
import os
from datetime import datetime
import random

# Configuration
NUM_GAMES = 100
STOCKFISH_PATH = "../stockfish/stockfish-windows-x86-64-avx2.exe"
CLEAN_DEPTH = 25  # Depth for clean evaluation
PLAY_DEPTH = 20   # Depth for playing moves
NOISE_PROBABILITY = 0.15  # 15% chance Black makes a blunder (hangs a piece)
OUTPUT_PATH = "training_data/stockfish_positions.json"

class StockfishDataGenerator:
    """Generate training data from Stockfish self-play"""
    
    def __init__(self):
        self.positions = []
        self.games_played = 0
        self.stats = {
            'total_games': 0,
            'total_positions': 0,
            'white_wins': 0,
            'black_wins': 0,
            'draws': 0,
            'avg_moves_per_game': 0
        }
    
    def add_noise_to_move(self, engine, board, depth):
        """
        Get move with noise (intentional blunders):
        - 85% of time: best move (depth 20) - returns (move, False)
        - 15% of time: BAD move that hangs a piece - returns (move, True)
        
        This teaches Chessy to punish opponent mistakes!
        
        Returns: (move, is_noise)
        """
        if random.random() < NOISE_PROBABILITY:
            # Make a blunder: find moves that hang pieces
            legal_moves = list(board.legal_moves)
            bad_moves = []
            
            for move in legal_moves:
                board.push(move)
                
                # Check if this move hangs a piece
                # Look at opponent's captures
                opponent_captures = [m for m in board.legal_moves if board.is_capture(m)]
                
                if opponent_captures:
                    # Evaluate how bad this move is
                    for capture in opponent_captures:
                        captured_square = capture.to_square
                        piece = board.piece_at(captured_square)
                        if piece:
                            # Piece values
                            piece_values = {
                                chess.PAWN: 1,
                                chess.KNIGHT: 3,
                                chess.BISHOP: 3,
                                chess.ROOK: 5,
                                chess.QUEEN: 9
                            }
                            value = piece_values.get(piece.piece_type, 0)
                            if value > 0:
                                bad_moves.append((move, value))
                
                board.pop()
            
            # If we found bad moves, pick one that hangs a valuable piece
            if bad_moves:
                # Sort by piece value (prefer hanging more valuable pieces)
                bad_moves.sort(key=lambda x: x[1], reverse=True)
                # Pick from top 3 worst moves
                worst_moves = bad_moves[:min(3, len(bad_moves))]
                selected_move = random.choice(worst_moves)[0]
                return (selected_move, True)  # This is a blunder
            
            # If no hanging moves found, just pick a random legal move
            return (random.choice(legal_moves), True)
        
        # No noise: get best move at full depth
        result = engine.play(board, chess.engine.Limit(depth=depth))
        return (result.move, False)  # This is a clean move
    
    def evaluate_position(self, engine, board):
        """
        Evaluate position with clean Stockfish (depth 25)
        Returns evaluation in centipawns
        """
        try:
            info = engine.analyse(board, chess.engine.Limit(depth=CLEAN_DEPTH))
            score = info['score'].relative
            
            # Convert to centipawns
            if score.is_mate():
                # Mate score: convert to large number
                mate_in = score.mate()
                if mate_in > 0:
                    cp_score = 10000 - (mate_in * 100)
                else:
                    cp_score = -10000 - (mate_in * 100)
            else:
                cp_score = score.score()
            
            # Normalize to -1 to 1 range (tanh-like)
            normalized = np.tanh(cp_score / 400.0)
            
            return {
                'centipawns': cp_score,
                'normalized': float(normalized),
                'is_mate': score.is_mate()
            }
        except Exception as e:
            print(f"⚠️ Evaluation error: {e}")
            return {'centipawns': 0, 'normalized': 0.0, 'is_mate': False}
    
    def board_to_features(self, board):
        """Convert board to feature representation"""
        # 768 features: 64 squares * 12 piece types
        features = np.zeros(768)
        
        piece_map = {
            chess.PAWN: 0, chess.KNIGHT: 1, chess.BISHOP: 2,
            chess.ROOK: 3, chess.QUEEN: 4, chess.KING: 5
        }
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                piece_type = piece_map[piece.piece_type]
                offset = piece_type if piece.color == chess.WHITE else piece_type + 6
                features[square * 12 + offset] = 1
        
        return features.tolist()
    
    def play_game(self, game_num, engine):
        """Play one game of Stockfish vs Stockfish with noise"""
        board = chess.Board()
        game_positions = []
        
        print(f"\n🎮 Game {game_num}/{NUM_GAMES}")
        
        move_count = 0
        noise_moves = 0
        while not board.is_game_over() and move_count < 200:
            # BOTH sides can make blunders (15% chance each)
            move, is_noise_move = self.add_noise_to_move(engine, board, PLAY_DEPTH)
            
            if is_noise_move:
                noise_moves += 1
            
            # ONLY collect position if it's NOT a noise move
            if not is_noise_move:
                # Store position BEFORE move (for training)
                position_data = {
                    'fen': board.fen(),
                    'features': self.board_to_features(board),
                    'move_number': board.fullmove_number,
                    'turn': 'white' if board.turn == chess.WHITE else 'black',
                    'is_clean': True  # Mark as clean position
                }
                
                # Evaluate position with clean Stockfish
                evaluation = self.evaluate_position(engine, board)
                position_data['evaluation'] = evaluation
                
                game_positions.append(position_data)
            
            board.push(move)
            move_count += 1
        
        # Game result
        result = board.result()
        if result == "1-0":
            self.stats['white_wins'] += 1
            outcome = "White wins"
        elif result == "0-1":
            self.stats['black_wins'] += 1
            outcome = "Black wins"
        else:
            self.stats['draws'] += 1
            outcome = "Draw"
        
        print(f"   Result: {outcome} ({move_count} moves)")
        print(f"   Collected: {len(game_positions)} clean positions ({noise_moves} blunders excluded)")
        
        # Add to dataset
        self.positions.extend(game_positions)
        self.stats['total_games'] += 1
        self.stats['total_positions'] += len(game_positions)
        
        return game_positions
    
    def save_dataset(self):
        """Save collected positions to JSON file"""
        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
        
        # Calculate statistics
        if self.stats['total_games'] > 0:
            self.stats['avg_moves_per_game'] = self.stats['total_positions'] / self.stats['total_games']
        
        dataset = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'stockfish_depth_play': PLAY_DEPTH,
                'stockfish_depth_eval': CLEAN_DEPTH,
                'noise_probability': NOISE_PROBABILITY,
                'num_games': NUM_GAMES
            },
            'statistics': self.stats,
            'positions': self.positions
        }
        
        with open(OUTPUT_PATH, 'w') as f:
            json.dump(dataset, f, indent=2)
        
        print(f"\n✅ Dataset saved to {OUTPUT_PATH}")
        print(f"   Total positions: {len(self.positions)}")
        print(f"   File size: {os.path.getsize(OUTPUT_PATH) / 1024 / 1024:.2f} MB")
    
    def print_summary(self):
        """Print generation summary"""
        print("\n" + "="*70)
        print("📊 TRAINING DATA GENERATION COMPLETE")
        print("="*70)
        
        print(f"\n🎮 Games Played: {self.stats['total_games']}")
        print(f"   White wins: {self.stats['white_wins']}")
        print(f"   Black wins: {self.stats['black_wins']}")
        print(f"   Draws: {self.stats['draws']}")
        
        print(f"\n📦 Dataset Statistics:")
        print(f"   Total positions: {self.stats['total_positions']}")
        print(f"   Avg moves/game: {self.stats['avg_moves_per_game']:.1f}")
        
        # Sample evaluation distribution
        if self.positions:
            evals = [p['evaluation']['centipawns'] for p in self.positions]
            print(f"\n📈 Evaluation Distribution:")
            print(f"   Min: {min(evals)} cp")
            print(f"   Max: {max(evals)} cp")
            print(f"   Mean: {np.mean(evals):.1f} cp")
            print(f"   Median: {np.median(evals):.1f} cp")
        
        print("\n" + "="*70)


def main():
    """Main data generation pipeline"""
    print("="*70)
    print("🚀 STOCKFISH TRAINING DATA GENERATOR")
    print("="*70)
    print(f"\nConfiguration:")
    print(f"   Games: {NUM_GAMES}")
    print(f"   Play Depth: {PLAY_DEPTH}")
    print(f"   Eval Depth: {CLEAN_DEPTH}")
    print(f"   Blunder Probability: {NOISE_PROBABILITY * 100}% (Black hangs pieces)")
    print(f"\nEstimated time: {NUM_GAMES * 2} minutes")
    print("-"*70)
    
    generator = StockfishDataGenerator()
    
    # Open Stockfish engine
    print(f"\n🔧 Starting Stockfish engine...")
    with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
        print(f"✅ Stockfish ready: {engine.id['name']}")
        
        # Generate games
        print(f"\n📍 Generating {NUM_GAMES} games...")
        print("-"*70)
        
        for game_num in range(1, NUM_GAMES + 1):
            try:
                generator.play_game(game_num, engine)
                
                # Save progress every 10 games
                if game_num % 10 == 0:
                    generator.save_dataset()
                    print(f"\n💾 Progress saved ({game_num}/{NUM_GAMES} games)")
            
            except Exception as e:
                print(f"⚠️ Error in game {game_num}: {e}")
                continue
    
    # Final save
    generator.save_dataset()
    
    # Print summary
    generator.print_summary()
    
    print("\n✅ Data generation complete!")
    print(f"📁 Dataset saved to: {OUTPUT_PATH}")
    print(f"\n💡 Next step: Train Chessy 1.5 with this data")
    print(f"   python TRAIN_CHESSY_1.5_FROM_STOCKFISH.py")


if __name__ == "__main__":
    main()
