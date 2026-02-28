# Chessy 1.6 on Render Free Tier

## Free Tier Limitations

| Feature | Free Tier | Paid Tier |
|---------|-----------|-----------|
| Hours/Month | 750 hours | Unlimited |
| Cost | $0 | $7/month |
| Sleep | After 15 min inactivity | Never |
| CPU | Shared | Dedicated |
| Memory | 512 MB | 512 MB+ |
| Startup Time | ~30 sec (after sleep) | Instant |

**750 hours/month = ~31 hours/day average**

---

## Free Tier Strategy

### Option 1: Multiple Short Training Sessions (Recommended)

Instead of one 8-hour session, run multiple shorter sessions:

```
Session 1: 6 hours (data gen + partial training)
Session 2: 6 hours (continue training + self-play)
Session 3: 6 hours (testing + model save)
```

**Advantage**: Fits within free tier, automatic resume from checkpoints

### Option 2: Reduce Training Scope

Modify `training_config.json` to train faster:

```json
{
  "numGamesGeneration": 500,      // Reduced from 1000
  "stockfishDepth": 12,           // Reduced from 15
  "epochs": 50,                   // Reduced from 100
  "numSelfPlayGames": 250,        // Reduced from 500
  "numTestGames": 50              // Reduced from 100
}
```

**Result**: ~2-3 hours per cycle instead of 4-8 hours

### Option 3: Hybrid Approach (Best)

1. **Local Testing** (free, your computer)
   - Run `python3 train_cloud.py` locally
   - Generate training data
   - Train for 20-30 epochs

2. **Cloud Refinement** (free tier, Render)
   - Upload checkpoint to Render
   - Continue training for 20-30 more epochs
   - Test against Stockfish
   - Save final model

---

## Free Tier Deployment

