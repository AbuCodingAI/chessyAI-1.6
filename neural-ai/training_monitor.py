"""
Training Monitor - Track progress of both Chessy 1.0 and 1.1
"""

import os
import json
import time
from datetime import datetime

def format_time(seconds):
    """Format seconds to readable time"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def check_model_info(model_path):
    """Check if model info file exists and read it"""
    info_path = model_path.replace('.h5', '_info.json')
    
    if os.path.exists(info_path):
        with open(info_path, 'r') as f:
            return json.load(f)
    return None

def monitor_training():
    """Monitor training progress"""
    
    print("=" * 80)
    print("♔ CHESSY TRAINING MONITOR")
    print("=" * 80)
    print("\nMonitoring training progress for Chessy 1.0 and 1.1...")
    print("Press Ctrl+C to stop monitoring\n")
    
    start_time = time.time()
    
    try:
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print("=" * 80)
            print("♔ CHESSY TRAINING MONITOR")
            print("=" * 80)
            
            elapsed = time.time() - start_time
            print(f"\n⏱️  Monitoring time: {format_time(elapsed)}")
            print(f"🕐 Current time: {datetime.now().strftime('%H:%M:%S')}")
            
            # Check Chessy 1.0 models
            print("\n" + "─" * 80)
            print("🤖 CHESSY 1.0 - SELF-PLAY TRAINING")
            print("─" * 80)
            
            chessy_1_0_models = [
                ('chess_model_basic.h5', 'Initial Model'),
                ('chess_model_selfplay_gen25.h5', 'Generation 25'),
                ('chess_model_selfplay_gen50.h5', 'Generation 50'),
                ('chess_model_selfplay_gen75.h5', 'Generation 75'),
                ('chess_model_selfplay_final.h5', 'Final Model')
            ]
            
            found_1_0 = False
            for model_path, name in chessy_1_0_models:
                if os.path.exists(model_path):
                    found_1_0 = True
                    size_mb = os.path.getsize(model_path) / (1024 * 1024)
                    mod_time = datetime.fromtimestamp(os.path.getmtime(model_path))
                    
                    print(f"\n✅ {name}")
                    print(f"   📁 {model_path}")
                    print(f"   💾 Size: {size_mb:.2f} MB")
                    print(f"   🕐 Modified: {mod_time.strftime('%H:%M:%S')}")
                    
                    info = check_model_info(model_path)
                    if info:
                        if 'games_played' in info:
                            print(f"   🎮 Games played: {info['games_played']}")
                        if 'training_iterations' in info:
                            print(f"   🔄 Training iterations: {info['training_iterations']}")
                        if 'replay_buffer_size' in info:
                            print(f"   💾 Replay buffer: {info['replay_buffer_size']} positions")
            
            if not found_1_0:
                print("\n⏳ No Chessy 1.0 models found yet...")
                print("   Waiting for self-play training to start...")
            
            # Check Chessy 1.1 models
            print("\n" + "─" * 80)
            print("🏆 CHESSY 1.1 - MAGNUS CARLSEN TRAINING")
            print("─" * 80)
            
            chessy_1_1_models = [
                ('chess_model_magnus_basic.h5', 'Magnus Basic'),
                ('chess_model_magnus_deep.h5', 'Magnus Deep'),
                ('chess_model_magnus_basic_best.h5', 'Magnus Basic (Best)'),
                ('chess_model_magnus_deep_best.h5', 'Magnus Deep (Best)')
            ]
            
            found_1_1 = False
            for model_path, name in chessy_1_1_models:
                if os.path.exists(model_path):
                    found_1_1 = True
                    size_mb = os.path.getsize(model_path) / (1024 * 1024)
                    mod_time = datetime.fromtimestamp(os.path.getmtime(model_path))
                    
                    print(f"\n✅ {name}")
                    print(f"   📁 {model_path}")
                    print(f"   💾 Size: {size_mb:.2f} MB")
                    print(f"   🕐 Modified: {mod_time.strftime('%H:%M:%S')}")
                    
                    info = check_model_info(model_path)
                    if info:
                        if 'training_positions' in info:
                            print(f"   📊 Training positions: {info['training_positions']}")
                        if 'games_used' in info:
                            print(f"   🎮 Games used: {info['games_used']}")
                        if 'final_val_mae' in info:
                            print(f"   📈 Validation MAE: {info['final_val_mae']:.4f}")
            
            if not found_1_1:
                print("\n⏳ No Chessy 1.1 models found yet...")
                print("   Waiting for Magnus training to start...")
            
            # Training status
            print("\n" + "─" * 80)
            print("📊 TRAINING STATUS")
            print("─" * 80)
            
            if found_1_0 and found_1_1:
                print("\n✅ Both models are training!")
                print("   Run compare_models.py when both are complete")
            elif found_1_0:
                print("\n⏳ Chessy 1.0 training in progress...")
                print("   Waiting for Chessy 1.1 to start...")
            elif found_1_1:
                print("\n⏳ Chessy 1.1 training in progress...")
                print("   Waiting for Chessy 1.0 to start...")
            else:
                print("\n⏳ Waiting for training to start...")
            
            print("\n" + "=" * 80)
            print("🔄 Refreshing in 10 seconds... (Ctrl+C to stop)")
            print("=" * 80)
            
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\n\n✅ Monitoring stopped.")
        print("\n📊 Final status saved above.")


if __name__ == "__main__":
    monitor_training()
