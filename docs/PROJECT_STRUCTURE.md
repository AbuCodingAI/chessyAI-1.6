# 📁 Chessy Project Structure

## 🎯 Root Directory (Main Game)

### Core Game Files
- **index.html** - Main chess game interface
- **style.css** - Game styling
- **script.js** - Game logic with AI engine
- **README.md** - Project overview
- **requirements.txt** - Python dependencies

---

## 📂 Folders

### `/neural-ai/` - Neural Network Chess AI
Complete neural network implementation with Python backend

**Files:**
- `Chessy1-0.html` - Neural AI interface
- `Chessy1-0.css` - Neural AI styling
- `Chessy1-0.js` - Neural AI frontend logic
- `chess_ai_server.py` - Python Flask server
- `test_installation.py` - Installation test script
- `start_server.bat` - Quick start script
- `NEURAL_AI_SETUP.md` - Setup guide
- `NEURAL_AI_SUMMARY.md` - Overview
- `INSTALL.md` - Installation instructions

**How to use:**
```bash
cd neural-ai
pip install -r ../requirements.txt
python chess_ai_server.py
# Then open Chessy1-0.html in browser
```

---

### `/docs/` - Documentation
All documentation and guides

**Files:**
- `AI_ENGINE.md` - Chess engine documentation
- `TRASH_TALKER.md` - Trash Talker AI guide
- `SPECIAL_AI_MODES.md` - Randy & AntiGuess docs
- `ALL_AI_OPPONENTS.md` - Complete AI roster
- `ADVANCED_AI_FEATURES.md` - Transposition tables & quiescence
- `chesscom.log` - Chess.com feature research

---

### `/ToBeDeleted/` - Old Files
Files that can be safely deleted

**Contents:**
- Old documentation versions
- Duplicate files
- Outdated implementations

**To delete this folder:**
```bash
# Windows
rmdir /s ToBeDeleted

# Mac/Linux
rm -rf ToBeDeleted
```

---

### `/assets/` - Assets (Future)
For images, sounds, etc. (currently empty)

---

## 🎮 Quick Start

### Play the Main Game
1. Open `index.html` in your browser
2. Select AI difficulty
3. Play!

### Play Neural Network AI
1. `cd neural-ai`
2. `pip install -r ../requirements.txt`
3. `python chess_ai_server.py`
4. Open `Chessy1-0.html`

---

## 📊 Project Stats

### Main Game Features
- ✅ 14 AI opponents (100-3800 Elo)
- ✅ Complete chess rules
- ✅ Minimax + Alpha-Beta pruning
- ✅ Transposition tables
- ✅ Quiescence search
- ✅ 8 time controls
- ✅ Achievements system
- ✅ Dark mode
- ✅ 5 board themes

### Neural Network Features
- ✅ 3 neural network models
- ✅ Python Flask backend
- ✅ TensorFlow integration
- ✅ Real-time training
- ✅ Live analysis
- ✅ Adjustable depth & temperature

---

## 🗂️ File Organization

```
Chessy/
├── index.html              # Main game
├── style.css               # Main styling
├── script.js               # Main game logic
├── README.md               # Project overview
├── requirements.txt        # Python packages
├── PROJECT_STRUCTURE.md    # This file
│
├── neural-ai/              # Neural network AI
│   ├── Chessy1-0.html
│   ├── Chessy1-0.css
│   ├── Chessy1-0.js
│   ├── chess_ai_server.py
│   ├── test_installation.py
│   ├── start_server.bat
│   ├── NEURAL_AI_SETUP.md
│   ├── NEURAL_AI_SUMMARY.md
│   └── INSTALL.md
│
├── docs/                   # Documentation
│   ├── AI_ENGINE.md
│   ├── TRASH_TALKER.md
│   ├── SPECIAL_AI_MODES.md
│   ├── ALL_AI_OPPONENTS.md
│   ├── ADVANCED_AI_FEATURES.md
│   └── chesscom.log
│
├── ToBeDeleted/            # Old files (can delete)
│   ├── CHESS_RULES_IMPLEMENTED.md
│   ├── NEW_FEATURES.md
│   ├── IMPLEMENTATION_SUMMARY.md
│   └── ... (other old files)
│
└── assets/                 # Future assets
    └── (empty for now)
```

---

## 🧹 Cleanup Instructions

### Safe to Delete
The entire `/ToBeDeleted/` folder can be removed:
```bash
rmdir /s /q ToBeDeleted
```

### Keep Everything Else!
All other files and folders are part of the active project.

---

## 📝 Notes

- **Main game** works standalone (no Python needed)
- **Neural AI** requires Python + TensorFlow
- Both versions are fully functional
- Documentation is organized in `/docs/`
- Old files are in `/ToBeDeleted/`

---

## 🎯 What to Use

### For Quick Play
→ Open `index.html` (no setup needed!)

### For Neural Network Experiments
→ Use `/neural-ai/` (requires Python setup)

### For Documentation
→ Check `/docs/` folder

---

**Your workspace is now organized!** 🎉
