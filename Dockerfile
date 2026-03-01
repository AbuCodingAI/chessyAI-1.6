# Chessy 1.6 Cloud Training - Render Deployment
FROM ubuntu:22.04

# Set working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    python3 \
    python3-pip \
    curl \
    wget \
    libeigen3-dev \
    libboost-all-dev \
    nlohmann-json3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r chessy-1.6/requirements.txt

# Clean build directory to force rebuild
RUN rm -rf chessy-1.6/build

# Build the C++ project
WORKDIR /app/chessy-1.6
RUN mkdir -p build && cd build && \
    echo "=== CMake Configuration ===" && \
    cmake .. -DCMAKE_BUILD_TYPE=Release 2>&1 | tail -20 && \
    echo "=== Building ===" && \
    make -j4 2>&1 | tail -30 && \
    echo "=== Verifying Binary ===" && \
    find . -name "chessy-1.6" -type f && \
    cp bin/chessy-1.6 ../bin/chessy-1.6 2>/dev/null || cp CMakeFiles/chessy-1.6.dir/../bin/chessy-1.6 ../bin/chessy-1.6 2>/dev/null || true && \
    ls -lh ../bin/ && \
    test -f ../bin/chessy-1.6 && echo "✓ Binary ready!" || (echo "✗ Binary not found, checking build output..." && find . -name "chessy-1.6" && exit 1)

# Install Stockfish from apt repository
RUN apt-get update && apt-get install -y stockfish && rm -rf /var/lib/apt/lists/*

# Set working directory back to root
WORKDIR /app

# Expose port for keep-alive pings
EXPOSE 3000

# Run training
CMD ["python3", "chessy-1.6/train_cloud.py"]
