"""
Chess AI Training Script
Generates training data using Stockfish and trains the neural network
"""

import chess
import chess.pgn
import chess.engine
import numpy as np
import tensorflow as tf
from tensorflow import keras
import os
import json
from datetime import datetime
import requests
import gzip
import io

# Import model functions from server
from chess_ai_server import board_to_array, create_basic_cnn, create_deep_cnn, create_residual_model

# Configuration
STOCKFISH_PATH = "stockfish.exe"  # Update this path
TRAINING_POSITIONS = 10000  # Number of positions to generate
BATCH_SIZE = 64
EPOCHS = 20
MODEL_TYPE = "basic"  # basic, deep, or residual

def download_lichess_games(num_games=100000):
    """Download sample games from lichess"""
    print(f"📥 Downloading {num_games} games from lichess...")
    
    # Lichess database URL (monthly database)
    # For testing, we'll use a smaller sample
    url = "https://lichess.org/api/games/user/thibault?max=10000&pgnInJson=false"
    
    try:
        response = requests.get(url, headers={"Accept": "application/x-chess-pgn"})
        if response.status_code == 200:
            return response.text
        else:
            print(f"⚠️ Could not download games: {response.status_code}")
            return None
    except Exception as e:
        print(f"⚠️ Error downloading games: {e}")
        return None

def parse_pgn_games(pgn_text):
    """Parse PGN text and extract games"""
    games = []
    pgn_io = io.StringIO(pgn_text)
    
    while True:
        game = chess.pgn.read_game(pgn_io)
        if game is None:
            break
        games.append(game)
    
    return games

def generate_positions_from_games(games, max_positions=10000):
    """Extract positions from games"""
    print(f"📊 Extracting positions from {len(games)} games...")
    positions = []
    
    for game in games:
        board = game.board()
        for move in game.mainline_moves():
            board.push(move)
            
            # Skip opening positions (first 5 moves)
            if board.fullmove_number < 5:
                continue
            
            # Skip endgame positions with too few pieces
            if len(board.piece_map()) < 8:
                continue
            
            positions.append(board.copy())
            
            if len(positions) >= max_positions:
                return positions
    
    return positions

def evaluate_with_stockfish(board, engine, depth=15):
    """Evaluate position using Stockfish"""
    try:
        info = engine.analyse(board, chess.engine.Limit(depth=depth))
        score = info["score"].relative
        
        # Convert to normalized value (-1 to 1)
        if score.is_mate():
            # Mate score
            mate_in = score.mate()
            return 1.0 if mate_in > 0 else -1.0
        else:
            # Centipawn score, normalize to roughly -1 to 1
            cp = score.score()
            return np.tanh(cp / 400.0)
    except:
        return 0.0

def generate_training_data_stockfish(num_positions=1000, stockfish_path=None):
    """Generate training data using Stockfish self-play"""
    print(f"🤖 Generating {num_positions} positions using Stockfish...")
    
    if stockfish_path is None or not os.path.exists(stockfish_path):
        print("⚠️ Stockfish not found. Using random positions with material evaluation.")
        return generate_random_training_data(num_positions)
    
    try:
        engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
    except Exception as e:
        print(f"⚠️ Could not start Stockfish: {e}")
        return generate_random_training_data(num_positions)
    
    X_train = []
    y_train = []
    
    positions_per_game = 20
    num_games = num_positions // positions_per_game
    
    for game_num in range(num_games):
        if game_num % 10 == 0:
            print(f"  Game {game_num}/{num_games}...")
        
        board = chess.Board()
        
        # Play a game
        for move_num in range(positions_per_game):
            if board.is_game_over():
                break
            
            # Get Stockfish's move
            result = engine.play(board, chess.engine.Limit(depth=5))
            board.push(result.move)
            
            # Evaluate position
            evaluation = evaluate_with_stockfish(board, engine, depth=10)
            
            # Store position and evaluation
            X_train.append(board_to_array(board))
            y_train.append(evaluation)
    
    engine.quit()
    
    return np.array(X_train), np.array(y_train)

def generate_random_training_data(num_positions=1000):
    """Generate random positions (fallback method)"""
    print(f"🎲 Generating {num_positions} random positions...")
    print(f"💡 TIP: Download Stockfish for 10x better training quality!")
    
    X_train = []
    y_train = []
    
    for i in range(num_positions):
        if i % 100 == 0:
            print(f"  Position {i}/{num_positions}...")
        
        board = chess.Board()
        
        # Make random moves (varied game phases)
        num_moves = np.random.randint(10, 40)
        for _ in range(num_moves):
            if board.is_game_over():
                break
            
            legal_moves = list(board.legal_moves)
            if not legal_moves:
                break
            
            move = np.random.choice(legal_moves)
            board.push(move)
        
        # Enhanced evaluation (material + basic positional)
        evaluation = enhanced_evaluation(board)
        
        X_train.append(board_to_array(board))
        y_train.append(evaluation)
    
    return np.array(X_train), np.array(y_train)

