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
RUN chmod +x build.sh && ./build.sh

# Download Stockfish if not present
RUN mkdir -p /app/chessy-1.6/stockfish && \
    cd /app/chessy-1.6/stockfish && \
    wget --timeout=30 https://github.com/official-stockfish/Stockfish/releases/download/sf_16/stockfish-ubuntu-x86-64-avx2 -O stockfish 2>&1 || echo "Stockfish download failed, will use fallback" && \
    chmod +x stockfish 2>/dev/null || true

# Set working directory back to root
WORKDIR /app

# Expose port for keep-alive pings
EXPOSE 3000

# Run training
CMD ["python3", "chessy-1.6/train_cloud.py"]
