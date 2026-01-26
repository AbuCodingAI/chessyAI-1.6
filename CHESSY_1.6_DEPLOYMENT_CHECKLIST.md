# Chessy 1.6 Cloud Training - Deployment Checklist

## Pre-Deployment

- [ ] Build project locally
  ```bash
  cd chessy-1.6
  ./build.sh  # or build.bat on Windows
  ```

- [ ] Test training locally
  ```bash
  ./setup_cloud_training.sh  # or .bat on Windows
  python3 train_cloud.py
  ```

- [ ] Verify binary exists
  ```bash
  ls -la bin/chessy-1.6  # or bin/chessy-1.6.exe on Windows
  ```

- [ ] Check Stockfish
  ```bash
  ls -la stockfish/
  ```

- [ ] Review configuration
  ```bash
  cat training_config.json
  ```

---

## Local Testing Checklist

- [ ] Setup runs without errors
  ```bash
  ./setup_cloud_training.sh
  ```

- [ ] Directories created
  ```bash
  ls -la checkpoints/ models/ logs/
  ```

- [ ] Training starts
  ```bash
  python3 train_cloud.py
  ```

- [ ] Logs are generated
  ```bash
  tail -f training.log
  ```

- [ ] Checkpoints are created
  ```bash
  ls -la checkpoints/
  ```

- [ ] Training completes or stops gracefully
  - Check for "Training Complete" or "Early Stopping" message
  - Verify final model saved: `models/chessy-1.6-trained.bin`

---

## GitHub Preparation

- [ ] Repository initialized
  ```bash
  git init
  ```

- [ ] All files added
  ```bash
  git add .
  ```

- [ ] Commit created
  ```bash
  git commit -m "Add Chessy 1.6 cloud training"
  ```

- [ ] Remote configured
  ```bash
  git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
  ```

- [ ] Pushed to main branch
  ```bash
  git push -u origin main
  ```

- [ ] Verify on GitHub
  - Go to github.com/YOUR_USERNAME/YOUR_REPO
  - Check all files are present
  - Verify `train_cloud.py` is there

---

## Render Deployment

### Account Setup
- [ ] Render account created (render.com)
- [ ] GitHub connected to Render
- [ ] Repository authorized

### Worker Configuration
- [ ] Click "New +" → "Background Worker"
- [ ] Repository selected
- [ ] Configuration entered:
  - [ ] Name: `chessy-1.6-trainer`
  - [ ] Runtime: `Docker` or `Node`
  - [ ] Build Command: `./build.sh && pip install -r requirements.txt`
  - [ ] Start Command: `python3 train_cloud.py`
- [ ] Environment variables set (if needed):
  - [ ] `PYTHONUNBUFFERED=1`
  - [ ] `STOCKFISH_PATH=./stockfish/stockfish`

### Deployment
- [ ] Worker created
- [ ] Deployment started
- [ ] Build logs checked for errors
- [ ] Worker status shows "Live" (green)

---

## Post-Deployment Monitoring

### First Hour
- [ ] Logs show training started
- [ ] No build errors
- [ ] Data generation in progress
- [ ] Stockfish integration working (or fallback active)

### First 24 Hours
- [ ] Checkpoints being created
  ```bash
  # Check Render logs for checkpoint messages
  ```
- [ ] Validation loss decreasing
- [ ] No memory errors
- [ ] Training progressing normally

### Ongoing
- [ ] Check logs daily
- [ ] Monitor checkpoint creation
- [ ] Verify no errors in logs
- [ ] Training continues without interruption

---

## Troubleshooting Checklist

### Build Fails
- [ ] Check build logs in Render
- [ ] Verify C++ compiler available
- [ ] Check for missing dependencies
- [ ] Try building locally first

### Training Won't Start
- [ ] Check `train_cloud.py` exists
- [ ] Verify Python 3 installed
- [ ] Check binary exists: `bin/chessy-1.6`
- [ ] Review error logs

### Training Stops
- [ ] Check logs for errors
- [ ] Verify disk space available
- [ ] Check memory usage
- [ ] Look for timeout messages