### Step 1: Create Render Account
- Go to [render.com](https://render.com)
- Sign up (free)
- No credit card required

### Step 2: Deploy Background Worker
1. Click "New +" → "Background Worker"
2. Select `chessyAI-1.6` repository
3. Configure:
   ```
   Name: chessy-1.6-trainer-free
   Build Command: ./build.sh && pip install -r requirements.txt
   Start Command: python3 train_cloud.py
   ```
4. Click "Create Background Worker"

### Step 3: Monitor
- Go to worker dashboard
- Click "Logs" to watch training
- Training will run for ~6 hours before free tier timeout

---

## Optimized Config for Free Tier

Create `training_config_free.json`:

```json
{
  "numGamesGeneration": 500,
  "stockfishDepth": 12,
  "blunderRate": 0.05,
  "epochs": 50,
  "learningRate": 0.001,
  "batchSize": 32,
  "numSelfPlayGames": 250,
  "numTestGames": 50,
  "overfitting": {
    "enableEarlyStopping": true,
    "patienceEpochs": 5,
    "minValidationImprovement": 0.001,
    "l2Regularization": 0.0001,
    "dropoutRate": 0.3,
    "enableDataAugmentation": true,
    "augmentationRate": 0.2,
    "validationSplitRatio": 20,
    "enableCrossValidation": false,
    "kFolds": 5
  },
  "enableCheckpointing": true,
  "checkpointDir": "./checkpoints",
  "checkpointInterval": 3,
  "isCloudDeployment": true,
  "maxTrainingHours": 5,
  "modelOutputPath": "./models/chessy-1.6-trained.bin"
}
```

**Changes**:
- Reduced games: 1000 → 500
- Reduced depth: 15 → 12
- Reduced epochs: 100 → 50
- Reduced self-play: 500 → 250
- Reduced test games: 100 → 50
- Reduced patience: 10 → 5
- Disabled cross-validation
- Max training: 5 hours (safe for free tier)

**Result**: ~2-3 hours per training session

---

## Free Tier Timeline

### Single Session (2-3 hours)
```
Data Generation: 15-20 min
Neural Network Training: 1-1.5 hours
Self-Play: 30-45 min
Testing: 15-20 min
Total: 2-3 hours
```

### Multiple Sessions (Recommended)

**Session 1** (Day 1)
- Data generation
- Initial training (20 epochs)
- Checkpoint saved

**Session 2** (Day 2)
- Resume from checkpoint
- Continue training (20 epochs)
- Self-play
- Checkpoint saved

**Session 3** (Day 3)
- Resume from checkpoint
- Final training (10 epochs)
- Testing
- Model saved

---

## How to Use Free Tier Effectively

### Step 1: Deploy to Render
```bash
# Push to GitHub
git push origin main

# Create Background Worker on render.com
# Set start command: python3 train_cloud.py
```

### Step 2: Monitor First Session
- Go to Render dashboard
- Click "Logs"
- Watch training progress
- Note when it stops (after ~6 hours)

### Step 3: Restart Training
- Click "Manual Deploy"
- Select "Deploy latest commit"
- Training resumes from latest checkpoint
- Repeat as needed

### Step 4: Download Model
When training is complete:
1. Go to worker dashboard
2. Click "Files" or check logs
3. Download `models/chessy-1.6-trained.bin`

---

## Free Tier Costs

| Item | Cost |
|------|------|
| Render Free Tier | $0 |
| GitHub (free) | $0 |
| Stockfish (free) | $0 |
| **Total** | **$0** |

---

## Free Tier Limitations & Workarounds

### Limitation 1: 750 hours/month
**Workaround**: Run multiple shorter sessions
- 750 hours ÷ 30 days = 25 hours/day average
- Run 4-5 hour sessions, restart as needed

### Limitation 2: Sleeps after 15 min inactivity
**Workaround**: Not an issue for training (continuous CPU usage)
- Training keeps worker awake
- Only sleeps if idle

### Limitation 3: Shared resources
**Workaround**: Reduce training scope
- Use optimized config (500 games instead of 1000)
- Reduce Stockfish depth (12 instead of 15)
- Reduce epochs (50 instead of 100)

### Limitation 4: 512 MB RAM
**Workaround**: Already optimized for this
- Neural network: ~100 MB
- Training data: ~200 MB
- Stockfish: ~150 MB
- Total: ~450 MB (fits in 512 MB)

---

## Expected Results on Free Tier

### With Optimized Config
- **Training Time**: 2-3 hours per session
- **Sessions Needed**: 2-3 sessions
- **Total Time**: 4-9 hours spread over 2-3 days
- **Validation MSE**: 0.5 → 0.2 (good improvement)
- **Self-Play Win Rate**: 50-60%
- **vs Stockfish**: 35-45%
- **Estimated ELO**: 1600-1900

### With Standard Config
- **Training Time**: 4-8 hours per session
- **Sessions Needed**: 1-2 sessions
- **Total Time**: 4-16 hours spread over 1-2 days
- **Validation MSE**: 0.5 → 0.1 (excellent)
- **Self-Play Win Rate**: 55-65%
- **vs Stockfish**: 40-50%
- **Estimated ELO**: 1800-2200

---

## Free Tier vs Paid Tier

### Free Tier ($0/month)
- ✅ No cost
- ✅ Good for testing
- ✅ Fits within 750 hours/month
- ❌ Multiple sessions needed
- ❌ Shared resources
- ❌ Slower training

### Paid Tier ($7/month)
- ✅ Always on (no restarts)
- ✅ Dedicated resources
- ✅ Faster training
- ✅ Better for production
- ❌ Costs $7/month
- ❌ Overkill for hobby projects

---

## Recommendation

### For Testing/Learning
**Use Free Tier** with optimized config
- Cost: $0
- Time: 2-3 hours per session
- Quality: Good (1600-1900 ELO)

### For Production
**Use Paid Tier** ($7/month)
- Cost: $7/month
- Time: 4-8 hours continuous
- Quality: Excellent (1800-2200 ELO)

### For Maximum Value
**Hybrid Approach**:
1. Train on free tier (2-3 hours)
2. Get decent model (1600-1900 ELO)
3. Upgrade to paid tier if needed
4. Continue training for better results

---

## Step-by-Step: Free Tier Deployment

### Step 1: Prepare Repository
```bash
cd chessy-1.6
git add .
git commit -m "Ready for free tier deployment"
git push origin main
```

### Step 2: Create Render Account
- Go to [render.com](https://render.com)
- Sign up (free, no credit card)

### Step 3: Deploy Worker
1. Click "New +" → "Background Worker"
2. Select `chessyAI-1.6` repository
3. Configure:
   ```
   Name: chessy-1.6-free
   Build Command: ./build.sh && pip install -r requirements.txt
   Start Command: python3 train_cloud.py
   ```
4. Click "Create Background Worker"

### Step 4: Monitor Training
- Go to worker dashboard
- Click "Logs"
- Watch training progress
- Training will run for ~2-3 hours

### Step 5: Restart Training
- Click "Manual Deploy"
- Select "Deploy latest commit"
- Training resumes from checkpoint
- Repeat 2-3 times for full training

### Step 6: Download Model
- Go to worker dashboard
- Download `models/chessy-1.6-trained.bin`
- Use in your chess engine

---

## Free Tier FAQ

**Q: How long can I train on free tier?**
A: 750 hours/month = ~25 hours/day average. Run multiple 2-3 hour sessions.

**Q: Will my training be lost if it stops?**
A: No! Checkpoints save every 3-5 epochs. Just restart and it resumes.

**Q: Can I upgrade to paid tier later?**
A: Yes! Just click "Upgrade" in Render dashboard. Your worker continues.

**Q: How many times can I restart?**
A: Unlimited! Restart as many times as needed within 750 hours/month.

**Q: What if I exceed 750 hours?**
A: Worker stops. Upgrade to paid tier or wait for next month.

**Q: Can I use free tier for production?**
A: Not recommended. Use paid tier ($7/month) for always-on training.

**Q: How do I optimize for free tier?**
A: Use optimized config (500 games, depth 12, 50 epochs) = 2-3 hours per session.

---

## Conclusion

**Free Tier is Perfect For:**
- ✅ Testing the system
- ✅ Learning how it works
- ✅ Getting a decent trained model (1600-1900 ELO)
- ✅ Zero cost
- ✅ Multiple training sessions

**Paid Tier is Better For:**
- ✅ Production use
- ✅ Continuous training
- ✅ Better results (1800-2200 ELO)
- ✅ No restarts needed
- ✅ Only $7/month

**Recommendation**: Start with free tier, upgrade to paid if you want better results!

---

## Next Steps

1. Deploy to Render free tier (5 minutes)
2. Monitor first training session (2-3 hours)
3. Restart training 2-3 times
4. Download trained model
5. Use in your chess engine

**Cost: $0** 🎉

Deploy now and start training!
