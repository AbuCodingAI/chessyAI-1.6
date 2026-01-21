# Quick Start - Chessy 1.4

## Fastest Way to Play

### Option 1: Server Already Running
If you see "Server running on http://localhost:3000" in a terminal:
1. Open your browser
2. Go to: **http://localhost:3000**
3. Start playing!

### Option 2: Start Fresh
1. Double-click **START_CHESSY_1.4.bat**
2. Wait for browser to open automatically
3. Start playing!

### Option 3: Manual Start
```bash
npm install
node server.js
```
Then open: http://localhost:3000

---

## What You Can Do

### Play Against AI
- Choose from 15 different AI personalities
- ELO range: 100 (Noob) to 2700+ (Chessy 1.4)
- Special AIs: Chocker, Random Guy, Trash Talker

### Multiplayer
- Create a room
- Share the room code with friends
- Play together on local network

### Test Chessy 1.4
```bash
cd neural-ai
python test_quiescence.py
```

---

## Troubleshooting

### "Cannot GET /"
- Server is not running
- Run: `node server.js`

### "Module not found"
- Dependencies not installed
- Run: `npm install`

### Batch file doesn't work
- Just open: http://localhost:3000 in your browser
- Or run: `node server.js` in terminal

---

## Files

### Main Files
- `START_CHESSY_1.4.bat` - Start everything
- `server.js` - Main server
- `index.html` - Game interface

### Chessy 1.4 Files
- `neural-ai/chess_engine_quiescence.py` - GM-level engine
- `neural-ai/chessy_1.4.py` - Command line interface
- `neural-ai/test_quiescence.py` - Test suite

### Documentation
- `CHESSY_1.4_READY.md` - Complete guide
- `QUICK_START.md` - This file

---

## That's It!

Just open **http://localhost:3000** and start playing! 🚀♔