### Checkpoints Not Saving
- [ ] Verify `checkpoints/` directory exists
- [ ] Check write permissions
- [ ] Ensure disk space available
- [ ] Review logs for save errors

### Validation Loss Not Improving
- [ ] Check learning rate (try 0.0005)
- [ ] Increase training data (try 2000 games)
- [ ] Increase epochs (try 200)
- [ ] Review overfitting settings

---

## Performance Verification

### Expected Metrics
- [ ] Data generation: 30-60 minutes
- [ ] Neural network training: 2-4 hours
- [ ] Self-play: 1-2 hours
- [ ] Testing: 30 minutes
- [ ] Total: 4-8 hours per cycle

### Expected Results
- [ ] Validation MSE: 0.5 → 0.1
- [ ] Self-play win rate: 55-65%
- [ ] vs Stockfish: 40-50%
- [ ] Estimated ELO: 1800-2200

### Resource Usage
- [ ] CPU: 2-4 cores utilized
- [ ] Memory: 2-4 GB used
- [ ] Disk: 1-2 GB for checkpoints/model

---

## Model Verification

### After Training Complete
- [ ] Final model exists: `models/chessy-1.6-trained.bin`
- [ ] Model size reasonable (>1 MB)
- [ ] Training logs show completion
- [ ] No errors in final output

### Download Model
- [ ] Connect to Render via SFTP or download from dashboard
- [ ] Verify file integrity
- [ ] Test loading model locally

---

## Continuous Training Setup

### Auto-Restart
- [ ] Render worker set to auto-restart on failure
- [ ] Checkpoint loading verified
- [ ] Resume from checkpoint working

### Monitoring
- [ ] Set up log alerts (if available)
- [ ] Check logs weekly
- [ ] Monitor disk usage
- [ ] Track training progress

### Maintenance
- [ ] Clean old checkpoints monthly
  ```bash
  ls -t checkpoints/ | tail -n +6 | xargs rm
  ```
- [ ] Archive completed models
- [ ] Review training metrics

---

## Deployment Success Criteria

✅ **All of the following must be true:**

- [ ] Project builds without errors
- [ ] Training runs locally successfully
- [ ] Code pushed to GitHub
- [ ] Render worker created and deployed
- [ ] Worker shows "Live" status
- [ ] Training logs visible in Render
- [ ] Checkpoints being created
- [ ] No errors in logs
- [ ] Training progressing normally
- [ ] Model will be saved on completion

---

## Rollback Plan

If deployment fails:

1. [ ] Stop Render worker
2. [ ] Check logs for errors
3. [ ] Fix issue locally
4. [ ] Test locally
5. [ ] Push to GitHub
6. [ ] Restart Render worker
7. [ ] Verify logs

---

## Documentation

- [ ] Read `CHESSY_1.6_CLOUD_TRAINING.md` (full guide)
- [ ] Read `CHESSY_1.6_CLOUD_SUMMARY.md` (implementation details)
- [ ] Read `CHESSY_1.6_CLOUD_QUICKSTART.md` (quick reference)
- [ ] Bookmark Render dashboard
- [ ] Save GitHub repository URL

---

## Final Verification

Before considering deployment complete:

```bash
# 1. Verify all files present
ls -la chessy-1.6/
ls -la chessy-1.6/src/training/
ls -la models/
ls -la checkpoints/

# 2. Check logs
tail -100 training.log

# 3. Verify model
ls -la models/chessy-1.6-trained.bin

# 4. Check Render dashboard
# - Worker status: Live
# - Logs: No errors
# - Checkpoints: Being created
```

---

## Sign-Off

- [ ] All checklist items completed
- [ ] Deployment successful
- [ ] Training running 24/7
- [ ] Monitoring in place
- [ ] Documentation reviewed

**Deployment Date**: _______________
**Deployed By**: _______________
**Status**: ✅ READY FOR PRODUCTION

---

## Next Steps

1. Monitor training for first 24 hours
2. Verify checkpoints being created
3. Check logs daily
4. Download model when training complete
5. Test trained model locally
6. Deploy trained model to production

---

**Questions?** See `CHESSY_1.6_CLOUD_TRAINING.md` for detailed troubleshooting.

🚀 Happy training!
