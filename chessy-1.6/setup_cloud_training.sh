#!/bin/bash
# Chessy 1.6 Cloud Training Setup Script

echo "================================"
echo "Chessy 1.6 Cloud Training Setup"
echo "================================"
echo ""

# Check if build directory exists
if [ ! -d "bin" ]; then
    echo "❌ Build directory not found. Building project..."
    if [ -f "build.sh" ]; then
        ./build.sh
    else
        echo "❌ build.sh not found"
        exit 1
    fi
fi

# Check if binary exists
if [ ! -f "bin/chessy-1.6" ]; then
    echo "❌ Binary not found. Please build first."
    exit 1
fi

echo "✓ Binary found: bin/chessy-1.6"

# Create directories
mkdir -p checkpoints
mkdir -p models
mkdir -p logs

echo "✓ Directories created"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3."
    exit 1
fi

echo "✓ Python 3 found"

# Check Stockfish
if [ -f "stockfish/stockfish" ] || [ -f "stockfish/stockfish.exe" ]; then
    echo "✓ Stockfish found"
else
    echo "⚠ Stockfish not found. Training will use fallback evaluation."
    echo "  Download from: https://stockfishchess.org/download/"
fi

echo ""
echo "================================"
echo "Setup Complete!"
echo "================================"
echo ""
echo "To start training:"
echo "  python3 train_cloud.py"
echo ""
echo "To monitor training:"
echo "  tail -f training.log"
echo ""
echo "To deploy to Render:"
echo "  1. Push to GitHub"
echo "  2. Go to render.com"
echo "  3. Create new Background Worker"
echo "  4. Select this repository"
echo "  5. Set start command: python3 train_cloud.py"
echo ""