def enhanced_evaluation(board):
    """Better evaluation than just material"""
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3.25,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
    }
    
    score = 0
    
    # Material count
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = piece_values[piece.piece_type]
            
            # Positional bonuses
            rank = chess.square_rank(square)
            file = chess.square_file(square)
            
            # Center control bonus
            if 2 <= rank <= 5 and 2 <= file <= 5:
                value += 0.1
            
            # Pawn advancement bonus
            if piece.piece_type == chess.PAWN:
                if piece.color == chess.WHITE:
                    value += rank * 0.1
                else:
                    value += (7 - rank) * 0.1
            
            score += value if piece.color == chess.WHITE else -value
    
    # Mobility bonus (more legal moves = better)
    mobility = len(list(board.legal_moves))
    score += mobility * 0.01 if board.turn == chess.WHITE else -mobility * 0.01
    
    # King safety penalty if in check
    if board.is_check():
        score += -0.5 if board.turn == chess.WHITE else 0.5
    
    # Normalize to -1 to 1
    return np.tanh(score / 12.0)

def material_evaluation(board):
    """Simple material evaluation"""
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
    }
    
    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = piece_values[piece.piece_type]
            score += value if piece.color == chess.WHITE else -value
    
    # Normalize to -1 to 1
    return np.tanh(score / 10.0)

def train_model(X_train, y_train, model_type="basic", epochs=20):
    """Train the neural network"""
    print(f"\n🧠 Training {model_type} model...")
    print(f"  Training samples: {len(X_train)}")
    print(f"  Epochs: {epochs}")
    
    # Create model
    if model_type == "basic":
        model = create_basic_cnn()
    elif model_type == "deep":
        model = create_deep_cnn()
    elif model_type == "residual":
        model = create_residual_model()
    else:
        raise ValueError(f"Unknown model type: {model_type}")
    
    # Split data
    split_idx = int(len(X_train) * 0.8)
    X_train_split = X_train[:split_idx]
    y_train_split = y_train[:split_idx]
    X_val = X_train[split_idx:]
    y_val = y_train[split_idx:]
    
    # Callbacks
    callbacks = [
        keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True),
        keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=3),
        keras.callbacks.ModelCheckpoint(
            f'chess_model_{model_type}_best.h5',
            save_best_only=True,
            monitor='val_loss'
        )
    ]
    
    # Train
    history = model.fit(
        X_train_split, y_train_split,
        validation_data=(X_val, y_val),
        epochs=epochs,
        batch_size=BATCH_SIZE,
        callbacks=callbacks,
        verbose=1
    )
    
    # Save final model
    model.save(f'chess_model_{model_type}.h5')
    
    # Save training info
    info = {
        'model_type': model_type,
        'training_positions': len(X_train),
        'epochs': epochs,
        'final_loss': float(history.history['loss'][-1]),
        'final_val_loss': float(history.history['val_loss'][-1]),
        'final_mae': float(history.history['mae'][-1]),
        'final_val_mae': float(history.history['val_mae'][-1]),
        'trained_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    with open(f'chess_model_{model_type}_info.json', 'w') as f:
        json.dump(info, f, indent=2)
    
    print(f"\n✅ Training complete!")
    print(f"  Final loss: {info['final_loss']:.4f}")
    print(f"  Final MAE: {info['final_mae']:.4f}")
    print(f"  Validation loss: {info['final_val_loss']:.4f}")
    print(f"  Validation MAE: {info['final_val_mae']:.4f}")
    
    return model, history

def main():
    print("=" * 60)
    print("♔ Chess AI Training Script")
    print("=" * 60)
    
    # Check for Stockfish
    stockfish_available = os.path.exists(STOCKFISH_PATH)
    
    if stockfish_available:
        print(f"✅ Stockfish found at: {STOCKFISH_PATH}")
        print("\n📊 Training Method: Stockfish-evaluated positions")
        X_train, y_train = generate_training_data_stockfish(
            TRAINING_POSITIONS,
            STOCKFISH_PATH
        )
    else:
        print(f"⚠️ Stockfish not found at: {STOCKFISH_PATH}")
        print("\n📊 Training Method: Random positions (limited quality)")
        print("\n💡 For better results:")
        print("  1. Download Stockfish from https://stockfishchess.org/download/")
        print("  2. Update STOCKFISH_PATH in this script")
        print("  3. Run training again")
        
        X_train, y_train = generate_random_training_data(TRAINING_POSITIONS)
    
    # Train model
    model, history = train_model(X_train, y_train, MODEL_TYPE, EPOCHS)
    
    print("\n" + "=" * 60)
    print("🎉 Training Complete!")
    print("=" * 60)
    print(f"\n📁 Model saved as: chess_model_{MODEL_TYPE}.h5")
    print(f"📁 Info saved as: chess_model_{MODEL_TYPE}_info.json")
    print("\n🎮 Start the server and play against your trained AI!")

if __name__ == "__main__":
    main()
