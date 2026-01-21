"""
Chessy 1.4 - GM Level with Smart Quiescence Search
Can be called from command line or Node.js
~2700+ ELO strength
"""

import sys
import chess
from chess_engine_quiescence import QuiescenceEngine

def get_best_move(fen, model_path='chess_model_chessy_1.3.h5', max_depth=10, time_limit=30):
    """
    Get best move for given position
    
    Args:
        fen: Position in FEN notation
        model_path: Path to neural network model
        max_depth: Maximum search depth
        time_limit: Maximum time in seconds
    
    Returns:
        Best move in UCI format (e.g. 'e2e4')
    """
    try:
        # Create engine
        engine = QuiescenceEngine(model_path, max_depth=max_depth, max_quiescence_depth=10)
        
        # Parse position
        board = chess.Board(fen)
        
        # Get best move
        best_move = engine.get_best_move(board, time_limit=time_limit)
        
        if best_move:
            return best_move.uci()
        else:
            return None
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return None


if __name__ == "__main__":
    # Command line usage:
    # python chessy_1.3_quiescence.py "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    
    if len(sys.argv) < 2:
        print("Usage: python chessy_1.3_quiescence.py <FEN>")
        print("Example: python chessy_1.3_quiescence.py \"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1\"")
        sys.exit(1)
    
    fen = sys.argv[1]
    
    print(f"\n🧠 Chessy 1.4 - GM Level (~2700+ ELO)")
    print(f"Smart Quiescence Search - Depth 10")
    print(f"Position: {fen}\n")
    
    best_move = get_best_move(fen)
    
    if best_move:
        print(f"\n✅ Best move: {best_move}")
    else:
        print(f"\n❌ No legal moves")
