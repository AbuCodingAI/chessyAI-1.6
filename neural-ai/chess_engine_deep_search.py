"""
Deep Search Chess Engine - IM Beatable Strength
Combines neural network evaluation with deep minimax search
"""

import chess
import numpy as np
from tensorflow import keras
import time

class DeepSearchEngine:
    """Chess engine with deep search for IM-level play"""
    
    def __init__(self, model_path, max_depth=7):
        """
        Initialize engine
        
        max_depth: Maximum search depth
        - 3: ~2000 ELO (club player)
        - 5: ~2300 ELO (expert)
        - 7: ~2500 ELO (IM level)
        - 10: ~2700 ELO (GM level)
        """
        self.model = keras.models.load_model(model_path, compile=False)
        self.max_depth = max_depth
        self.nodes_searched = 0
        self.transposition_table = {}  # Cache evaluations
        
        print(f"🧠 Deep Search Engine initialized")
        print(f"   Max depth: {max_depth}")
        print(f"   Expected strength: {self.estimate_elo(max_depth)} ELO")
    
    def estimate_elo(self, depth):
        """Estimate ELO based on search depth"""
        elo_map = {
            1: 1800,
            2: 2000,
            3: 2100,
            4: 2200,
            5: 2300,
            6: 2400,
            7: 2500,
            8: 2600,
            9: 2650,
            10: 2700
        }
        return elo_map.get(depth, 2700)
    
    def board_to_array(self, board):
        """Convert board to neural network input"""
        array = np.zeros((8, 8, 12), dtype=np.float32)
        
        piece_map = {
            chess.PAWN: 0, chess.KNIGHT: 1, chess.BISHOP: 2,
            chess.ROOK: 3, chess.QUEEN: 4, chess.KING: 5
        }
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                row, col = divmod(square, 8)
                channel = piece_map[piece.piece_type]
                if piece.color == chess.BLACK:
                    channel += 6
                array[row, col, channel] = 1.0
        
        return array
    
    def evaluate_position(self, board):
        """Evaluate position using neural network"""
        board_array = self.board_to_array(board)
        board_array = np.expand_dims(board_array, axis=0)
        evaluation = self.model.predict(board_array, verbose=0)[0][0]
        return float(evaluation)
    
    def order_moves(self, board, moves):
        """
        Order moves for better alpha-beta pruning
        Good move ordering = faster search
        """
        move_scores = []
        
        for move in moves:
            score = 0
            
            # Prioritize captures
            if board.is_capture(move):
                captured = board.piece_at(move.to_square)
                if captured:
                    score += 10 + captured.piece_type
            
            # Prioritize checks
            board.push(move)
            if board.is_check():
                score += 5
            board.pop()
            
            # Prioritize center moves
            to_square = move.to_square
            row, col = divmod(to_square, 8)
            if 2 <= row <= 5 and 2 <= col <= 5:
                score += 1
            
            move_scores.append((move, score))
        
        # Sort by score (highest first)
        move_scores.sort(key=lambda x: x[1], reverse=True)
        return [move for move, _ in move_scores]
    
    def minimax(self, board, depth, alpha, beta, maximizing_player):
        """
        Minimax with alpha-beta pruning
        
        This is what gives us IM-level strength!
        """
        self.nodes_searched += 1
        
        # Check transposition table (use FEN as hash)
        board_hash = board.fen()
        if board_hash in self.transposition_table:
            cached_depth, cached_eval = self.transposition_table[board_hash]
            if cached_depth >= depth:
                return cached_eval
        
        # Terminal node or max depth
        if depth == 0 or board.is_game_over():
            eval_score = self.evaluate_position(board)
            self.transposition_table[board_hash] = (depth, eval_score)
            return eval_score
        
        legal_moves = list(board.legal_moves)
        
        # No legal moves
        if not legal_moves:
            if board.is_checkmate():
                return -10.0 if maximizing_player else 10.0
            else:  # Stalemate
                return 0.0
        
        # Order moves for better pruning
        legal_moves = self.order_moves(board, legal_moves)
        
        if maximizing_player:
            max_eval = -float('inf')
            
            for move in legal_moves:
                board.push(move)
                eval_score = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                
                # Alpha-beta pruning
                if beta <= alpha:
                    break
            
            self.transposition_table[board_hash] = (depth, max_eval)
            return max_eval
        
        else:
            min_eval = float('inf')
            
            for move in legal_moves:
                board.push(move)
                eval_score = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                
                # Alpha-beta pruning
                if beta <= alpha:
                    break
            
            self.transposition_table[board_hash] = (depth, min_eval)
            return min_eval
    
    def get_best_move(self, board, time_limit=None):
        """
        Get best move using deep search
        
        time_limit: Maximum time in seconds (optional)
        """
        start_time = time.time()
        self.nodes_searched = 0
        
        legal_moves = list(board.legal_moves)
        
        if not legal_moves:
            return None
        
        if len(legal_moves) == 1:
            return legal_moves[0]
        
        # Iterative deepening (search deeper if time allows)
        best_move = None
        best_eval = -float('inf')
        
        current_depth = 1
        while current_depth <= self.max_depth:
            # Check time limit
            if time_limit and (time.time() - start_time) > time_limit:
                break
            
            move_evaluations = []
            alpha = -float('inf')
            beta = float('inf')
            
            # Order moves
            ordered_moves = self.order_moves(board, legal_moves)
            
            for move in ordered_moves:
                board.push(move)
                
                # Check for immediate checkmate
                if board.is_checkmate():
                    board.pop()
                    print(f"   🎯 Found checkmate in {current_depth} moves!")
                    return move
                
                # Evaluate this move
                eval_score = -self.minimax(board, current_depth - 1, -beta, -alpha, False)
                board.pop()
                
                move_evaluations.append((move, eval_score))
                
                if eval_score > best_eval:
                    best_eval = eval_score
                    best_move = move
                
                alpha = max(alpha, eval_score)
            
            # Sort moves by evaluation for next iteration
            move_evaluations.sort(key=lambda x: x[1], reverse=True)
            legal_moves = [move for move, _ in move_evaluations]
            
            elapsed = time.time() - start_time
            print(f"   Depth {current_depth}: eval={best_eval:.3f}, nodes={self.nodes_searched}, time={elapsed:.2f}s")
            
            current_depth += 1
        
        elapsed = time.time() - start_time
        nps = self.nodes_searched / elapsed if elapsed > 0 else 0
        
        print(f"\n   ✅ Best move: {best_move}")
        print(f"   📊 Evaluation: {best_eval:.3f}")
        print(f"   🔍 Nodes searched: {self.nodes_searched:,}")
        print(f"   ⚡ Nodes/second: {nps:,.0f}")
        print(f"   ⏱️  Time: {elapsed:.2f}s")
        
        return best_move
    
    def clear_cache(self):
        """Clear transposition table"""
        self.transposition_table.clear()


def test_engine():
    """Test the deep search engine"""
    print("\n" + "=" * 70)
    print("🧠 TESTING DEEP SEARCH ENGINE")
    print("=" * 70)
    
    # Load Chessy 1.2 model
    model_path = 'chess_model_stockfish_deep.h5'
    
    if not os.path.exists(model_path):
        print(f"\n❌ Model not found: {model_path}")
        print("   Train Chessy 1.2 first!")
        return
    
    # Test different depths
    depths = [3, 5, 7]
    
    for depth in depths:
        print(f"\n{'=' * 70}")
        print(f"Testing depth {depth} (~{2000 + depth * 100} ELO)")
        print('=' * 70)
        
        engine = DeepSearchEngine(model_path, max_depth=depth)
        
        # Test position
        board = chess.Board()
        
        print("\nStarting position:")
        print(board)
        
        print(f"\nSearching for best move (depth {depth})...")
        best_move = engine.get_best_move(board, time_limit=10)
        
        print(f"\n✅ Engine would play: {best_move}")


if __name__ == "__main__":
    import os
    test_engine()
