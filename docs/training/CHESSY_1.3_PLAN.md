# Chessy 1.3 - Time Control Specialist

**Status:** 📋 Planned (waiting for 1.2 to complete)
**Focus:** Optimized for Bullet, Blitz, and Rapid time controls
**Target Strength:** ~2200-2400 ELO (time-aware)

---

## The Problem with Current Versions

### Chessy 1.0, 1.1, 1.2
- ❌ Same evaluation speed regardless of time control
- ❌ No time management strategy
- ❌ Doesn't adjust depth based on remaining time
- ❌ Can lose on time in bullet/blitz
- ❌ Wastes time in rapid/classical

### What Players Need
- ⚡ **Bullet (1-2 min):** Fast, intuitive moves
- 🏃 **Blitz (3-5 min):** Quick tactical calculation
- 🎯 **Rapid (10-15 min):** Balanced speed and depth
- 🧠 **Classical (30+ min):** Deep calculation

---

## Chessy 1.3 Features

### 1. Time-Aware Evaluation

**Dynamic Depth Adjustment:**
```python
if time_remaining < 10:  # Bullet mode
    search_depth = 1
    use_fast_eval = True
elif time_remaining < 60:  # Blitz mode
    search_depth = 2
    use_fast_eval = True
elif time_remaining < 300:  # Rapid mode
    search_depth = 3
    use_fast_eval = False
else:  # Classical mode
    search_depth = 5
    use_fast_eval = False
```

**Time Allocation:**
```python
# Allocate time per move based on game phase
if move_number < 10:  # Opening
    time_per_move = total_time * 0.02  # 2% per move
elif move_number < 30:  # Middlegame
    time_per_move = total_time * 0.05  # 5% per move
else:  # Endgame
    time_per_move = total_time * 0.03  # 3% per move
```

### 2. Multiple Neural Networks

**Fast Network (Bullet/Blitz):**
- Smaller architecture (32-64 filters)
- Single conv layer
- Fast inference (~0.01s per position)
- Optimized for speed over accuracy

**Standard Network (Rapid):**
- Current architecture (64-128-256 filters)
- 3 conv layers
- Balanced speed/accuracy (~0.05s per position)

**Deep Network (Classical):**
- Larger architecture (128-256-512 filters)
- 5+ conv layers
- Maximum accuracy (~0.1s per position)

### 3. Opening Book by Time Control

**Bullet Opening Book:**
- Fast, solid openings
- Avoid complex theory
- Quick development
- Examples: Italian Game, London System

**Blitz Opening Book:**
- Tactical openings
- Sharp positions
- Surprise value
- Examples: Sicilian, King's Indian

**Rapid/Classical Opening Book:**
- Deep theory
- Complex positions
- Strategic depth
- Examples: Ruy Lopez, Queen's Gambit

### 4. Time Pressure Handling

**When Low on Time (<10s):**
- Switch to pre-moves
- Use opening book exclusively
- Simple captures only
- Avoid calculation

**Time Scramble Mode (<5s):**
- Instant moves
- Pattern recognition only
- No search
- Survival mode

### 5. Training for Each Time Control

**Bullet Training:**
- Train on positions requiring fast decisions
- Penalize slow moves
- Reward quick tactical shots
- Dataset: Bullet games from Lichess

**Blitz Training:**
- Train on tactical puzzles
- Medium-depth positions
- Dataset: Blitz games from top players

**Rapid Training:**
- Train on strategic positions
- Deeper evaluation
- Dataset: Rapid/Classical games

---

## Implementation Plan

### Phase 1: Time Management System
```python
class TimeManager:
    def __init__(self, time_control, increment):
        self.time_control = time_control
        self.increment = increment
        self.time_remaining = time_control
        
    def allocate_time(self, move_number, game_phase):
        """Calculate time to spend on this move"""
        # Complex algorithm based on:
        # - Remaining time
        # - Move number
        # - Game phase
        # - Position complexity
        pass
    
    def should_move_now(self, time_spent):
        """Check if we should stop thinking"""
        return time_spent >= self.allocated_time
```

### Phase 2: Fast Neural Network
```python
def create_fast_cnn():
    """Lightweight network for bullet/blitz"""
    model = keras.Sequential([
        keras.layers.Conv2D(32, 3, activation='relu', 
                           padding='same', input_shape=(8, 8, 12)),
        keras.layers.Flatten(),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(1, activation='tanh')
    ])
    return model
```

### Phase 3: Time-Control-Specific Training
```python
def train_for_time_control(time_control):
    """Train model optimized for specific time control"""
    
    # Download games of that time control
    games = download_games_by_time_control(time_control)
    
    # Extract positions with time pressure
    positions = extract_time_critical_positions(games)
    
    # Train with time-aware loss function
    model = train_with_time_penalty(positions)
    
    return model
```

### Phase 4: Adaptive Search
```python
def get_best_move_adaptive(board, time_remaining):
    """Adjust search based on time"""
    
    if time_remaining < 10:
        # Bullet mode: instant move
        return get_fast_move(board)
    elif time_remaining < 60:
        # Blitz mode: shallow search
        return minimax(board, depth=2)
    elif time_remaining < 300:
        # Rapid mode: medium search
        return minimax(board, depth=3)
    else:
        # Classical mode: deep search
        return minimax(board, depth=5)
```

