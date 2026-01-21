"""
Chessy 1.0 - Neural Network Chess AI Server
Flask backend for neural network chess evaluation
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import tensorflow as tf
from tensorflow import keras
import chess
import chess.engine  # For move validation and optional Stockfish integration
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Global variables
model = None
model_name = "basic_cnn"
training_data = []
model_info = {
    'training_games': 0,
    'accuracy': 0.0,
    'last_update': 'Never'
}

# Piece values for evaluation
PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

def board_to_array(board):
    """Convert chess board to neural network input (8x8x12)"""
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

def create_basic_cnn():
    """Create basic CNN model"""
    model = keras.Sequential([
        keras.layers.Conv2D(64, 3, activation='relu', padding='same', input_shape=(8, 8, 12)),
        keras.layers.Conv2D(128, 3, activation='relu', padding='same'),
        keras.layers.Flatten(),
        keras.layers.Dense(256, activation='relu'),
        keras.layers.Dropout(0.3),
        keras.layers.Dense(1, activation='tanh')  # Output: position evaluation
    ])
    
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model

def create_deep_cnn():
    """Create deep CNN model"""
    model = keras.Sequential([
        keras.layers.Conv2D(64, 3, activation='relu', padding='same', input_shape=(8, 8, 12)),
        keras.layers.Conv2D(128, 3, activation='relu', padding='same'),
        keras.layers.Conv2D(256, 3, activation='relu', padding='same'),
        keras.layers.Flatten(),
        keras.layers.Dense(512, activation='relu'),
        keras.layers.Dropout(0.4),
        keras.layers.Dense(256, activation='relu'),
        keras.layers.Dropout(0.3),
        keras.layers.Dense(1, activation='tanh')
    ])
    
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model

def create_residual_model():
    """Create ResNet-style model"""
    inputs = keras.Input(shape=(8, 8, 12))
    
    x = keras.layers.Conv2D(64, 3, padding='same', activation='relu')(inputs)
    
    # Residual blocks
    for _ in range(3):
        residual = x
        x = keras.layers.Conv2D(64, 3, padding='same', activation='relu')(x)
        x = keras.layers.Conv2D(64, 3, padding='same')(x)
        x = keras.layers.Add()([x, residual])
        x = keras.layers.Activation('relu')(x)
    
    x = keras.layers.Flatten()(x)
    x = keras.layers.Dense(256, activation='relu')(x)
    x = keras.layers.Dropout(0.3)(x)
    outputs = keras.layers.Dense(1, activation='tanh')(x)
    
    model = keras.Model(inputs=inputs, outputs=outputs)
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model

def evaluate_position(board):
    """Evaluate position using neural network"""
    global model
    
    if model is None:
        # Fallback to material count
        return material_evaluation(board)
    
    board_array = board_to_array(board)
    board_array = np.expand_dims(board_array, axis=0)
    
    evaluation = model.predict(board_array, verbose=0)[0][0]
    return float(evaluation)

def material_evaluation(board):
    """Simple material evaluation"""
    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = PIECE_VALUES[piece.piece_type]
            score += value if piece.color == chess.WHITE else -value
    return score / 1000.0  # Normalize

def get_best_move_nn(board, depth=3, temperature=0.1):
    """Get best move using neural network evaluation"""
    legal_moves = list(board.legal_moves)
    
    if not legal_moves:
        return None
    
    move_scores = []
    nodes_searched = 0
    
    for move in legal_moves:
        board.push(move)
        score = -evaluate_position(board)
        board.pop()
        
        move_scores.append((move, score))
        nodes_searched += 1
    
    # Sort by score
    move_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Apply temperature for move selection
    if temperature > 0:
        scores = np.array([score for _, score in move_scores])
        scores = scores / temperature
        probs = np.exp(scores) / np.sum(np.exp(scores))
        
        # Sample move based on probabilities
        idx = np.random.choice(len(move_scores), p=probs)
        best_move, best_score = move_scores[idx]
        confidence = probs[idx]
    else:
        best_move, best_score = move_scores[0]
        confidence = 1.0
    
    return {
        'move': best_move.uci(),
        'evaluation': float(best_score),
        'confidence': float(confidence),
        'nodes_searched': nodes_searched
    }

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'model_loaded': model is not None,
        'model_name': model_name,
        'training_games': model_info['training_games'],
        'accuracy': model_info['accuracy'],
        'last_update': model_info['last_update']
    })

@app.route('/get_move', methods=['POST'])
def get_move():
    """Get AI move for current position"""
    data = request.json
    
    try:
        # Convert board array to chess.Board
        board = chess.Board()
        board.clear()
        
        # Reconstruct board from array
        piece_map = {
            '♔': (chess.KING, chess.WHITE), '♕': (chess.QUEEN, chess.WHITE),
            '♖': (chess.ROOK, chess.WHITE), '♗': (chess.BISHOP, chess.WHITE),
            '♘': (chess.KNIGHT, chess.WHITE), '♙': (chess.PAWN, chess.WHITE),
            '♚': (chess.KING, chess.BLACK), '♛': (chess.QUEEN, chess.BLACK),
            '♜': (chess.ROOK, chess.BLACK), '♝': (chess.BISHOP, chess.BLACK),
            '♞': (chess.KNIGHT, chess.BLACK), '♟': (chess.PAWN, chess.BLACK)
        }
        
        board_array = data['board']
        for row in range(8):
            for col in range(8):
                piece_symbol = board_array[row][col]
                if piece_symbol:
                    piece_type, color = piece_map[piece_symbol]
                    square = chess.square(col, 7 - row)
                    board.set_piece_at(square, chess.Piece(piece_type, color))
        
        board.turn = chess.BLACK  # AI plays black
        
        # Get move
        depth = data.get('depth', 3)
        temperature = data.get('temperature', 0.1)
        
        result = get_best_move_nn(board, depth, temperature)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/retrain', methods=['POST'])
def retrain():
    """Retrain the neural network"""
    global model, model_info
    
    try:
        # Generate training data (simplified - in production, use real games)
        print("Generating training data...")
        X_train = []
        y_train = []
        
        for _ in range(1000):
            board = chess.Board()
            # Make random moves
            for _ in range(np.random.randint(5, 20)):
                if board.is_game_over():
                    break
                move = np.random.choice(list(board.legal_moves))
                board.push(move)
            
            X_train.append(board_to_array(board))
            y_train.append(material_evaluation(board))
        
        X_train = np.array(X_train)
        y_train = np.array(y_train)
        
        # Train model
        print("Training model...")
        model = create_basic_cnn()
        history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2, verbose=1)
        
        # Update info
        model_info['training_games'] = 1000
        model_info['accuracy'] = float(history.history['val_mae'][-1])
        model_info['last_update'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Save model
        model.save('chess_model.h5')
        
        return jsonify({
            'status': 'success',
            'accuracy': model_info['accuracy'],
            'loss': float(history.history['loss'][-1])
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/load_model', methods=['POST'])
def load_model():
    """Load a specific model"""
    global model, model_name
    
    data = request.json
    model_type = data.get('model', 'basic')
    
    try:
        if model_type == 'basic':
            model = create_basic_cnn()
        elif model_type == 'deep':
            model = create_deep_cnn()
        elif model_type == 'residual':
            model = create_residual_model()
        else:
            return jsonify({'error': 'Unknown model type'}), 400
        
        model_name = model_type
        
        # Try to load weights if they exist
        if os.path.exists(f'chess_model_{model_type}.h5'):
            model.load_weights(f'chess_model_{model_type}.h5')
        
        return jsonify({'status': 'success', 'model': model_type})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Chessy 1.0 Neural Network Server...")
    print("📡 Server will run on http://localhost:5000")
    print("🧠 Loading neural network model...")
    
    # Try to load existing model
    if os.path.exists('chess_model.h5'):
        try:
            model = keras.models.load_model('chess_model.h5')
            print("✅ Loaded existing model")
        except:
            print("⚠️ Could not load model, creating new one...")
            model = create_basic_cnn()
    else:
        print("📦 Creating new model...")
        model = create_basic_cnn()
    
    print("✅ Server ready!")
    print("\n🎮 Open Chessy1-0.html in your browser to play!")
    
    app.run(debug=True, port=5000)
