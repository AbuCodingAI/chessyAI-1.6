# Quick Deploy to Render (5 Minutes)

## TL;DR - Deploy Now

### Step 1: Go to Render
https://render.com → Sign in with GitHub

### Step 2: Create Web Service
Click **"New +"** → **"Web Service"**

### Step 3: Connect Repository
- Click **"Connect GitHub"**
- Select: **`chessyAI-1.6`**
- Branch: **`main`**

### Step 4: Configure Service

```
Name:                    chessy-1.6-trainer
Environment:             Docker
Region:                  Oregon (US West)
Build Command:           (leave blank - uses Dockerfile)
Start Command:           python3 train_cloud.py
```

### Step 5: Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**

```
PYTHONUNBUFFERED = 1
STOCKFISH_PATH = ./stockfish/stockfish
```

### Step 6: Select Plan

**Select: Free Plan** ($0/month)

### Step 7: Deploy

Click **"Create Web Service"**

---

## That's It! ✅

Render will:
1. Clone your repository
2. Build Docker image
3. Start training
4. Keep running (with keep-alive)

---

## Monitor Training

1. Go to Render dashboard
2. Click `chessy-1.6-trainer`
3. Click **"Logs"** tab
4. Watch training progress

---

## Expected Timeline

```
Build:        5-10 minutes
Data Gen:     15-20 minutes
Training:     1-1.5 hours
Self-Play:    30-45 minutes
Testing:      15-20 minutes
─────────────────────────
Total:        2-3 hours
```

---

## What to Look For in Logs

✅ **Good Signs:**
```
[1/4] Generating training data...
Generated 2500 positions
[2/4] Training neural network...
Epoch 10 - Validation MSE: 0.45
[Keep-Alive] Ping successful (200)
```

❌ **Bad Signs:**
```
ERROR: Build failed
ERROR: Binary not found
ERROR: Stockfish not found
```

---

## After Training (2-3 hours)

### Option 1: Download Model
1. Go to Render dashboard
2. Click "Files"
3. Download `models/chessy-1.6-trained.bin`

### Option 2: Restart Training
1. Click "Manual Deploy"
2. Training resumes from checkpoint
3. Improves model quality

---

## Cost

**$0** - Free tier, no credit card required

---

## Troubleshooting

### Service won't start?
- Check logs for errors
- Verify Dockerfile is correct
- Check build.sh works locally

### Training stops?
- Check memory usage
- Verify disk space
- Review error logs

### Service sleeps?
- Keep-alive is automatic (every 10 min)
- Check logs for "Keep-Alive" messages

---

## That's All!

Your Chessy 1.6 is now training in the cloud. ☁️

Check logs every 30 minutes to monitor progress.

---

**Questions?** See `DEPLOYMENT_READY.md` for detailed guide.

