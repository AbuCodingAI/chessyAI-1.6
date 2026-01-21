"""
Chessy 1.4 - The Bongcloud Grandmaster
Plays the worst opening (Bongcloud), then plays like a 2800 ELO GM

The ultimate disrespect: "I'll give you a free advantage and still beat you"
"""

import chess
import chess.engine
import numpy as np
from tensorflow import keras
import random

# STOCKFISH PATH
STOCKFISH_PATH = r"C:\Users\Abu\Downloads\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe"

class BongcloudGrandmaster:
    """The most disrespectful AI ever created"""
    
    def __init__(self, model_path=None, stockfish_path=STOCKFISH_PATH):
        self.name = "Chessy 1.4 - Bongcloud GM"
        self.rating = "2800 ELO (after Bongcloud)"
        self.style = "Maximum Disrespect"
        
        print("=" * 70)
        print("👑 CHESSY 1.4 - THE BONGCLOUD GRANDMASTER")
        print("=" * 70)
        print("\n🤡 Opening: Bongcloud Attack (1.e4 e5 2.Ke2)")
        print("💪 Middlegame: 2800 ELO Grandmaster level")
        print("🏆 Goal: Win despite terrible opening")
        print("\n⚠️ Ultimate disrespect: 'I'll spot you a king move and still win'")
        print("=" * 70)
        
        # Load neural network
        if model_path and os.path.exists(model_path):
            print(f"\n📦 Loading neural network: {model_path}")
            self.model = keras.models.load_model(model_path, compile=False)
            self.model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        else:
            print("\n⚠️ No model loaded, will use Stockfish only")
            self.model = None
        
        # Start Stockfish for GM-level play
        try:
            print(f"\n🚀 Starting Stockfish (GM brain)...")
            self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
            print(f"   ✅ Stockfish ready!")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            self.engine = None
    
    def get_move(self, board, time_limit=5):
        """
        Get move with Bongcloud opening, then GM play
        
        Strategy:
        - Moves 1-3: Play Bongcloud (terrible)
        - Moves 4+: Play like 2800 ELO GM (Stockfish depth 20)
        """
        move_number = board.fullmove_number
        
        # Phase 1: The Bongcloud (Moves 1-3)
        if move_number <= 3:
            return self.play_bongcloud(board, move_number)
        
        # Phase 2: GM Mode (Moves 4+)
        return self.play_gm_mode(board, time_limit)
    
    def play_bongcloud(self, board, move_number):
        """Play the Bongcloud Attack"""
        
        bongcloud_moves = {
            1: 'e2e4',  # 1. e4
            2: 'e1e2',  # 2. Ke2!! (The Bongcloud!)
            3: 'e2f3',  # 3. Kf3!!! (Double Bongcloud!)
        }
        
        if board.turn == chess.WHITE:
            move_uci = bongcloud_moves.get(move_number)
            
            if move_uci:
                try:
                    move = chess.Move.from_uci(move_uci)
                    if move in board.legal_moves:
                        if move_number == 2:
                            print("\n🤡 BONGCLOUD ATTACK!")
                            print("   'Ke2!! - The most powerful move in chess'")
                            print("   - Hikaru Nakamura (probably)")
                        elif move_number == 3:
                            print("\n👑 DOUBLE BONGCLOUD!")
                            print("   'Kf3!!! - Assert dominance'")
                            print("   'My king is a warrior, not a coward'")
                        return move
                except:
                    pass
        
        # If Bongcloud not possible, play random
        legal_moves = list(board.legal_moves)
        return random.choice(legal_moves) if legal_moves else None
    
    def play_gm_mode(self, board, time_limit):
        """Play like a 2800 ELO GM using Stockfish"""
        
        if self.engine is None:
            print("⚠️ No engine, playing random")
            legal_moves = list(board.legal_moves)
            return random.choice(legal_moves) if legal_moves else None
        
        print("\n💪 GM MODE ACTIVATED")
        print("   Calculating with Stockfish depth 20...")
        
        # Use Stockfish at high depth
        result = self.engine.play(board, chess.engine.Limit(time=time_limit, depth=20))
        
        print(f"   ✅ Best move found: {result.move.uci()}")
        
        # Analyze position
        info = self.engine.analyse(board, chess.engine.Limit(depth=15))
        score = info["score"].relative
        
        if score.is_mate():
            print(f"   🎯 Mate in {abs(score.mate())}!")
        else:
            cp = score.score()
            print(f"   📊 Evaluation: {cp/100:+.2f} pawns")
        
        return result.move
    
    def taunt_by_phase(self, move_number):
        """Taunts based on game phase"""
        
        if move_number == 1:
            return "🤡 Let's start with something spicy..."
        elif move_number == 2:
            return "👑 BONGCLOUD! Your move, coward."
        elif move_number == 3:
            return "🚀 Double Bongcloud! I'm unstoppable!"
        elif move_number == 4:
            return "💪 Okay, playtime's over. GM mode activated."
        elif move_number == 10:
            return "🎯 Despite the Bongcloud, I'm winning. Skill issue?"
        elif move_number == 20:
            return "🏆 Told you. Bongcloud is unbeatable."
        else:
            taunts = [
                "😎 Bongcloud advantage is real.",
                "🧠 My king is better placed than yours.",
                "💀 You're losing to a Bongcloud. Embarrassing.",
                "🎪 This is what peak performance looks like.",
                "👑 King on f3 is objectively best.",
            ]
            return random.choice(taunts)
    
    def close(self):
        """Close engine"""
        if self.engine:
            self.engine.quit()


