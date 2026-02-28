#!/bin/bash

# Chessy 1.6 Build Script for Linux/macOS

echo ""
echo "========================================"
echo "Chessy 1.6 - C++ Neural Chess Engine"
echo "========================================"
echo ""

# Check if build directory exists
if [ ! -d "build" ]; then
    echo "Creating build directory..."
    mkdir build
fi

cd build

# Configure with CMake
echo "Configuring CMake..."
cmake .. -DCMAKE_BUILD_TYPE=Release

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: CMake configuration failed!"
    echo ""
    exit 1
fi

# Build
echo ""
echo "Building Chessy 1.6..."
make -j4

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Build failed!"
    echo ""
    exit 1
fi

cd ..

echo ""
echo "========================================"
echo "Build successful!"
echo "========================================"
echo ""
echo "Executable: bin/chessy-1.6"
echo ""
echo "Next steps:"
echo "  1. Download Stockfish from https://stockfishchess.org/download/"
echo "  2. Extract to: stockfish/"
echo "  3. Run: ./bin/chessy-1.6 --play"
echo ""
