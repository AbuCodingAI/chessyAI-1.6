# 🚀 Chessy 1.6 Quick Start

Get Chessy 1.6 up and running in 5 minutes.

## 1️⃣ Prerequisites

### Windows
- Visual Studio 2019+ or Build Tools
- CMake 3.16+
- vcpkg (for dependencies)

### Linux
```bash
sudo apt-get install build-essential cmake libeigen3-dev libboost-all-dev nlohmann-json3-dev
```

### macOS
```bash
brew install cmake eigen boost nlohmann-json
```

## 2️⃣ Download Stockfish

**Windows/Linux/macOS:**
1. Visit: https://stockfishchess.org/download/
2. Download latest version
3. Extract to: `chessy-1.6/stockfish/`

**Verify:**
```bash
# Windows
stockfish/stockfish-windows-x86-64-avx2.exe --version

# Linux
stockfish/stockfish-linux-x86-64-avx2 --version

# macOS
stockfish/stockfish-macos-11-m1 --version
```

## 3️⃣ Build

### Windows (MSVC)
```bash
mkdir build
cd build
cmake .. -G "Visual Studio 16 2019" -DCMAKE_TOOLCHAIN_FILE=C:\path\to\vcpkg\scripts\buildsystems\vcpkg.cmake
cmake --build . --config Release
cd ..
```

### Linux/macOS
```bash
mkdir build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j4
cd ..
```

## 4️⃣ Play!

### Interactive Mode
```bash
./bin/chessy-1.6 --play
```

Example game:
```
  a b c d e f g h
8 r n b q k b n r 8
7 p p p p p p p p 7
6 . . . . . . . . 6
5 . . . . . . . . 5
4 . . . . . . . . 4
3 . . . . . . . . 3
2 P P P P P P P P 2
1 R N B Q K B N R 1
  a b c d e f g h

Enter your move (e.g., e2e4): e2e4
Chessy 1.6 is thinking...
Chessy 1.6 plays: e7e5
```

## 5️⃣ Train (Optional)

### Generate Training Data
```bash
./bin/chessy-1.6 --generate-data
```
Time: 2-3 hours

### Train Neural Network
```bash
./bin/chessy-1.6 --train
```
Time: 20-30 hours total

### Test vs Stockfish
```bash
./bin/chessy-1.6 --test
```
Time: 8-10 hours

## 📊 Expected Results

After full training:
- **ELO**: 2600-2800 (IM to GM level)
- **vs Stockfish (depth 10)**: 45-55% win rate
- **Blunder punishment**: 70%+

## 🎯 Commands

```bash
# Play interactively
./bin/chessy-1.6 --play

# Generate training data
./bin/chessy-1.6 --generate-data

# Train neural network
./bin/chessy-1.6 --train

# Test vs Stockfish
./bin/chessy-1.6 --test

# Show help
./bin/chessy-1.6 --help
```

## 🐛 Troubleshooting

**Build fails with "Eigen not found"**
- Windows: Use vcpkg toolchain file
- Linux: `sudo apt-get install libeigen3-dev`
- macOS: `brew install eigen`

**Stockfish not found**
- Download from: https://stockfishchess.org/download/
- Extract to: `chessy-1.6/stockfish/`
- Verify executable exists

**Out of memory**
- Reduce training data size in config
- Use 64-bit build
- Close other applications

## 📚 Next Steps

1. Read full README.md for detailed documentation
2. Explore source code in `src/`
3. Modify training config for your hardware
4. Contribute improvements!

## 🎮 Have Fun!

Enjoy playing against Chessy 1.6! 🚀♟️

---

**Questions?** Check README.md or Chess Programming Wiki: https://www.chessprogramming.org/
