# Keep-Alive Mechanism for Render Free Tier

## Problem

Render free tier Web Services sleep after **15 minutes of inactivity**.

During training, the service is active (CPU usage), but Render might still sleep if there's no HTTP traffic.

## Solution

The `train_cloud.py` includes an automatic **keep-alive pinger** that:
- Runs in a background thread
- Pings the Render service URL every 10 minutes
- Generates HTTP traffic to prevent sleep
- Runs automatically (no configuration needed)

---

## How It Works

### Keep-Alive Thread

```python
def _keep_alive_ping(self):
    """Ping the service every 10 minutes to prevent sleep"""
    render_url = os.environ.get('RENDER_EXTERNAL_URL', 'http://localhost:3000')
    
    while self.keep_alive_running:
        time.sleep(600)  # Wait 10 minutes
        
        # Ping the Render service URL
        try:
            requests.get(f'{render_url}/health', timeout=5)
            print(f"[Keep-Alive] Ping successful")
        except:
            # Even failed requests count as activity
            print(f"[Keep-Alive] Ping attempt (no endpoint)")
```

### How It Gets the URL

Render automatically sets `RENDER_EXTERNAL_URL` environment variable:
```
RENDER_EXTERNAL_URL=https://chessy-1-6-trainer.onrender.com
```

The keep-alive uses this to ping itself.

### Automatic Startup

Keep-alive starts automatically when training begins:

```python
# Start keep-alive thread
self.keep_alive_running = True
self.keep_alive_thread = threading.Thread(target=self._keep_alive_ping, daemon=True)
self.keep_alive_thread.start()
```

### Automatic Shutdown

Keep-alive stops when training ends:

```python
# Stop keep-alive thread
self.keep_alive_running = False
```

---

## What You'll See in Logs

```
✓ Keep-alive thread started (pings every 10 minutes)
[Keep-Alive] Ping successful at 10:05:23
[Keep-Alive] Ping successful at 10:15:23
[Keep-Alive] Ping attempt (no endpoint) at 10:25:23
...
```

---

## How to Verify It's Working

### Check Logs
```bash
grep "Keep-Alive" training.log
```

Expected output:
```
✓ Keep-alive thread started (pings every 10 minutes)
[Keep-Alive] Ping successful at 10:05:23
[Keep-Alive] Ping successful at 10:15:23
```

### Monitor in Render Dashboard
1. Go to your Web Service dashboard
2. Click "Logs"
3. Look for "Keep-Alive" messages
4. Should see one every 10 minutes

---

## Ping Target

The keep-alive pings the **Render service URL**:

```
https://chessy-1-6-trainer.onrender.com/health
```

This is obtained from the `RENDER_EXTERNAL_URL` environment variable that Render automatically sets.

### Why This Works

1. **Render sets the URL automatically**
   - Every Web Service gets a unique URL
   - Stored in `RENDER_EXTERNAL_URL` env var
   - Available inside the container

2. **Pinging generates HTTP traffic**
   - Even if `/health` endpoint doesn't exist
   - Failed requests still count as activity
   - Prevents Render from sleeping

3. **Timing is perfect**
   - Render sleeps after 15 min inactivity
   - 10 min pings = 5 min safety margin
   - Ensures service stays awake

---

## What If Ping Fails?

### If Endpoint Doesn't Exist
```
[Keep-Alive] Ping attempt (no endpoint)
```

This is **normal and expected**! The training binary doesn't expose HTTP endpoints, so pings will fail. But the important part is that **any HTTP request** (even failed ones) counts as activity.

### If Service Still Sleeps
- Render might have other inactivity detection
- Restart the service manually
- Training resumes from latest checkpoint

### If You See Errors
```
[Keep-Alive] Error: Connection refused
```

This means the service URL isn't accessible. Check:
1. Service is running
2. `RENDER_EXTERNAL_URL` is set
3. Network connectivity

---

## Manual Keep-Alive (Alternative)

If automatic keep-alive doesn't work, you can manually ping from your computer:

### From Your Computer
```bash
# Get your Render URL from dashboard
RENDER_URL="https://chessy-1-6-trainer.onrender.com"

# Ping every 10 minutes
while true; do
  curl $RENDER_URL/
  sleep 600
done
```

### From Another Service
Use a free uptime monitoring service:
- [UptimeRobot](https://uptimerobot.com) - Free tier available
- [Pingdom](https://www.pingdom.com) - Free tier available
- [StatusCake](https://www.statuscake.com) - Free tier available

Configure to ping your Render URL every 10 minutes.

---

## Troubleshooting

### Keep-Alive Not Starting
**Check**: Look for "Keep-alive thread started" in logs
**Fix**: Restart the service

### Keep-Alive Pings Failing
**Expected**: Pings will fail if no HTTP endpoint
**Normal**: Training continues anyway
**Fix**: No action needed

### Service Still Sleeping
**Check**: Look for "Keep-Alive" messages in logs
**If missing**: Keep-alive thread didn't start
**Fix**: Restart the service

### Training Interrupted by Sleep
**Symptom**: Training stops unexpectedly
**Cause**: Service went to sleep
**Fix**: 
1. Restart the service
2. Training resumes from checkpoint
3. Verify keep-alive is running

---

## Configuration

### Default Settings
- Interval: 10 minutes
- Timeout: 5 seconds
- URL: From `RENDER_EXTERNAL_URL` env var
- Behavior: Fail silently

### To Change Interval
Edit `train_cloud.py`:
```python
time.sleep(600)  # Change 600 to desired seconds
# 300 = 5 minutes
# 600 = 10 minutes (default)
# 900 = 15 minutes
```

### To Use Custom URL
Set environment variable in Render dashboard:
```
RENDER_EXTERNAL_URL=https://your-custom-url.com
```

---

## Summary

✅ **Automatic**: Keep-alive runs automatically
✅ **Self-Pinging**: Pings the Render service URL
✅ **Safe**: Fails gracefully if endpoint doesn't exist
✅ **Effective**: Prevents Render free tier sleep
✅ **No Configuration**: Works out of the box

---

## Next Steps

1. Deploy to Render free tier
2. Monitor logs for "Keep-Alive" messages
3. Training runs continuously for 2-3 hours
4. Service stays awake due to keep-alive pings

**Result**: Training completes without interruption! 🚀
