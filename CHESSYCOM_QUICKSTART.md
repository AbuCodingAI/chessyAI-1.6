# 🚀 ChessyCom Quick Start Guide

## Get Your Local Multiplayer Chess Running in 5 Minutes!

---

## Step 1: Install Node.js

1. Download Node.js from: https://nodejs.org/
2. Install it (just click Next, Next, Finish)
3. Verify installation:
   ```bash
   node --version
   npm --version
   ```

---

## Step 2: Install Dependencies

Open PowerShell in your Chessy folder and run:

```bash
npm install
```

This will install:
- Express (web server)
- Socket.io (real-time communication)
- Chess.js (chess logic)
- CORS (cross-origin support)

---

## Step 3: Start the Server

```bash
npm start
```

You should see:
```
🏰 ChessyCom Server Started!
📡 Server running on http://localhost:3000
🎮 Open http://localhost:3000 in your browser
```

---

## Step 4: Play!

### On Same Computer (Testing)
1. Open http://localhost:3000 in Chrome
2. Open http://localhost:3000 in another browser (Firefox/Edge)
3. Create game in one, join in the other

### On Same Network (Real Multiplayer)
1. Find your IP address:
   ```bash
   ipconfig
   ```
   Look for "IPv4 Address" (e.g., 192.168.1.100)

2. On your computer:
   - Open http://localhost:3000
   - Click "Host Game"
   - Get room code (e.g., "ABC123")

3. On friend's computer (same WiFi):
   - Open http://YOUR_IP:3000 (e.g., http://192.168.1.100:3000)
   - Click "Join Game"
   - Enter room code
   - Play!

---

## 🎮 Features

### Current
- ✅ Create game rooms
- ✅ Join with room codes
- ✅ Real-time move synchronization
- ✅ Chat system
- ✅ Spectator mode
- ✅ Game over detection

### Coming Soon
- ⏳ AI integration
- ⏳ Puzzles
- ⏳ Tournaments
- ⏳ Analysis board

---

## 🔧 Troubleshooting

### "npm: command not found"
**Solution:** Install Node.js first

### "Port 3000 already in use"
**Solution:** Change port in server.js:
```javascript
const PORT = 3001; // Change to any available port
```

### "Cannot connect from other device"
**Solution:** 
1. Check firewall settings
2. Make sure both devices on same WiFi
3. Use correct IP address

### "Room not found"
**Solution:** 
1. Make sure server is running
2. Check room code is correct
3. Room might have expired (1 hour timeout)

---

## 📱 Mobile Support

Works on mobile browsers too!
1. Find your computer's IP
2. On phone, connect to same WiFi
3. Open http://YOUR_IP:3000 in mobile browser
4. Play chess on your phone!

---

## 🎯 Next Steps

### Option 1: Integrate with Current UI
Update `script.js` to use Socket.io:
```javascript
const socket = io('http://localhost:3000');

socket.on('move-made', (data) => {
  game.load(data.fen);
  updateBoard();
});
```

### Option 2: Create New Multiplayer Page
Create `multiplayer.html` with:
- Room creation UI
- Room code input
- Player list
- Chat box

### Option 3: Fix AI First
Before multiplayer, fix AI integration:
- Connect to Stockfish
- Implement difficulty levels
- Test AI moves

---

## 🌐 Sharing Your Game

### Local Network Only (Secure)
- Only people on your WiFi can join
- No internet required
- Fast and private

### Internet (Advanced)
To play over internet, you need:
1. Port forwarding on router
2. Dynamic DNS service
3. Or use ngrok: https://ngrok.com/

---

## 📊 Server Commands

```bash
# Start server
npm start

# Start with auto-reload (development)
npm run dev

# Stop server
Ctrl + C
```

---

## 🎉 You're Ready!

Your local chess server is running!

**Test it now:**
1. Open two browser windows
2. Create game in one
3. Join in the other
4. Make some moves
5. See them sync in real-time!

---

**Need help?** Check the full plan in `CHESSYCOM_PLAN.md`

**Ready to integrate?** Let's update `index.html` and `script.js` next!
