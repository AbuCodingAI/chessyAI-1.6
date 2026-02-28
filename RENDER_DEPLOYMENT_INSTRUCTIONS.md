# Deploy Chessy 1.6 Cloud Training to Render

## ⚠️ Important: Background Workers are Paid Only

Render's **Background Workers** require paid tier ($7/month minimum).

For **free tier**, use **Web Service** instead (see below).

---

## Option 1: Free Tier (Web Service) ✅ RECOMMENDED

**Cost**: $0
**Training Time**: 2-3 hours
**Quality**: Good (1600-1900 ELO)

See: `RENDER_DEPLOYMENT_FREE_TIER.md`

---

## Option 2: Paid Tier (Background Worker)

**Cost**: $7/month
**Training Time**: 4-8 hours continuous
**Quality**: Excellent (1800-2200 ELO)

### Deploy to Paid Tier

1. Go to [render.com](https://render.com)
2. Click "New +" → "Background Worker"
3. Select `chessyAI-1.6` repository
4. Configure:
   ```
   Name: chessy-1.6-trainer
   Build Command: ./build.sh && pip install -r requirements.txt
   Start Command: python3 train_cloud.py
   ```
5. Select **Paid Plan** ($7/month)
6. Click "Create Background Worker"

---

## Comparison

| Feature | Free (Web Service) | Paid (Background Worker) |
|---------|-------------------|------------------------|
| Cost | $0 | $7/month |
| Training Time | 2-3 hours | 4-8 hours |
| Quality | Good (1600-1900 ELO) | Excellent (1800-2200 ELO) |
| Sleep | After 15 min | Never |
| Sessions | Multiple | Single |

---

## Recommendation

### For Testing/Learning
**Use Free Tier** (Web Service)
- Cost: $0
- Time: 2-3 hours
- Quality: Good

### For Production
**Use Paid Tier** (Background Worker)
- Cost: $7/month
- Time: 4-8 hours
- Quality: Excellent

---

## Next Steps

1. **Free Tier**: See `RENDER_DEPLOYMENT_FREE_TIER.md`
2. **Paid Tier**: See below

---

## Paid Tier Deployment (Background Worker)

### Step 1: Go to Render
Open [render.com](https://render.com)

### Step 2: Create Background Worker
1. Click "New +" → "Background Worker"
2. Select `chessyAI-1.6` repository
3. Configure:
   ```
   Name: chessy-1.6-trainer
   Build Command: ./build.sh && pip install -r requirements.txt
   Start Command: python3 train_cloud.py
   ```
4. Click "Create Background Worker"

### Step 3: Select Paid Plan
- Choose **Starter Plan** ($7/month)
- Or higher tier for better performance

### Step 4: Monitor
- Go to worker dashboard
- Click "Logs"
- Watch training progress

---

## Support

For issues:
1. Check Render logs
2. Review troubleshooting section
3. See `RENDER_DEPLOYMENT_FREE_TIER.md` (free tier)
4. Check `training.log`

---

**Status**: ✅ Ready for Render (free or paid)
**Free Tier**: 2-3 hours, $0
**Paid Tier**: 4-8 hours, $7/month