def train_bongcloud_recovery():
    """
    Train AI to recover from terrible openings
    
    Strategy:
    1. Start with Bongcloud (terrible position)
    2. Use Stockfish to find best moves from there
    3. Train neural network on recovery positions
    """
    print("\n" + "=" * 70)
    print("🎓 TRAINING: BONGCLOUD RECOVERY")
    print("=" * 70)
    print("\nTeaching AI to win despite terrible openings")
    print("Time: ~2 hours")
    print("=" * 70)
    
    try:
        engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
    except:
        print("\n❌ Stockfish not found!")
        return
    
    X_train = []
    y_train = []
    
    print("\n🤡 Generating Bongcloud recovery positions...")
    
    # Generate 1000 games starting from Bongcloud
    for game_num in range(1000):
        if game_num % 50 == 0:
            print(f"   Game {game_num}/1000...")
        
        board = chess.Board()
        
        # Play Bongcloud
        board.push(chess.Move.from_uci('e2e4'))  # 1. e4
        board.push(chess.Move.from_uci('e7e5'))  # 1... e5
        board.push(chess.Move.from_uci('e1e2'))  # 2. Ke2!! (Bongcloud!)
        
        # Now play with Stockfish from this terrible position
        for move_count in range(40):
            if board.is_game_over():
                break
            
            # Stockfish finds best move
            result = engine.play(board, chess.engine.Limit(depth=15))
            board.push(result.move)
            
            # Store position (after move 5)
            if move_count > 5:
                # Evaluate position
                info = engine.analyse(board, chess.engine.Limit(depth=18))
                score = info["score"].relative
                
                if score.is_mate():
                    eval_score = 1.0 if score.mate() > 0 else -1.0
                else:
                    eval_score = np.tanh(score.score() / 400.0)
                
                X_train.append(board_to_array(board))
                y_train.append(eval_score)
    
    engine.quit()
    
    print(f"\n✅ Generated {len(X_train)} recovery positions")
    
    # Train model
    print("\n🧠 Training recovery model...")
    
    from chess_ai_server import create_deep_cnn
    
    model = create_deep_cnn()
    
    X_train = np.array(X_train)
    y_train = np.array(y_train)
    
    history = model.fit(
        X_train, y_train,
        epochs=30,
        batch_size=64,
        validation_split=0.2,
        verbose=1
    )
    
    model.save('chess_model_bongcloud_gm.h5')
    
    print("\n✅ Bongcloud GM model trained!")
    print("   This AI can recover from terrible openings!")

def board_to_array(board):
    """Convert board to array"""
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


def main():
    """Main function"""
    print("\n" + "=" * 70)
    print("👑 CHESSY 1.4 - THE BONGCLOUD GRANDMASTER")
    print("=" * 70)
    print("\nThe ultimate disrespect AI:")
    print("  1. Plays Bongcloud (worst opening)")
    print("  2. Switches to GM mode (2800 ELO)")
    print("  3. Wins anyway")
    print("\n🎯 Goal: Maximum disrespect, maximum skill")
    print("🏆 Rating: 2800 ELO (despite Bongcloud)")
    
    print("\n" + "=" * 70)
    print("OPTIONS")
    print("=" * 70)
    print("\n1. 🎮 Watch demo game")
    print("2. 🎓 Train Bongcloud recovery model")
    print("3. 🤡 Just show me the memes")
    
    choice = input("\nSelect (1/2/3): ").strip()
    
    if choice == '1':
        play_demo_game()
    elif choice == '2':
        train_bongcloud_recovery()
    else:
        chocker = BongcloudGrandmaster()
        openings = chocker.get_opening_book()
        
        print("\n🤡 MEME OPENINGS:")
        for opening in openings.values():
            print(f"\n{opening['name']}")
            print(f"  {opening['description']}")


if __name__ == "__main__":
    import os
    main()
