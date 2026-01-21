# 🧠 Chessy 1.0 - Neural Network AI

## 🚀 Quick Start (2 Options)

### Option 1: Double-Click (Easiest!)
1. Double-click `start_server.bat`
2. Wait for browser to open automatically
3. Play!

### Option 2: Manual
1. Open Command Prompt here
2. Run: `python chess_ai_server.py`
3. Open `Chessy1-0.html` in browser

---

## ⚡ What Happens When You Open Chessy1-0.html

The page will automatically:
1. ✅ Check if Python server is running
2. ✅ Connect if server is found
3. ⚠️ Show setup instructions if server is not running
4. 🔄 Provide "Retry Connection" button

**No manual connection needed!**

---

## 📦 First Time Setup

Install Python packages:
```bash
pip install flask flask-cors tensorflow numpy python-chess
```

Or use:
```bash
pip install -r ../requirements.txt
```

---

## 🎮 How to Use

1. **Start Server**: Run `start_server.bat` or `python chess_ai_server.py`
2. **Open Game**: Open `Chessy1-0.html` (auto-connects!)
3. **Play**: Make moves, AI responds automatically
4. **Adjust Settings**: Change model, depth, temperature
5. **Train**: Click "Retrain Model" to improve AI

---

## 🧠 Features

- **Auto-Connection**: Detects server automatically
- **3 AI Models**: Basic CNN, Deep CNN, ResNet
- **Adjustable Depth**: 1-10 moves ahead
- **Temperature Control**: 0.0-1.0 creativity
- **Live Analysis**: Real-time position evaluation
- **Training**: One-click model retraining

---

## 🐛 Troubleshooting

### "Server Not Running" Alert
- Run `start_server.bat` or `python chess_ai_server.py`
- Click "Retry Connection" after server starts

### "Module not found"
```bash
pip install flask flask-cors tensorflow numpy python-chess
```

### Server won't start
- Check if Python 3.8+ is installed: `python --version`
- Check if port 5000 is available

---

## 📁 Files

- `Chessy1-0.html` - Game interface (auto-connects!)
- `Chessy1-0.css` - Styling
- `Chessy1-0.js` - Game logic
- `chess_ai_server.py` - Python server
- `start_server.bat` - Quick start script
- `test_installation.py` - Test packages

---

## 🎯 Quick Commands

```bash
# Start server
python chess_ai_server.py

# Test installation
python test_installation.py

# Install packages
pip install -r ../requirements.txt
```

---

**Just double-click `start_server.bat` to begin!** 🎮
