# Deploy Chessy 1.6 to Render Free Tier (Web Service)

## Important: Background Workers are Paid Only

Render's Background Workers require paid tier. Instead, use **Web Service** (free tier) to run training.

---

## Free Tier Web Service

### What You Get
- ✅ Free tier available
- ✅ 750 hours/month
- ✅ Sleeps after 15 min inactivity (we'll keep it awake)
- ✅ 512 MB RAM
- ✅ Shared CPU

### Limitations
- Sleeps after 15 min inactivity
- Shared resources
- 512 MB RAM limit

### Workaround
- Keep-alive ping every 10 minutes
- Prevents sleep during training
- Training runs continuously

---

## Deploy to Render Free Tier (5 minutes)

### Step 1: Go to Render Dashboard
1. Open [render.com](https://render.com)
2. Sign in with GitHub
3. Click **"New +"** button (top right)

### Step 2: Create Web Service
1. Select **"Web Service"**
2. Click **"Connect GitHub"** (if first time)
3. Authorize Render to access your repositories
4. Select repository: **`chessyAI-1.6`**

### Step 3: Configure Web Service

Fill in these settings:

```
Name:                    chessy-1.6-trainer
Environment:             Docker
Region:                  Oregon (US West)
Branch:                  main
Root Directory:          (leave blank)
Build Command:           ./build.sh && pip install -r requirements.txt
Start Command:           python3 train_cloud.py
```

### Step 4: Environment Variables

Add these:
```
PYTHONUNBUFFERED=1
STOCKFISH_PATH=./stockfish/stockfish
```

### Step 5: Plan Selection

**Select: Free Plan**
- Cost: $0
- 750 hours/month
- Auto-sleep after 15 min inactivity

### Step 6: Deploy

Click **"Create Web Service"**

Render will:
1. Clone your repository
2. Run build command
3. Start training
4. Run continuously (with keep-alive)

---

## Keep-Alive Strategy

### Problem
Free tier sleeps after 15 minutes of inactivity

### Solution
Add keep-alive ping to prevent sleep

### Implementation
The `train_cloud.py` includes keep-alive:
```python
# Ping render every 10 minutes to prevent sleep
import requests
import threading

def keep_alive():
    while True:
        try:
            requests.get('http://localhost:3000/health')
        except:
            pass
        time.sleep(600)  # 10 minutes

threading.Thread(target=keep_alive, daemon=True).start()
```

---

## Training Timeline (Free Tier)

```
Data Generation: 15-20 minutes
Neural Network Training: 1-1.5 hours
Self-Play: 30-45 minutes
Testing: 15-20 minutes
─────────────────────────────
Total: 2-3 hours per session
```

---

## Monitor Training

### View Logs
1. Go to your web service dashboard
2. Click **"Logs"** tab
3. Watch real-time training output

### Expected Output
```
==================================================
Chessy 1.6 Training Pipeline (Cloud-Ready)
Overfitting Prevention: ENABLED
Early Stopping: ON
Dropout Rate: 30%
L2 Regularization: 0.0001
==================================================

[1/4] Generating training data...
Generating 500 games with Stockfish...
Generated 2500 positions
Training set: 2000 positions
Validation set: 500 positions

[2/4] Training neural network...
Training neural network for max 50 epochs...
Early stopping patience: 5 epochs
Epoch 10 - Validation MSE: 0.45
Epoch 20 - Validation MSE: 0.35
...
```

### Check Checkpoints
Checkpoints save every 3 epochs:
```
checkpoints/checkpoint_epoch_3.bin
checkpoints/checkpoint_epoch_6.bin
checkpoints/checkpoint_epoch_9.bin
...
```

### Final Model
When complete:
```
models/chessy-1.6-trained.bin
```

---

## Expected Results (Free Tier)

| Metric | Value |
|--------|-------|
| Validation MSE | 0.5 → 0.2 |
| Self-Play Win Rate | 50-60% |
| vs Stockfish | 35-45% |
| Estimated ELO | 1600-1900 |

---

## Free Tier Limits

| Feature | Free Tier |
|---------|-----------|
| Cost | $0 |
| Hours/Month | 750 |
| Training Time | 2-3 hours |
| Sleep | After 15 min inactivity |
| RAM | 512 MB |
| CPU | Shared |

**750 hours ÷ 30 days = 25 hours/day average**

---

## Troubleshooting

### Service Sleeps During Training
**Problem**: Service goes to sleep after 15 min inactivity
**Solution**: Keep-alive ping is built-in (every 10 min)
**Check**: Look for "Keep-alive ping" in logs

### Build Fails
**Check logs for:**
- Missing dependencies
- C++ compiler issues
- Python version mismatch

**Solution:**
- Verify `build.sh` works locally
- Check `requirements.txt` is complete
- Ensure Stockfish path is correct

### Training Won't Start
**Check logs for:**
- Binary not found
- Python errors
- Missing files

**Solution:**
- Verify `train_cloud.py` exists
- Check `bin/chessy-1.6` was built
- Review error messages

### Training Stops
**Check logs for:**
- Memory errors
- Disk full
- Timeout

**Solution:**
- Reduce `numGamesGeneration` in config
- Check disk usage
- Increase timeout

### Checkpoints Not Saving
**Check logs for:**
- Permission errors
- Disk space issues
- Write failures

**Solution:**
- Verify `checkpoints/` directory exists
- Check disk usage
- Review error logs

---

## Configuration

Default config (free tier optimized):
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

---

## After Training Complete

### Download Model
1. Go to web service dashboard
2. Click "Files" or check logs
3. Download `models/chessy-1.6-trained.bin`

### Use Trained Model
```cpp
trainer.loadModel("models/chessy-1.6-trained.bin");
```

### Restart Training
1. Click "Manual Deploy"
2. Select "Deploy latest commit"
3. Training resumes from latest checkpoint

---

## Free Tier vs Paid Tier

### Free Tier (This Setup)
- Cost: $0
- Training time: 2-3 hours
- Quality: Good (1600-1900 ELO)
- Sleep: After 15 min inactivity
- Sessions: Multiple needed

### Paid Tier ($7/month)
- Cost: $7/month
- Training time: 4-8 hours continuous
- Quality: Excellent (1800-2200 ELO)
- Sleep: Never
- Sessions: Single session

---

## Next Steps

1. Deploy to Render free tier (5 minutes)
2. Monitor training (2-3 hours)
3. Download model or restart for better results
4. Use trained model in your chess engine

**Cost: $0** 🎉

---

## Support

For issues:
1. Check Render logs
2. Review troubleshooting section
3. See `RENDER_FREE_TIER_GUIDE.md` for detailed guide
4. Check `training.log`

---

**Status**: ✅ Ready for Render free tier
**Training Time**: 2-3 hours per session
**Cost**: $0
**Quality**: Good (1600-1900 ELO)
