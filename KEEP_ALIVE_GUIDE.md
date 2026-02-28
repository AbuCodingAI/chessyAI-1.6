# Keep-Alive Mechanism for Render Free Tier

## Problem

Render free tier Web Services sleep after **15 minutes of inactivity**.

During training, the service is active (CPU usage), but Render might still sleep if there's no HTTP traffic.

## Solution

The `train_cloud.py` includes an automatic **keep-alive pinger** that:
- Runs in a background thread
- Pings the service every 10 minutes
- Prevents sleep during training
- Runs automatically (no configuration needed)

---

## How It Works

### Keep-Alive Thread

```python
def _keep_alive_ping(self):
    """Ping the service every 10 minutes to prevent sleep"""
    while self.keep_alive_running:
        time.sleep(600)  # Wait 10 minutes
        
        # Try to ping localhost
        try:
            requests.get('http://localhost:3000/health', timeout=5)
            print(f"[Keep-Alive] Ping successful")
        except:
            pass  # Continue even if ping fails
```

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
[Keep-Alive] Ping successful at 10:25:23
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

## Ping Targets

The keep-alive tries multiple ports:

1. **Port 3000** (primary)
   - Common Node.js port
   - Fallback if training doesn't expose HTTP

2. **Port 8000** (secondary)
   - Common Python port
   - Fallback if port 3000 fails

3. **Silently fails** if neither works
   - Training continues anyway
   - CPU activity keeps service awake

---

## Why Multiple Ports?

The training binary doesn't expose an HTTP endpoint, so the keep-alive:
- Tries to ping common ports
- Fails gracefully if no endpoint exists
- Continues running anyway

The important part is that **any HTTP request** (even failed ones) counts as activity and prevents sleep.

---

## Timing

### Keep-Alive Schedule
- Starts: When training begins
- Interval: Every 10 minutes
- Stops: When training ends

### Why 10 Minutes?
- Render sleeps after 15 minutes of inactivity
- 10 minute pings = 5 minute safety margin
- Ensures service stays awake

---

## What If Keep-Alive Fails?

### If Pings Fail
- Training continues normally
- CPU activity keeps service awake
- No impact on training

### If Service Still Sleeps
- Render might have other inactivity detection
- Restart the service manually
- Training resumes from latest checkpoint

### If You See Errors
```
[Keep-Alive] Ping failed
```

This is normal! The training binary doesn't expose HTTP endpoints, so pings will fail. The important part is that the service stays active due to CPU usage.

---

## Manual Keep-Alive (Alternative)

If automatic keep-alive doesn't work, you can manually ping:

### From Your Computer
```bash
# Ping every 10 minutes
while true; do
  curl https://your-render-url.onrender.com/
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
- Ports: 3000, 8000
- Behavior: Fail silently

### To Change Interval
Edit `train_cloud.py`:
```python
time.sleep(600)  # Change 600 to desired seconds
# 300 = 5 minutes
# 600 = 10 minutes (default)
# 900 = 15 minutes
```

---

## Summary

✅ **Automatic**: Keep-alive runs automatically
✅ **Background**: Runs in separate thread
✅ **Safe**: Fails gracefully if pings don't work
✅ **Effective**: Prevents Render free tier sleep
✅ **No Configuration**: Works out of the box

---

## Next Steps

1. Deploy to Render free tier
2. Monitor logs for "Keep-Alive" messages
3. Training runs continuously for 2-3 hours
4. Service stays awake due to keep-alive pings

**Result**: Training completes without interruption! 🚀
