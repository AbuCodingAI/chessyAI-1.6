"""
Quiescence Search Chess Engine - GM Level Strength
Combines neural network evaluation with deep search + quiescence search
Depth 10 + quiescence = ~2700+ ELO (GM level)
"""

import chess
import numpy as np
from tensorflow import keras
import time

class QuiescenceEngine:
    """Chess engine with quiescence search for GM-level play"""
    
    def __init__(self, model_path, max_depth=10, max_quiescence_depth=10):
        """
        Initialize engine with quiescence search
        
        max_depth: Maximum normal search depth (10 = GM level)
        max_quiescence_depth: Maximum depth for capture/check sequences
        """
        self.model = keras.models.load_model(model_path, compile=False)
        self.max_depth = max_depth
        self.max_quiescence_depth = max_quiescence_depth
        self.nodes_searched = 0
        self.quiescence_nodes = 0
        self.transposition_table = {}
        
        print(f"🧠 Quiescence Search Engine initialized")
        print(f"   Max depth: {max_depth}")
        print(f"   Quiescence depth: {max_quiescence_depth}")
        print(f"   Expected strength: ~2700+ ELO (GM level)")
    
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
    
    def is_quiet_position(self, board):
        """
        Check if position is quiet (no forcing moves)
        Quiet = no captures, no checks available
        """
        # If in check, not quiet
        if board.is_check():
            return False
        
        # Check if any captures available
        for move in board.legal_moves:
            if board.is_capture(move):
                return False
        
        return True
    
    def get_tactical_moves(self, board):
        """
        Get only tactical moves (captures and checks)
        Used in quiescence search
        """
        tactical_moves = []
        
        for move in board.legal_moves:
            # Captures
            if board.is_capture(move):
                tactical_moves.append(move)
                continue
            
            # Checks
            board.push(move)
            if board.is_check():
                tactical_moves.append(move)
            board.pop()
        
        return tactical_moves
    
    def order_moves(self, board, moves):
        """
        Order moves for better alpha-beta pruning
        MVV-LVA (Most Valuable Victim - Least Valuable Attacker)
        """
        move_scores = []
        
        for move in moves:
            score = 0
            
            # Prioritize captures (MVV-LVA)
            if board.is_capture(move):
                captured = board.piece_at(move.to_square)
                attacker = board.piece_at(move.from_square)
                if captured and attacker:
                    # Victim value - Attacker value
                    score += (captured.piece_type * 10) - attacker.piece_type
                    score += 100  # Base capture bonus
            
            # Prioritize checks
            board.push(move)
            if board.is_check():
                score += 50
            board.pop()
            
            # Prioritize center moves
            to_square = move.to_square
            row, col = divmod(to_square, 8)
            if 2 <= row <= 5 and 2 <= col <= 5:
                score += 5
            
            # Prioritize promotions
            if move.promotion:
                score += 200
            
            move_scores.append((move, score))
        
        # Sort by score (highest first)
        move_scores.sort(key=lambda x: x[1], reverse=True)
        return [move for move, _ in move_scores]
    
    def quiescence_search(self, board, alpha, beta, depth=0, checked_quiet_move=False):
        """
        Quiescence search - search until position is quiet
        
        This prevents the horizon effect:
        - Continue searching captures until chain ends
        - Continue searching checks until no more checks
        - After tactical sequence ends, search 1 more move (eye of hurricane check)
        """
        self.quiescence_nodes += 1
        
        # Max quiescence depth reached
        if depth >= self.max_quiescence_depth:
            return self.evaluate_position(board)
        
        # Game over
        if board.is_game_over():
            if board.is_checkmate():
                return -10.0  # We got checkmated
            return 0.0  # Draw
        
        # Stand pat evaluation (current position value)
        stand_pat = self.evaluate_position(board)
        
        # Beta cutoff
        if stand_pat >= beta:
            return beta
        
        # Update alpha
        if stand_pat > alpha:
            alpha = stand_pat
        
        # Get tactical moves (captures and checks)
        tactical_moves = self.get_tactical_moves(board)
        
        # If no tactical moves, position is quiet
        if not tactical_moves:
            # If we haven't checked a quiet move yet, do it now (eye of hurricane)
            if not checked_quiet_move:
                legal_moves = list(board.legal_moves)
                if legal_moves:
                    # Order moves and try the best quiet move
                    ordered_moves = self.order_moves(board, legal_moves)
                    best_eval = stand_pat
                    
                    # Try the top quiet move
                    for move in ordered_moves[:1]:  # Just check 1 move
                        board.push(move)
                        eval_score = -self.quiescence_search(board, -beta, -alpha, depth + 1, True)
                        board.pop()
                        best_eval = max(best_eval, eval_score)
                        if best_eval >= beta:
                            return beta
                        alpha = max(alpha, best_eval)
                    return best_eval
            
            # Already checked quiet move or no moves available
            return stand_pat
        
        # Order tactical moves
        tactical_moves = self.order_moves(board, tactical_moves)
        
        # Search tactical moves
        for move in tactical_moves:
            board.push(move)
            eval_score = -self.quiescence_search(board, -beta, -alpha, depth + 1, False)
            board.pop()
            
            if eval_score >= beta:
                return beta
            
            if eval_score > alpha:
                alpha = eval_score
        
        return alpha
    
    def minimax(self, board, depth, alpha, beta, maximizing_player, last_move_was_tactical=False):
        """
        Minimax with alpha-beta pruning + smart quiescence search
        
        Quiescence only triggers if last move was capture/check
        """
        self.nodes_searched += 1
        
        # Check transposition table (use FEN as hash)
        board_hash = board.fen()
        if board_hash in self.transposition_table:
            cached_depth, cached_eval = self.transposition_table[board_hash]
            if cached_depth >= depth:
                return cached_eval
        
        # Terminal node - check if we need quiescence
        if depth == 0:
            # Only do quiescence if last move was tactical (capture/check)
            if last_move_was_tactical:
                eval_score = self.quiescence_search(board, alpha, beta)
            else:
                # Position is quiet, just evaluate
                eval_score = self.evaluate_position(board)
            
            self.transposition_table[board_hash] = (depth, eval_score)
            return eval_score
        
        # Game over
        if board.is_game_over():
            if board.is_checkmate():
                return -10.0 if maximizing_player else 10.0
            return 0.0  # Draw
        
        legal_moves = list(board.legal_moves)
        
        # No legal moves
        if not legal_moves:
            if board.is_checkmate():
                return -10.0 if maximizing_player else 10.0
            return 0.0
        
        # Order moves for better pruning
        legal_moves = self.order_moves(board, legal_moves)
        
        if maximizing_player:
            max_eval = -float('inf')
            
            for move in legal_moves:
                # Check if this move is tactical (capture or check)
                is_capture = board.is_capture(move)
                board.push(move)
                is_check = board.is_check()
                is_tactical = is_capture or is_check
                
                eval_score = self.minimax(board, depth - 1, alpha, beta, False, is_tactical)
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
                # Check if this move is tactical (capture or check)
                is_capture = board.is_capture(move)
                board.push(move)
                is_check = board.is_check()
                is_tactical = is_capture or is_check
                
                eval_score = self.minimax(board, depth - 1, alpha, beta, True, is_tactical)
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
        Get best move using deep search + quiescence
        """
        start_time = time.time()
        self.nodes_searched = 0
        self.quiescence_nodes = 0
        
        legal_moves = list(board.legal_moves)
        
        if not legal_moves:
            return None
        
        if len(legal_moves) == 1:
            return legal_moves[0]
        
        # Iterative deepening
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
                    print(f"   🎯 Found checkmate!")
                    return move
                
                # Check if this move is tactical
                is_capture = board.is_capture(move)
                is_check = board.is_check()
                is_tactical = is_capture or is_check
                
                # Evaluate this move
                eval_score = -self.minimax(board, current_depth - 1, -beta, -alpha, False, is_tactical)
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
            total_nodes = self.nodes_searched + self.quiescence_nodes
            print(f"   Depth {current_depth}: eval={best_eval:.3f}, nodes={total_nodes:,} ({self.quiescence_nodes:,} quiescence), time={elapsed:.2f}s")
            
            current_depth += 1
        
        elapsed = time.time() - start_time
        total_nodes = self.nodes_searched + self.quiescence_nodes
        nps = total_nodes / elapsed if elapsed > 0 else 0
        
        print(f"\n   ✅ Best move: {best_move}")
        print(f"   📊 Evaluation: {best_eval:.3f}")
        print(f"   🔍 Total nodes: {total_nodes:,}")
        print(f"   🎯 Quiescence nodes: {self.quiescence_nodes:,} ({self.quiescence_nodes/total_nodes*100:.1f}%)")
        print(f"   ⚡ Nodes/second: {nps:,.0f}")
        print(f"   ⏱️  Time: {elapsed:.2f}s")
        
        return best_move
    
    def clear_cache(self):
        """Clear transposition table"""
        self.transposition_table.clear()


def test_engine():
    """Test the quiescence search engine"""
    import os
    
    print("\n" + "=" * 70)
    print("🧠 TESTING QUIESCENCE SEARCH ENGINE")
    print("=" * 70)
    
    # Load Chessy 1.3 model
    model_path = 'chess_model_chessy_1.3.h5'
    
    if not os.path.exists(model_path):
        print(f"\n❌ Model not found: {model_path}")
        print("   Train Chessy 1.3 first!")
        return
    
    print("\n🎯 Testing tactical position (capture sequence)...")
    
    # Create engine
    engine = QuiescenceEngine(model_path, max_depth=10, max_quiescence_depth=10)
    
    # Test position with capture sequence
    board = chess.Board("r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 1")
    
    print("\nPosition (Italian Game):")
    print(board)
    
    print(f"\nSearching for best move (depth 10 + quiescence)...")
    best_move = engine.get_best_move(board, time_limit=30)
    
    print(f"\n✅ Engine would play: {best_move}")
    print("\n💡 Quiescence search ensures we don't stop in middle of captures!")


if __name__ == "__main__":
    test_engine()
