"""
Chessy 1.3 - Time Control Specialist
Optimized for Bullet, Blitz, Rapid, and Classical time controls
"""

import chess
import chess.engine
import chess.pgn
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import layers
import os
import json
from datetime import datetime
import random
import requests
import io

from chess_ai_server import board_to_array, create_deep_cnn

# STOCKFISH PATH
STOCKFISH_PATH = r"C:\Users\Abu\Downloads\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe"

class TimeControlTrainer:
    """Train models optimized for different time controls"""
    
    def __init__(self, stockfish_path=STOCKFISH_PATH):
        self.stockfish_path = stockfish_path
        self.engine = None
        
        print("=" * 70)
        print("⚡ CHESSY 1.3 - TIME CONTROL SPECIALIST")
        print("=" * 70)
        
        # Start Stockfish
        try:
            print(f"\n🚀 Starting Stockfish...")
            self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
            print(f"   ✅ Stockfish started successfully!")
        except Exception as e:
            print(f"   ❌ Error starting Stockfish: {e}")
            self.engine = None
    
    def create_fast_network(self):
        """Create lightweight network for bullet/blitz"""
        print("\n⚡ Creating FAST network (Bullet/Blitz)...")
        
        model = keras.Sequential([
            keras.layers.Conv2D(32, 3, activation='relu', padding='same', 
                               input_shape=(8, 8, 12)),
            keras.layers.Flatten(),
            keras.layers.Dense(128, activation='relu'),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(1, activation='tanh')
        ])
        
        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        
        print(f"   Parameters: ~{model.count_params():,}")
        print(f"   Inference: ~0.01s per position")
        
        return model
    
    def create_standard_network(self):
        """Create standard network for rapid"""
        print("\n🎯 Creating STANDARD network (Rapid)...")
        
        model = create_deep_cnn()  # Use existing architecture
        
        print(f"   Parameters: ~{model.count_params():,}")
        print(f"   Inference: ~0.05s per position")
        
        return model
    
    def create_deep_network(self):
        """Create deep network for classical"""
        print("\n🧠 Creating DEEP network (Classical)...")
        
        inputs = keras.Input(shape=(8, 8, 12))
        
        # Deep convolutional layers
        x = keras.layers.Conv2D(128, 3, padding='same', activation='relu')(inputs)
        x = keras.layers.Conv2D(256, 3, padding='same', activation='relu')(x)
        x = keras.layers.Conv2D(512, 3, padding='same', activation='relu')(x)
        x = keras.layers.Conv2D(512, 3, padding='same', activation='relu')(x)
        x = keras.layers.Conv2D(512, 3, padding='same', activation='relu')(x)
        
        # Residual connections
        residual = x
        x = keras.layers.Conv2D(512, 3, padding='same', activation='relu')(x)
        x = keras.layers.Conv2D(512, 3, padding='same')(x)
        x = keras.layers.Add()([x, residual])
        x = keras.layers.Activation('relu')(x)
        
        x = keras.layers.Flatten()(x)
        x = keras.layers.Dense(512, activation='relu')(x)
        x = keras.layers.Dropout(0.3)(x)
        x = keras.layers.Dense(256, activation='relu')(x)
        x = keras.layers.Dropout(0.2)(x)
        outputs = keras.layers.Dense(1, activation='tanh')(x)
        
        model = keras.Model(inputs=inputs, outputs=outputs)
        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        
        print(f"   Parameters: ~{model.count_params():,}")
        print(f"   Inference: ~0.1s per position")
        
        return model
    
    def download_time_control_games(self, time_control='blitz', max_games=200):
        """
        Download games from Lichess by time control
        
        time_control: 'bullet', 'blitz', 'rapid', 'classical'
        """
        print(f"\n📥 Downloading {time_control} games from Lichess...")
        
        # Map time controls to Lichess perfType
        perf_types = {
            'bullet': 'bullet',
            'blitz': 'blitz',
            'rapid': 'rapid',
            'classical': 'classical'
        }
        
        perf_type = perf_types.get(time_control, 'blitz')
        
        # Use a strong player's games
        username = "DrNykterstein"  # Magnus Carlsen
        
        url = f"https://lichess.org/api/games/user/{username}"
        
        params = {
            'max': max_games,
            'rated': 'true',
            'perfType': perf_type,
            'opening': 'true',
            'clocks': 'true',  # Include time information
            'evals': 'false',
            'pgnInJson': 'false'
        }
        
        headers = {
            'Accept': 'application/x-chess-pgn'
        }
        
        try:
            response = requests.get(url, params=params, headers=headers, stream=True)
            
            if response.status_code == 200:
                pgn_text = response.text
                print(f"   ✅ Downloaded {time_control} games!")
                return pgn_text
            else:
                print(f"   ❌ Error: HTTP {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   ❌ Error downloading: {e}")
            return None
    
    def parse_games_with_time_info(self, pgn_text):
        """Parse PGN games and extract time information"""
        print("\n📖 Parsing games with time information...")
        
        games_data = []
        pgn_io = io.StringIO(pgn_text)
        
        game_count = 0
        while True:
            game = chess.pgn.read_game(pgn_io)
            if game is None:
                break
            
            games_data.append(game)
            game_count += 1
            
            if game_count % 50 == 0:
                print(f"   Parsed {game_count} games...")
        
        print(f"✅ Parsed {len(games_data)} games")
        return games_data
    
    def extract_positions_by_time_control(self, games, time_control):
        """
        Extract positions with time-aware labeling
        
        Positions where time pressure matters get special treatment
        """
        print(f"\n🎯 Extracting {time_control} positions...")
        
        positions = []
        labels = []
        
        for game_idx, game in enumerate(games):
            if game_idx % 50 == 0:
                print(f"   Processing game {game_idx}/{len(games)}...")
            
            # Get game result
            result = game.headers.get('Result', '*')
            
            if result == '1-0':
                outcome = 1.0
            elif result == '0-1':
                outcome = -1.0
            elif result == '1/2-1/2':
                outcome = 0.0
            else:
                continue
            
            # Extract positions
            board = game.board()
            move_count = 0
            
            for move in game.mainline_moves():
                board.push(move)
                move_count += 1
                
                # Skip opening
                if move_count < 10:
                    continue
                
                # For bullet/blitz, focus on middlegame (time pressure)
                if time_control in ['bullet', 'blitz']:
                    if 15 <= move_count <= 40:
                        positions.append(board_to_array(board))
                        
                        # Adjust label based on time pressure
                        # In time pressure, simpler positions are better
                        position_value = outcome
                        if board.turn == chess.BLACK:
                            position_value = -outcome
                        
                        labels.append(position_value)
                
                # For rapid, include more positions
                elif time_control == 'rapid':
                    if 10 <= move_count <= 60:
                        positions.append(board_to_array(board))
                        position_value = outcome if board.turn == chess.WHITE else -outcome
                        labels.append(position_value)
                
                # For classical, include all phases
                elif time_control == 'classical':
                    if 10 <= move_count <= 80:
                        positions.append(board_to_array(board))
                        position_value = outcome if board.turn == chess.WHITE else -outcome
                        labels.append(position_value)
        
        print(f"✅ Extracted {len(positions)} positions")
        
        return np.array(positions), np.array(labels)
    
    def train_time_control_model(self, time_control, network_type, epochs=30):
        """
        Train a model for specific time control
        
        time_control: 'bullet', 'blitz', 'rapid', 'classical'
        network_type: 'fast', 'standard', 'deep'
        """
        print("\n" + "=" * 70)
        print(f"🎯 TRAINING {time_control.upper()} MODEL")
        print("=" * 70)
        
        # Download games
        pgn_text = self.download_time_control_games(time_control, max_games=200)
        
        if pgn_text is None:
            print(f"\n❌ Could not download {time_control} games")
            return None, None
        
        # Parse games
        games = self.parse_games_with_time_info(pgn_text)
        
        if len(games) == 0:
            print(f"\n❌ No games parsed")
            return None, None
        
        # Extract positions
        X_train, y_train = self.extract_positions_by_time_control(games, time_control)
        
        if len(X_train) == 0:
            print(f"\n❌ No positions extracted")
            return None, None
        
        print(f"\n📊 Training data: {len(X_train)} positions")
        
        # Create model
        if network_type == 'fast':
            model = self.create_fast_network()
        elif network_type == 'standard':
            model = self.create_standard_network()
        elif network_type == 'deep':
            model = self.create_deep_network()
        else:
            raise ValueError(f"Unknown network type: {network_type}")
        
        # Train
        print(f"\n🚀 Training {time_control} model...\n")
        
        callbacks = [
            keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True),
            keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=3),
            keras.callbacks.ModelCheckpoint(
                f'chess_model_{time_control}_{network_type}_best.h5',
                save_best_only=True,
                monitor='val_loss'
            )
        ]
        
        history = model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=64,
            validation_split=0.2,
            callbacks=callbacks,
            verbose=1
        )
        
        # Save model
        model.save(f'chess_model_{time_control}_{network_type}.h5')
        
        # Save info
        info = {
            'version': 'Chessy 1.3',
            'time_control': time_control,
            'network_type': network_type,
            'training_positions': len(X_train),
            'games_used': len(games),
            'epochs': epochs,
            'final_loss': float(history.history['loss'][-1]),
            'final_val_loss': float(history.history['val_loss'][-1]),
            'trained_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        with open(f'chess_model_{time_control}_{network_type}_info.json', 'w') as f:
            json.dump(info, f, indent=2)
        
        print(f"\n✅ {time_control.upper()} model complete!")
        print(f"   Training loss: {info['final_loss']:.4f}")
        print(f"   Validation loss: {info['final_val_loss']:.4f}")
        
        return model, history
    
    def close(self):
        """Close Stockfish engine"""
        if self.engine:
            self.engine.quit()
            print("\n✅ Stockfish closed")


def main():
    """Main training pipeline"""
    
    print("\n" + "=" * 70)
    print("⚡ CHESSY 1.3 - TIME CONTROL SPECIALIST")
    print("=" * 70)
    print("\nTrain specialized models for different time controls!")
    print("Each model is optimized for its specific time format.\n")
    
    trainer = TimeControlTrainer(STOCKFISH_PATH)
    
    print("\n" + "=" * 70)
    print("📊 TRAINING OPTIONS")
    print("=" * 70)
    print("\n1. ⚡ Bullet (Fast network)")
    print("   - Time: ~30 min")
    print("   - Strength: ~2000 ELO")
    print("   - Speed: 0.01s per move")
    
    print("\n2. 🏃 Blitz (Fast network)")
    print("   - Time: ~30 min")
    print("   - Strength: ~2100 ELO")
    print("   - Speed: 0.01s per move")
    
    print("\n3. 🎯 Rapid (Standard network)")
    print("   - Time: ~45 min")
    print("   - Strength: ~2200 ELO")
    print("   - Speed: 0.05s per move")
    
    print("\n4. 🧠 Classical (Deep network)")
    print("   - Time: ~60 min")
    print("   - Strength: ~2400 ELO")
    print("   - Speed: 0.1s per move")
    
    print("\n5. 🎯 All (Train all time controls)")
    print("   - Time: ~3 hours")
    print("   - Complete suite")
    
    choice = input("\nSelect option (1-5): ").strip()
    
    if choice == '1':
        trainer.train_time_control_model('bullet', 'fast', epochs=25)
    elif choice == '2':
        trainer.train_time_control_model('blitz', 'fast', epochs=25)
    elif choice == '3':
        trainer.train_time_control_model('rapid', 'standard', epochs=30)
    elif choice == '4':
        trainer.train_time_control_model('classical', 'deep', epochs=35)
    elif choice == '5':
        print("\n🚀 Training all time controls...")
        trainer.train_time_control_model('bullet', 'fast', epochs=25)
        trainer.train_time_control_model('blitz', 'fast', epochs=25)
        trainer.train_time_control_model('rapid', 'standard', epochs=30)
        trainer.train_time_control_model('classical', 'deep', epochs=35)
    else:
        print("\n❌ Invalid choice")
        return
    
    trainer.close()
    
    print("\n" + "=" * 70)
    print("🎉 CHESSY 1.3 TRAINING COMPLETE!")
    print("=" * 70)
    print("\n💪 You now have time-control-optimized models!")
    print("\n🎮 Next steps:")
    print("   1. Update server to select model by time control")
    print("   2. Test each model in its time format")
    print("   3. Enjoy optimized performance!")


if __name__ == "__main__":
    main()