---

## Training Data Sources

### Bullet Games
- Lichess bullet database
- Filter: 1+0, 1+1, 2+1 time controls
- Players: 2000+ ELO
- Focus: Fast tactical positions

### Blitz Games
- Lichess blitz database
- Filter: 3+0, 3+2, 5+0 time controls
- Players: 2200+ ELO
- Focus: Sharp tactical games

### Rapid Games
- Lichess rapid database
- Filter: 10+0, 15+10 time controls
- Players: 2400+ ELO
- Focus: Strategic depth

---

## Expected Performance

### By Time Control

| Time Control | Current (1.2) | Target (1.3) | Improvement |
|--------------|---------------|--------------|-------------|
| Bullet (1+0) | ~1600 ELO | ~2000 ELO | +400 |
| Blitz (3+0) | ~1800 ELO | ~2200 ELO | +400 |
| Rapid (10+0) | ~2000 ELO | ~2400 ELO | +400 |
| Classical (30+0) | ~2000 ELO | ~2400 ELO | +400 |

### Why the Improvement?

**Current Problem:**
- Uses same slow evaluation for all time controls
- Loses on time in bullet/blitz
- Doesn't use available time in rapid/classical

**After 1.3:**
- Fast network for bullet/blitz
- Time-aware search depth
- Proper time allocation
- Never loses on time

---

## Technical Specifications

### Network Architectures

**Fast Network (Bullet/Blitz):**
```
Input: 8x8x12
Conv2D: 32 filters, 3x3
Flatten
Dense: 128 neurons
Output: 1 (evaluation)

Parameters: ~50k
Inference time: ~0.01s
```

**Standard Network (Rapid):**
```
Input: 8x8x12
Conv2D: 64 filters, 3x3
Conv2D: 128 filters, 3x3
Conv2D: 256 filters, 3x3
Flatten
Dense: 256 neurons
Output: 1 (evaluation)

Parameters: ~500k
Inference time: ~0.05s
```

**Deep Network (Classical):**
```
Input: 8x8x12
Conv2D: 128 filters, 3x3
Conv2D: 256 filters, 3x3
Conv2D: 512 filters, 3x3
Conv2D: 512 filters, 3x3
Conv2D: 512 filters, 3x3
Flatten
Dense: 512 neurons
Dense: 256 neurons
Output: 1 (evaluation)

Parameters: ~2M
Inference time: ~0.1s
```

---

## Training Timeline

### Phase 1: Fast Network (1 hour)
- Train lightweight network
- Optimize for speed
- Test inference time

### Phase 2: Time Management (30 min)
- Implement time allocation
- Test with different time controls
- Tune parameters

### Phase 3: Time-Control Training (3 hours)
- Download bullet/blitz/rapid games
- Train separate models
- Evaluate performance

### Phase 4: Integration (30 min)
- Combine all components
- Test end-to-end
- Benchmark performance

**Total Time: ~5 hours**

---

## Success Metrics

### Performance Goals
- ✅ Never lose on time in bullet
- ✅ <1% time losses in blitz
- ✅ Use 90%+ of available time in rapid
- ✅ Maintain 2200+ ELO in all time controls

### Speed Goals
- ✅ Bullet: <0.5s per move average
- ✅ Blitz: <2s per move average
- ✅ Rapid: <5s per move average
- ✅ Classical: <10s per move average

### Accuracy Goals
- ✅ Bullet: 85%+ accuracy
- ✅ Blitz: 90%+ accuracy
- ✅ Rapid: 95%+ accuracy
- ✅ Classical: 98%+ accuracy

---

## After Chessy 1.3

### Chessy 2.0 (Future Vision)
- Transformer architecture
- Multi-GPU training
- Online play with matchmaking
- Real-time ELO tracking
- Opening book database (1M+ positions)
- Endgame tablebases (7-piece)
- Target: 2600+ ELO across all time controls

---

## Implementation Checklist

### Prerequisites
- [ ] Chessy 1.2 training complete
- [ ] Stockfish integration working
- [ ] Time management system designed
- [ ] Fast network architecture defined

### Development
- [ ] Implement TimeManager class
- [ ] Create fast CNN architecture
- [ ] Download time-control-specific games
- [ ] Train fast network
- [ ] Train standard network (already done)
- [ ] Train deep network
- [ ] Implement adaptive search
- [ ] Add opening books by time control

### Testing
- [ ] Test bullet performance
- [ ] Test blitz performance
- [ ] Test rapid performance
- [ ] Test classical performance
- [ ] Benchmark inference speed
- [ ] Verify time management
- [ ] Compare vs Chessy 1.2

### Deployment
- [ ] Update server with time control selection
- [ ] Add UI for time control choice
- [ ] Document usage
- [ ] Create comparison videos

---

## Ready to Implement?

**Wait for Chessy 1.2 to complete first!**

Then:
```bash
python train_chessy_1.3_time_controls.py
```

This will be the most versatile Chessy yet! ⚡🏃🎯🧠
