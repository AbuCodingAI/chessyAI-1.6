"""
VIEW CHESSY 1.5 RESULTS
Display training and testing results in a readable format
"""

import json
import os

RESULTS_PATH = "results/chessy_1.5_results.json"

def load_results():
    """Load results from JSON file"""
    if not os.path.exists(RESULTS_PATH):
        print(f"❌ Results file not found: {RESULTS_PATH}")
        print("   Run TRAIN_CHESSY_1.5_SELF_PLAY.py first!")
        return None
    
    with open(RESULTS_PATH, 'r') as f:
        return json.load(f)

def print_results(results):
    """Print results in formatted output"""
    print("\n" + "="*70)
    print("🏆 CHESSY 1.5 TRAINING RESULTS")
    print("="*70)
    
    print(f"\n📅 Training Date: {results.get('timestamp', 'Unknown')}")
    print(f"🎯 Estimated ELO: {results.get('estimated_elo', 'N/A')}")
    
    # Self-Play Results
    print("\n" + "-"*70)
    print("📊 SELF-PLAY RESULTS (Chessy vs Chessy)")
    print("-"*70)
    
    sp = results['self_play']
    print(f"   Total Games: {sp['games']}")
    print(f"   White Wins:  {sp['white_wins']} ({sp['white_wins']/sp['games']*100:.1f}%)")
    print(f"   Black Wins:  {sp['black_wins']} ({sp['black_wins']/sp['games']*100:.1f}%)")
    print(f"   Draws:       {sp['draws']} ({sp['draws']/sp['games']*100:.1f}%)")
    
    # vs Stockfish Results
    print("\n" + "-"*70)
    print("⚔️ VS STOCKFISH RESULTS (Depth 10 ≈ 2400 ELO)")
    print("-"*70)
    
    vs = results['vs_stockfish']
    total = vs['games']
    
    if total > 0:
        win_rate = (vs['wins'] + 0.5 * vs['draws']) / total * 100
        
        print(f"   Total Games: {total}")
        print(f"   Wins:        {vs['wins']} ({vs['wins']/total*100:.1f}%)")
        print(f"   Losses:      {vs['losses']} ({vs['losses']/total*100:.1f}%)")
        print(f"   Draws:       {vs['draws']} ({vs['draws']/total*100:.1f}%)")
        print(f"\n   📈 Win Rate: {win_rate:.1f}%")
        
        # Performance assessment
        print("\n   Performance Assessment:")
        if win_rate >= 60:
            print("   🌟 EXCELLENT - Stronger than Stockfish depth 10!")
        elif win_rate >= 50:
            print("   ✅ GOOD - Competitive with Stockfish depth 10")
        elif win_rate >= 40:
            print("   📊 DECENT - Close to Stockfish depth 10")
        elif win_rate >= 30:
            print("   ⚠️ NEEDS IMPROVEMENT - Below Stockfish depth 10")
        else:
            print("   ❌ WEAK - Significantly below Stockfish depth 10")
    
    # Training History
    if 'training_history' in results and results['training_history']:
        print("\n" + "-"*70)
        print("🧠 TRAINING HISTORY")
        print("-"*70)
        
        for i, entry in enumerate(results['training_history'], 1):
            print(f"\n   Training Session {i}:")
            print(f"   - Positions: {entry['positions']}")
            print(f"   - Loss: {entry['loss']:.4f}")
            print(f"   - Val Loss: {entry['val_loss']:.4f}")
    
    print("\n" + "="*70)

def compare_versions():
    """Compare Chessy 1.5 with previous versions"""
    print("\n" + "="*70)
    print("📊 CHESSY VERSION COMPARISON")
    print("="*70)
    
    versions = {
        "Chessy 1.0": {"elo": 1600, "description": "Basic neural network"},
        "Chessy 1.1": {"elo": 1800, "description": "Enhanced material evaluation"},
        "Chessy 1.2": {"elo": 2200, "description": "Magnus training"},
        "Chessy 1.3": {"elo": 2500, "description": "Deep search (depth 7)"},
        "Chessy 1.4": {"elo": 2700, "description": "Quiescence search (depth 10+)"},
    }
    
    # Load Chessy 1.5 results
    results = load_results()
    if results:
        chessy_15_elo = results.get('estimated_elo', 0)
        versions["Chessy 1.5"] = {
            "elo": chessy_15_elo,
            "description": "Self-play training"
        }
    
    # Print comparison
    print("\n   Version      ELO    Description")
    print("   " + "-"*60)
    
    for version, data in versions.items():
        elo_str = f"{data['elo']}" if data['elo'] else "N/A"
        print(f"   {version:<12} {elo_str:<6} {data['description']}")
    
    if results:
        print(f"\n   🎯 Chessy 1.5 Improvement:")
        improvement = chessy_15_elo - 2700  # vs Chessy 1.4
        if improvement > 0:
            print(f"   ✅ +{improvement} ELO vs Chessy 1.4")
        elif improvement < 0:
            print(f"   ⚠️ {improvement} ELO vs Chessy 1.4")
        else:
            print(f"   ➡️ Same as Chessy 1.4")
    
    print("\n" + "="*70)

def main():
    """Main function"""
    results = load_results()
    
    if results:
        print_results(results)
        compare_versions()
    else:
        print("\n⚠️ No results available yet.")
        print("   Run: python TRAIN_CHESSY_1.5_SELF_PLAY.py")

if __name__ == "__main__":
    main()
