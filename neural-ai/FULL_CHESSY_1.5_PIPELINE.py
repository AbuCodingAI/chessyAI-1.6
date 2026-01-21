"""
FULL CHESSY 1.5 TRAINING PIPELINE
Complete training and testing pipeline:
1. Generate training data (Stockfish vs Stockfish with noise)
2. Train neural network from data
3. Self-play testing (40 games)
4. Stockfish testing (60 games)
5. Calculate final ELO
"""

import subprocess
import sys
import os
from datetime import datetime

def run_script(script_name, description):
    """Run a Python script and handle errors"""
    print("\n" + "="*70)
    print(f"📍 {description}")
    print("="*70)
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            check=True,
            capture_output=False
        )
        print(f"\n✅ {description} - Complete")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {description} - Failed")
        print(f"   Error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ {description} - Error")
        print(f"   {e}")
        return False

def main():
    """Run full training pipeline"""
    start_time = datetime.now()
    
    print("="*70)
    print("🚀 CHESSY 1.5 - FULL TRAINING PIPELINE")
    print("="*70)
    print(f"\nStart time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nPipeline steps:")
    print("   1. Generate training data (Stockfish vs Stockfish)")
    print("   2. Train neural network")
    print("   3. Self-play testing (40 games)")
    print("   4. Stockfish testing (60 games)")
    print("   5. Calculate ELO rating")
    print("\nEstimated time: 4-6 hours")
    print("="*70)
    
    input("\nPress Enter to start...")
    
    # Step 1: Generate training data
    if not run_script(
        "GENERATE_TRAINING_DATA_STOCKFISH.py",
        "STEP 1: Generate Training Data"
    ):
        print("\n❌ Pipeline failed at step 1")
        return
    
    # Step 2: Train from Stockfish data
    if not run_script(
        "TRAIN_CHESSY_1.5_FROM_STOCKFISH.py",
        "STEP 2: Train Neural Network"
    ):
        print("\n❌ Pipeline failed at step 2")
        return
    
    # Step 3: Self-play and Stockfish testing
    if not run_script(
        "TRAIN_CHESSY_1.5_SELF_PLAY.py",
        "STEP 3: Self-Play & Stockfish Testing"
    ):
        print("\n❌ Pipeline failed at step 3")
        return
    
    # Step 4: View results
    run_script(
        "view_chessy_1.5_results.py",
        "STEP 4: View Results"
    )
    
    # Calculate total time
    end_time = datetime.now()
    duration = end_time - start_time
    hours = duration.seconds // 3600
    minutes = (duration.seconds % 3600) // 60
    
    print("\n" + "="*70)
    print("🏆 FULL PIPELINE COMPLETE!")
    print("="*70)
    print(f"\nStart time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"End time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duration: {hours}h {minutes}m")
    
    print("\n📁 Generated files:")
    print("   - training_data/stockfish_positions.json")
    print("   - models/chessy_1.5_stockfish_model.h5")
    print("   - models/chessy_1.5_model.h5")
    print("   - results/chessy_1.5_results.json")
    
    print("\n✅ Chessy 1.5 is ready to play!")
    print("="*70)

if __name__ == "__main__":
    main()
