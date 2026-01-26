#!/usr/bin/env python3
"""
Chessy 1.6 Cloud Training Wrapper
Runs the C++ training engine with cloud-specific optimizations
Handles checkpointing, monitoring, and graceful shutdown
"""

import subprocess
import os
import sys
import json
import time
import signal
from pathlib import Path
from datetime import datetime

class ChessyCloudTrainer:
    def __init__(self):
        self.binary_path = "./bin/chessy-1.6"
        self.checkpoint_dir = "./checkpoints"
        self.models_dir = "./models"
        self.log_file = "training.log"
        self.config_file = "training_config.json"
        self.process = None
        
        # Create directories
        Path(self.checkpoint_dir).mkdir(exist_ok=True)
        Path(self.models_dir).mkdir(exist_ok=True)
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGTERM, self._handle_shutdown)
        signal.signal(signal.SIGINT, self._handle_shutdown)
    
    def _handle_shutdown(self, signum, frame):
        """Gracefully shutdown training"""
        print("\n⚠ Shutdown signal received. Saving checkpoint...")
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=30)
            except subprocess.TimeoutExpired:
                self.process.kill()
        sys.exit(0)
    
    def create_config(self):
        """Create training configuration for cloud deployment"""
        config = {
            "numGamesGeneration": 1000,
            "stockfishDepth": 15,
            "blunderRate": 0.05,
            "epochs": 100,
            "learningRate": 0.001,
            "batchSize": 32,
            "numSelfPlayGames": 500,
            "numTestGames": 100,
            "overfitting": {
                "enableEarlyStopping": True,
                "patienceEpochs": 10,
                "minValidationImprovement": 0.001,
                "l2Regularization": 0.0001,
                "dropoutRate": 0.3,
                "enableDataAugmentation": True,
                "augmentationRate": 0.2,
                "validationSplitRatio": 20,
                "enableCrossValidation": True,
                "kFolds": 5
            },
            "enableCheckpointing": True,
            "checkpointDir": self.checkpoint_dir,
            "checkpointInterval": 5,
            "isCloudDeployment": True,
            "maxTrainingHours": 24,
            "modelOutputPath": f"{self.models_dir}/chessy-1.6-trained.bin"
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✓ Configuration created: {self.config_file}")
        return config
    
    def check_binary(self):
        """Check if binary exists"""
        if not os.path.exists(self.binary_path):
            print(f"❌ Binary not found: {self.binary_path}")
            print("Please run: build.bat (Windows) or ./build.sh (Linux/macOS)")
            return False
        return True
    
    def check_stockfish(self):
        """Check if Stockfish is available"""
        stockfish_paths = [
            "./stockfish/stockfish-windows-x86-64-avx2.exe",
            "./stockfish/stockfish",
            "/usr/games/stockfish",
            "/usr/local/bin/stockfish"
        ]
        
        for path in stockfish_paths:
            if os.path.exists(path):
                print(f"✓ Stockfish found: {path}")
                return True
        
        print("⚠ Stockfish not found. Training will use fallback evaluation.")
        return False
    
    def run_training(self):
        """Run the training process"""
        print("\n" + "="*60)
        print("Chessy 1.6 Cloud Training")
        print("="*60)
        print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Checkpoint dir: {self.checkpoint_dir}")
        print(f"Models dir: {self.models_dir}")
        print("="*60 + "\n")
        
        # Checks
        if not self.check_binary():
            return False
        
        self.check_stockfish()
        
        # Create config
        self.create_config()
        
        # Run training
        try:
            print("Starting training process...")
            self.process = subprocess.Popen(
                [self.binary_path, "--train"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            # Stream output
            with open(self.log_file, 'w') as log:
                for line in self.process.stdout:
                    print(line, end='')
                    log.write(line)
                    log.flush()
            
            returncode = self.process.wait()
            
            print("\n" + "="*60)
            print(f"Training completed with exit code: {returncode}")
            print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Log file: {self.log_file}")
            print("="*60)
            
            return returncode == 0
            
        except Exception as e:
            print(f"❌ Error running training: {e}")
            return False
    
    def monitor_training(self):
        """Monitor training progress"""
        print("\nMonitoring training progress...")
        
        while True:
            # Check for latest checkpoint
            checkpoints = sorted(Path(self.checkpoint_dir).glob("checkpoint_epoch_*.bin"))
            if checkpoints:
                latest = checkpoints[-1]
                print(f"Latest checkpoint: {latest.name}")
            
            # Check for final model
            final_model = Path(self.models_dir) / "chessy-1.6-trained.bin"
            if final_model.exists():
                print(f"✓ Final model saved: {final_model}")
                break
            
            time.sleep(60)  # Check every minute

def main():
    trainer = ChessyCloudTrainer()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--monitor":
            trainer.monitor_training()
        elif sys.argv[1] == "--config":
            trainer.create_config()
        else:
            print(f"Unknown option: {sys.argv[1]}")
            print("Usage: python train_cloud.py [--monitor|--config]")
    else:
        success = trainer.run_training()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
