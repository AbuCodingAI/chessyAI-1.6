# Chessy 1.6 Cloud Training Guide

## Overview

Chessy 1.6 now supports continuous training on cloud servers with built-in overfitting prevention. Your neural network can train 24/7 while your computer is off.

## What's New

✅ **Overfitting Prevention**
- Early stopping (stops when validation loss plateaus)
- Dropout regularization (30% default)
- L2 weight decay (0.0001)
- Data augmentation (20% of training data)
- K-fold cross-validation support

✅ **Cloud-Ready Features**
- Automatic checkpointing every 5 epochs
- Resume from checkpoint on restart
- Time-aware training (stops gracefully before timeout)
- Comprehensive logging

✅ **Deployment Options**
- Render (recommended, free tier available)
- AWS, DigitalOcean, Heroku, or any cloud provider

---

## Quick Start: Deploy to Render

### Step 1: Prepare Your Repository

```bash
cd chessy-1.6
git add .
git commit -m "Add cloud training support"
git push origin main
```

### Step 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Authorize Render to access your repositories

### Step 3: Deploy Training Worker

1. Click **"New +"** → **"Background Worker"**
2. Select your repository
3. Configure:
   ```
   Name: chessy-1.6-trainer
   Runtime: Docker
   Build Command: ./build.sh && pip install -r requirements.txt
   Start Command: python3 train_cloud.py
   ```
4. Click **"Create Background Worker"**

### Step 4: Monitor Training

1. Go to your worker dashboard
2. Click **"Logs"** to see real-time training output
3. Training will run continuously for 24 hours
4. Checkpoints save every 5 epochs

---

## Local Testing

### Test the Training Pipeline

```bash
# Build the project
./build.bat  # Windows
./build.sh   # Linux/macOS

# Run training locally
python3 train_cloud.py

# Or directly
./bin/chessy-1.6 --train
```

### Monitor Progress

```bash
# Watch checkpoints being created
ls -la checkpoints/

# View training logs
tail -f training.log
```

---

## Overfitting Prevention Details

### Early Stopping
- **Patience**: 10 epochs without improvement
- **Threshold**: 0.001 minimum improvement
- **Benefit**: Prevents wasting compute on plateaued training

### Dropout
- **Rate**: 30% of features randomly dropped
- **Effect**: Forces network to learn robust features
- **Applied**: During both training and validation

### L2 Regularization
- **Weight**: 0.0001
- **Effect**: Penalizes large weights
- **Benefit**: Prevents overfitting to training data

### Data Augmentation
- **Rate**: 20% of training data
- **Method**: Add ±5 centipawn noise to evaluations
- **Benefit**: Increases training data diversity

### Validation Strategy
- **Split**: 80% training, 20% validation
- **K-Fold**: 5-fold cross-validation support
- **Monitoring**: Validation loss tracked every epoch

---

## Configuration

Edit `training_config.json` to customize:

```json
{
  "numGamesGeneration": 1000,      // More games = better training
  "stockfishDepth": 15,             // Deeper = stronger but slower
  "blunderRate": 0.05,              // 5% blunder injection
  "epochs": 100,                    // Max epochs (early stop may end earlier)
  "learningRate": 0.001,            // Lower = slower but more stable
  "overfitting": {
    "enableEarlyStopping": true,
    "patienceEpochs": 10,           // Stop after 10 epochs no improvement
    "dropoutRate": 0.3,             // 30% dropout
    "l2Regularization": 0.0001,
    "enableDataAugmentation": true,
    "augmentationRate": 0.2         // Augment 20% of data
  },
  "isCloudDeployment": true,
  "maxTrainingHours": 24            // Stop before timeout
}
```

---

## Checkpointing System

### How It Works

1. **Automatic Saves**: Every 5 epochs
2. **Location**: `./checkpoints/checkpoint_epoch_N.bin`
3. **Resume**: Automatically loads latest checkpoint on restart
4. **Safety**: Never loses progress

### Manual Checkpoint Management

```bash
# List all checkpoints
ls -la checkpoints/

# Load specific checkpoint
./bin/chessy-1.6 --load-checkpoint checkpoints/checkpoint_epoch_50.bin

# Clean old checkpoints (keep last 5)
ls -t checkpoints/checkpoint_epoch_*.bin | tail -n +6 | xargs rm
```

---

## Deployment Platforms

### Render (Recommended)
- **Cost**: Free tier available
- **Setup**: 5 minutes
- **Pros**: Simple, GitHub integration, auto-deploy
- **Cons**: Free tier has 750 hours/month limit

