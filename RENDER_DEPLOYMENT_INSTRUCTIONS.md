# Deploy Chessy 1.6 Cloud Training to Render

## ✅ Repository Ready

Your code is now on GitHub at:
```
https://github.com/AbuCodingAI/chessyAI-1.6
```

## Deploy to Render (5 minutes)

### Step 1: Go to Render Dashboard
1. Open [render.com](https://render.com)
2. Sign in with your GitHub account
3. Click **"New +"** button (top right)

### Step 2: Create Background Worker
1. Select **"Background Worker"**
2. Click **"Connect GitHub"** (if first time)
3. Authorize Render to access your repositories
4. Select repository: **`chessyAI-1.6`**

### Step 3: Configure Worker

Fill in these settings:

```
Name:                    chessy-1.6-trainer
Runtime:                 Docker
Region:                  Oregon (US West)
Branch:                  main
Root Directory:          (leave blank)
Dockerfile Path:         chessy-1.6/Dockerfile
```

**Note**: Render will automatically use the Dockerfile to build and run your project. The `.sh` scripts work fine on Render's Linux servers, even though you're on Windows.

### Step 4: Environment Variables (Optional)

Add these if needed:
```
PYTHONUNBUFFERED=1
STOCKFISH_PATH=./stockfish/stockfish
```

### Step 5: Advanced Settings

- **Auto-Deploy**: Yes (recommended)
- **Disk**: 10 GB (for checkpoints and model)
- **Timeout**: 86400 seconds (24 hours)

### Step 6: Deploy

Click **"Create Background Worker"**

Render will:
1. Clone your repository
2. Build Docker image (using Dockerfile)
3. Start training
4. Run continuously

---

## Why Docker?

You're on Windows, but Render runs on Linux. The Dockerfile handles this automatically:
- Installs Linux dependencies
- Downloads Stockfish for Linux
- Builds the C++ project
- Runs the training

You don't need to do anything special on Windows!

---

## Monitor Training

### View Logs
1. Go to your worker dashboard
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
Generating 1000 games with Stockfish...
Generated 5000 positions
Training set: 4000 positions
Validation set: 1000 positions

[2/4] Training neural network...
Training neural network for max 100 epochs...
Early stopping patience: 10 epochs
Epoch 10 - Validation MSE: 0.45
Epoch 20 - Validation MSE: 0.35
...
```

### Check Checkpoints
Checkpoints save every 5 epochs:
```
checkpoints/checkpoint_epoch_5.bin
checkpoints/checkpoint_epoch_10.bin
checkpoints/checkpoint_epoch_15.bin
...
```

### Final Model
When complete:
```
models/chessy-1.6-trained.bin
```

---

## Troubleshooting

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
- Increase disk size
- Reduce `numGamesGeneration` in config
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

## Expected Timeline

| Phase | Duration |
|-------|----------|
| Build | 2-5 minutes |
| Data Generation | 30-60 minutes |
| Neural Network Training | 2-4 hours |
| Self-Play | 1-2 hours |
| Testing | 30 minutes |
| **Total** | **4-8 hours** |

---

## Monitoring Checklist

- [ ] Worker shows "Live" status (green)
- [ ] Logs show training started
- [ ] Data generation in progress
- [ ] Checkpoints being created
- [ ] Validation loss decreasing
- [ ] No errors in logs
- [ ] Training progressing normally

---

## After Training Complete

### Download Model
1. Go to worker dashboard
2. Click **"Files"** or **"Logs"**
3. Download `models/chessy-1.6-trained.bin`

### Use Trained Model
```cpp
trainer.loadModel("models/chessy-1.6-trained.bin");
```

### Restart Training
1. Click **"Manual Deploy"**
2. Select **"Deploy latest commit"**
3. Training resumes from latest checkpoint

---

## Pricing

### Free Tier
- 750 hours/month
- Shared resources
- Good for testing

### Paid Tier ($7/month)
- Always on (no sleep)
- Better performance
- Recommended for production

---

## Support

For issues:
1. Check logs in Render dashboard
2. Review `CHESSY_1.6_CLOUD_TRAINING.md`
3. Check `training.log` in worker
4. See troubleshooting section above

---

## Next Steps

1. ✅ Code pushed to GitHub
2. ⏳ Deploy to Render (5 min)
3. ⏳ Monitor training (4-8 hours)
4. ⏳ Download trained model
5. ⏳ Use in production

---

**Repository**: https://github.com/AbuCodingAI/chessyAI-1.6
**Status**: ✅ Ready for Render deployment
**Training**: 24/7 continuous on cloud

🚀 Deploy now!
