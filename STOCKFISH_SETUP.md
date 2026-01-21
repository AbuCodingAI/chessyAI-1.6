# 🐟 Stockfish Setup Guide

## What is Stockfish?

Stockfish is a powerful chess engine that Chocker uses to:
- Evaluate positions
- Find the best moves (GM mode)
- Find the worst moves (throw mode)
- Power the ULTIMATE DISRESPECT

---

## 📥 How to Install Stockfish

### Step 1: Download Stockfish

1. Go to: https://stockfishchess.org/download/
2. Download **Stockfish 16 for Windows**
3. Choose the version that matches your CPU:
   - **Modern CPU (2011+):** `stockfish-windows-x86-64-avx2.exe`
   - **Older CPU:** `stockfish-windows-x86-64-modern.exe`
   - **Very old CPU:** `stockfish-windows-x86-64.exe`

### Step 2: Extract Stockfish

1. Extract the downloaded ZIP file
2. You'll get a file like: `stockfish-windows-x86-64-avx2.exe`

### Step 3: Place Stockfish in Your Project

**Option A: Create stockfish folder (Recommended)**
```
Chessy/
├── stockfish/
│   └── stockfish-windows-x86-64-avx2.exe  ← Put it here!
├── neural-ai/
├── batch files/
└── ...
```

**Option B: Put in neural-ai folder**
```
Chessy/
├── neural-ai/
│   ├── chocker.py
│   └── stockfish-windows-x86-64-avx2.exe  ← Or here!
└── ...
```

### Step 4: Update Path (if needed)

If you put Stockfish somewhere else, update line 28 in `chocker.py`:

```python
# Change this line:
def __init__(self, stockfish_path="stockfish/stockfish-windows-x86-64-avx2.exe"):

# To your path:
def __init__(self, stockfish_path="neural-ai/stockfish-windows-x86-64-avx2.exe"):
```

---

## ✅ Quick Setup (Copy-Paste)

### PowerShell Commands:

```powershell
# Create stockfish folder
New-Item -ItemType Directory -Path "stockfish" -Force

# Download Stockfish (you'll need to do this manually from the website)
# Then move it:
Move-Item "Downloads\stockfish-windows-x86-64-avx2.exe" "stockfish\" -Force
```

---

## 🧪 Test Stockfish

After installing, test if it works:

```bash
cd neural-ai
python chocker.py
```

You should see:
```
CHOCKER - THE ABSOLUTE MADMAN
ULTIMATE DISRESPECT MODE
...
```

If you see an error about Stockfish not found, check:
1. ✅ File exists in the right location
2. ✅ File name matches exactly
3. ✅ Path in chocker.py is correct

---

## 🎯 Alternative: Use Different Path

If you already have Stockfish installed elsewhere:

```python
# In chocker.py, line 28, change to your path:
stockfish_path = "C:/path/to/your/stockfish.exe"
```

---

## 📊 Recommended Versions

| CPU Type | Stockfish Version | Speed |
|----------|------------------|-------|
| Modern (2011+) | avx2 | Fastest |
| Older (2008+) | modern | Fast |
| Very Old | basic | Slower |

**Recommendation:** Try `avx2` first. If it doesn't work, try `modern`.

---

## 🚨 Common Issues

### Issue 1: "File not found"
**Solution:** Check the path and file name match exactly

### Issue 2: "Access denied"
**Solution:** Right-click → Properties → Unblock

### Issue 3: "Not a valid Win32 application"
**Solution:** Download the correct version for your CPU

---

## 🎮 After Setup

Once Stockfish is installed, you can play Chocker:

```bash
# Method 1: Batch file
"batch files\PLAY_CHESSY_COMEDIAN.bat"

# Method 2: Direct
cd neural-ai
python chocker.py
```

---

## 📁 Final Structure

Your project should look like:

```
Chessy/
├── stockfish/
│   └── stockfish-windows-x86-64-avx2.exe  ✅
├── neural-ai/
│   ├── chocker.py  ✅
│   └── ...
├── batch files/
│   └── PLAY_CHESSY_COMEDIAN.bat  ✅
└── ...
```

---

## 🎉 Ready to Play!

Once Stockfish is installed, Chocker will:
- ✅ Play ULTIMATE DISRESPECT opening (f3, Kf2)
- ✅ Force en passant (holy hell!)
- ✅ Throw advantages when winning
- ✅ Activate RAGE MODE if you don't en passant
- ✅ Promote to bishop/knight (or queen for stalemate)

---

**Need help?** Check if:
1. Stockfish file exists
2. Path is correct in chocker.py
3. File is executable (not blocked)

**ULTIMATE DISRESPECT:** Even our setup guide is organized! 🤡👑
