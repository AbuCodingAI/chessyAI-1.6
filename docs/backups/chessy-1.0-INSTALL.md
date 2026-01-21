# 🚀 Quick Installation Guide

## Step 1: Install Python Packages

### Option A: All at once (RECOMMENDED)
```bash
pip install flask flask-cors tensorflow numpy python-chess
```

### Option B: One by one
```bash
pip install flask
pip install flask-cors
pip install tensorflow
pip install numpy
pip install python-chess
```

### Option C: From requirements file
```bash
pip install -r requirements.txt
```

---

## ⚠️ Common Mistakes

### ❌ WRONG:
```bash
pip install chess.engine  # This doesn't exist!
pip install chess         # This is the wrong package!
```

### ✅ CORRECT:
```bash
pip install python-chess  # This is the right package!
```

**Note**: `chess.engine` is a MODULE inside `python-chess`, not a separate package!

---

## 🔍 Verify Installation

After installing, test each package:

```bash
python -c "import flask; print('Flask:', flask.__version__)"
python -c "import flask_cors; print('Flask-CORS: OK')"
python -c "import tensorflow as tf; print('TensorFlow:', tf.__version__)"
python -c "import numpy as np; print('NumPy:', np.__version__)"
python -c "import chess; print('Python-Chess:', chess.__version__)"
```

All should print without errors!

---

## 🐛 Troubleshooting

### "WARNING: Ignoring invalid distribution ~ip"
This is just a warning, ignore it. Your packages will still install.

### "Could not find a version that satisfies the requirement"
Make sure you're using Python 3.8 or newer:
```bash
python --version
```

### "Defaulting to user installation"
This is normal on Windows. It means packages install to your user folder.

### TensorFlow installation fails
Try installing an older version:
```bash
pip install tensorflow==2.13.0
```

---

## ✅ After Installation

Run the server:
```bash
python chess_ai_server.py
```

You should see:
```
🚀 Starting Chessy 1.0 Neural Network Server...
📡 Server will run on http://localhost:5000
🧠 Loading neural network model...
📦 Creating new model...
✅ Server ready!
```

Then open `Chessy1-0.html` in your browser!

---

## 📦 What Each Package Does

- **flask** - Web server framework
- **flask-cors** - Allows browser to connect to server
- **tensorflow** - Neural network library (the AI brain!)
- **numpy** - Fast array math
- **python-chess** - Chess rules and board (includes chess.engine module)

---

## 🎯 Quick Start After Install

1. ✅ Packages installed
2. Run: `python chess_ai_server.py`
3. Open: `Chessy1-0.html`
4. Click: "Test Connection"
5. Play! 🎮

**That's it!** 🎉