### AWS EC2
- **Cost**: ~$0.05/hour (t3.micro)
- **Setup**: 15 minutes
- **Pros**: Scalable, reliable
- **Cons**: More complex setup

### DigitalOcean
- **Cost**: $5-40/month
- **Setup**: 10 minutes
- **Pros**: Simple, affordable
- **Cons**: Manual management

### Heroku
- **Cost**: $7/month (paid dyno)
- **Setup**: 5 minutes
- **Pros**: Simple, GitHub integration
- **Cons**: Expensive for long training

---

## Monitoring & Logs

### Real-Time Monitoring

```bash
# Watch training progress
tail -f training.log

# Check checkpoint creation
watch -n 5 'ls -la checkpoints/ | tail -5'

# Monitor system resources
top
```

### Log Analysis

```bash
# Extract training metrics
grep "Epoch" training.log

# Find early stopping events
grep "Early stopping" training.log

# Check validation loss trend
grep "Validation MSE" training.log
```

---

## Troubleshooting

### Training Stops Unexpectedly

**Check logs for:**
```bash
grep "ERROR\|FATAL" training.log
```

**Common issues:**
- Out of memory: Reduce `numGamesGeneration`
- Stockfish not found: Install or provide path
- Time limit exceeded: Increase `maxTrainingHours`

### Validation Loss Not Improving

**Possible causes:**
- Learning rate too high: Reduce to 0.0005
- Learning rate too low: Increase to 0.002
- Insufficient data: Increase `numGamesGeneration`
- Model capacity: Increase hidden layer sizes

### Checkpoints Not Saving

**Check:**
```bash
ls -la checkpoints/
```

**If empty:**
- Verify write permissions
- Check disk space: `df -h`
- Ensure `enableCheckpointing: true`

---

## Performance Tips

### Faster Training
1. Reduce `stockfishDepth` to 12
2. Reduce `numGamesGeneration` to 500
3. Increase `learningRate` to 0.002
4. Disable `enableDataAugmentation`

### Better Results
1. Increase `numGamesGeneration` to 2000
2. Increase `stockfishDepth` to 18
3. Increase `epochs` to 200
4. Enable `enableCrossValidation`

### Balanced Setup
- `numGamesGeneration`: 1000
- `stockfishDepth`: 15
- `epochs`: 100
- `learningRate`: 0.001
- All overfitting prevention enabled

---

## Expected Results

### Training Timeline
- **Data Generation**: 30-60 minutes
- **Neural Network Training**: 2-4 hours
- **Self-Play**: 1-2 hours
- **Testing vs Stockfish**: 30 minutes
- **Total**: 4-8 hours per full cycle

### Performance Metrics
- **Validation MSE**: Should decrease from ~0.5 to ~0.1
- **Self-Play Win Rate**: Target 55-65%
- **vs Stockfish**: Target 40-50% (depth 10)
- **Estimated ELO**: 1800-2200

---

## Advanced: Custom Training

### Modify Training Config

```cpp
// In trainer.cpp
TrainingConfig config;
config.numGamesGeneration = 2000;  // More data
config.stockfishDepth = 18;        // Stronger analysis
config.epochs = 200;               // More training
config.overfitting.dropoutRate = 0.4;  // More regularization
```

### Add Custom Evaluation

```cpp
// In trainer.cpp, modify testVsStockfish()
// Add your own evaluation metrics
```

---

## FAQ

**Q: Will training continue if my computer is off?**
A: Yes! Training runs on the cloud server, not your computer.

**Q: How much does it cost?**
A: Render free tier: $0. Paid tier: $7/month. AWS: ~$1.20/day.

**Q: Can I stop training and resume later?**
A: Yes! Checkpoints save automatically. Just restart the worker.

**Q: How do I use the trained model?**
A: The model saves to `models/chessy-1.6-trained.bin`. Load it with:
```cpp
trainer.loadModel("models/chessy-1.6-trained.bin");
```

**Q: What if training gets interrupted?**
A: Latest checkpoint loads automatically on restart. No progress lost.

**Q: Can I train multiple instances?**
A: Yes, but they'll overwrite each other's models. Use different output paths.

---

## Next Steps

1. ✅ Build the project locally
2. ✅ Test training with `python3 train_cloud.py`
3. ✅ Push to GitHub
4. ✅ Deploy to Render
5. ✅ Monitor training progress
6. ✅ Download trained model when complete

---

## Support

For issues:
1. Check `training.log` for errors
2. Review this guide's troubleshooting section
3. Check Render/cloud provider logs
4. Verify Stockfish is installed

Happy training! 🚀♟️
