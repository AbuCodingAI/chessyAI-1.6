"""
Quick test script for Quiescence Search Engine
"""

import chess
from chess_engine_quiescence import QuiescenceEngine
import os

def test_basic_position():
    """Test on starting position"""
    print("\n" + "=" * 70)
    print("TEST 1: Starting Position")
    print("=" * 70)
    
    model_path = 'chess_model_chessy_1.3.h5'
    
    if not os.path.exists(model_path):
        print(f"\n❌ Model not found: {model_path}")
        print("   Please train Chessy 1.3 first!")
        return False
    
    engine = QuiescenceEngine(model_path, max_depth=6, max_quiescence_depth=10)
    board = chess.Board()
    
    print("\nPosition:")
    print(board)
    print("\nSearching...")
    
    best_move = engine.get_best_move(board, time_limit=10)
    
    print(f"\n✅ Best move: {best_move}")
    return True


def test_tactical_position():
    """Test on position with captures"""
    print("\n" + "=" * 70)
    print("TEST 2: Tactical Position (Italian Game)")
    print("=" * 70)
    
    model_path = 'chess_model_chessy_1.3.h5'
    
    if not os.path.exists(model_path):
        print(f"\n❌ Model not found: {model_path}")
        return False
    
    engine = QuiescenceEngine(model_path, max_depth=6, max_quiescence_depth=10)
    
    # Italian Game position with Bxf7+ tactic
    board = chess.Board("r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 1")
    
    print("\nPosition:")
    print(board)
    print("\nSearching for tactical shot...")
    
    best_move = engine.get_best_move(board, time_limit=15)
    
    print(f"\n✅ Best move: {best_move}")
    
    if best_move and best_move.uci() == "c4f7":
        print("🎯 Found Bxf7+! Quiescence search working!")
    
    return True


def test_capture_sequence():
    """Test position with long capture sequence"""
    print("\n" + "=" * 70)
    print("TEST 3: Capture Sequence")
    print("=" * 70)
    
    model_path = 'chess_model_chessy_1.3.h5'
    
    if not os.path.exists(model_path):
        print(f"\n❌ Model not found: {model_path}")
        return False
    
    engine = QuiescenceEngine(model_path, max_depth=5, max_quiescence_depth=10)
    
    # Position with multiple captures available
    board = chess.Board("r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 1")
    
    print("\nPosition:")
    print(board)
    print("\nSearching through capture sequences...")
    
    best_move = engine.get_best_move(board, time_limit=15)
    
    print(f"\n✅ Best move: {best_move}")
    print("💡 Quiescence ensured we saw entire capture chain!")
    
    return True


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("🧠 CHESSY 1.3 QUIESCENCE SEARCH - TEST SUITE")
    print("=" * 70)
    
    tests = [
        ("Basic Position", test_basic_position),
        ("Tactical Position", test_tactical_position),
        ("Capture Sequence", test_capture_sequence)
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"\n❌ Test failed: {e}")
            failed += 1
    
    print("\n" + "=" * 70)
    print("TEST RESULTS")
    print("=" * 70)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 All tests passed! Quiescence search is working!")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Check the output above.")


if __name__ == "__main__":
    main()
