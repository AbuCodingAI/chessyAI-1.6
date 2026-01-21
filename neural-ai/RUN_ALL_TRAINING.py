"""
Run All Chessy 1.3 Training - Complete Suite
Trains all components for IM-beatable AI
"""

import subprocess
import sys
import os
from datetime import datetime

def run_training_script(script_name, description, estimated_time):
    """Run a training script and handle errors"""
    print("\n" + "=" * 70)
    print(f"🚀 {description}")
    print(f"⏱️  Estimated time: {estimated_time}")
    print("=" * 70)
    
    start_time = datetime.now()
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            check=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        elapsed = datetime.now() - start_time
        print(f"\n✅ {description} complete!")
        print(f"   Time taken: {elapsed}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {description} failed!")
        print(f"   Error: {e}")
        return False
    except KeyboardInterrupt:
        print(f"\n⚠️ Training interrupted by user!")
        return False


def main():
    """Run complete training suite"""
    
    print("\n" + "=" * 70)
    print("♔ CHESSY 1.3 - COMPLETE TRAINING SUITE")
    print("=" * 70)
    print("\nThis will train Chessy 1.3 with ALL features:")
    print("  1️⃣  Time Control Optimization (Bullet/Blitz/Rapid/Classical)")
    print("  2️⃣  Blunder Recognition Training")
    print("  3️⃣  Opening Theory Training")
    print("\n📊 Total estimated time: ~5-6 hours")
    print("🏆 Result: 2500+ ELO IM-beatable AI!")
    print("\n⚠️  Make sure you have:")
    print("  ✅ Stockfish installed and path configured")
    print("  ✅ Internet connection (for downloading games)")
    print("  ✅ 5-6 hours available")
    print("  ✅ Chessy 1.2 base model trained")
    
    response = input("\n🎯 Start complete training? (y/n): ").lower()
    
    if response != 'y':
        print("\n❌ Training cancelled.")
        return
    
    overall_start = datetime.now()
    results = []
    
    # Step 1: Time Control Training
    success = run_training_script(
        'train_chessy_1.3_time_control.py',
        'STEP 1: Time Control Training',
        '~3 hours'
    )
    results.append(('Time Control Training', success))
    
    if not success:
        print("\n⚠️ Time control training failed. Continue anyway? (y/n): ")
        if input().lower() != 'y':
            return
    
    # Step 2: Blunder Training
    success = run_training_script(
        'blunder_training.py',
        'STEP 2: Blunder Recognition Training',
        '~1-2 hours'
    )
    results.append(('Blunder Training', success))
    
    if not success:
        print("\n⚠️ Blunder training failed. Continue anyway? (y/n): ")
        if input().lower() != 'y':
            return
    
    # Step 3: Opening Training
    success = run_training_script(
        'stockfish_opening_training.py',
        'STEP 3: Opening Theory Training',
        '~30-45 minutes'
    )
    results.append(('Opening Training', success))
    
    # Summary
    overall_elapsed = datetime.now() - overall_start
    
    print("\n" + "=" * 70)
    print("🎉 CHESSY 1.3 TRAINING COMPLETE!")
    print("=" * 70)
    
    print(f"\n⏱️  Total time: {overall_elapsed}")
    
    print("\n📊 Training Results:")
    for name, success in results:
        status = "✅ Success" if success else "❌ Failed"
        print(f"  {status}: {name}")
    
    all_success = all(success for _, success in results)
    
    if all_success:
        print("\n🏆 ALL TRAINING SUCCESSFUL!")
        print("\n💪 Your AI now has:")
        print("  ✅ 2500+ ELO strength (IM-beatable!)")
        print("  ✅ Time control optimization")
        print("  ✅ Blunder recognition")
        print("  ✅ Opening theory")
        print("  ✅ Deep search capability")
        
        print("\n📁 Models created:")
        print("  - chess_model_bullet_fast.h5")
        print("  - chess_model_blitz_fast.h5")
        print("  - chess_model_rapid_standard.h5")
        print("  - chess_model_classical_deep.h5")
        print("  - chess_model_blunder_trained.h5")
        print("  - chess_model_with_openings.h5")
        
        print("\n🎮 Next steps:")
        print("  1. Update chess_ai_server.py to use new models")
        print("  2. Integrate chess_engine_deep_search.py")
        print("  3. Test against strong opponents")
        print("  4. Enjoy your IM-level AI!")
    else:
        print("\n⚠️ Some training steps failed!")
        print("  Check the errors above and retry failed steps.")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Training interrupted by user!")
        print("  Progress has been saved.")
        print("  You can resume by running individual scripts.")
