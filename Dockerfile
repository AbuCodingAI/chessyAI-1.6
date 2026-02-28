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

# Build the C++ project (or use pre-built binary if available)
WORKDIR /app/chessy-1.6
RUN if [ -f bin/chessy-1.6 ]; then \
    echo "Using pre-built binary"; \
else \
    echo "=== Running CMake ===" && \
    mkdir -p build && cd build && \
    cmake .. -DCMAKE_BUILD_TYPE=Release 2>&1 && \
    echo "=== Running Make ===" && \
    make -j4 2>&1 && \
    echo "=== Checking for binary ===" && \
    test -f bin/chessy-1.6 && echo "Binary created successfully!" || (echo "ERROR: Binary not created!" && exit 1); \
fi

# Install Stockfish from apt repository
RUN apt-get update && apt-get install -y stockfish && rm -rf /var/lib/apt/lists/*

# Set working directory back to root
WORKDIR /app

# Expose port for keep-alive pings
EXPOSE 3000

# Run training
CMD ["python3", "chessy-1.6/train_cloud.py"]
