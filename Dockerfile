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
RUN if [ ! -f stockfish/stockfish ]; then \
    mkdir -p stockfish && \
    cd stockfish && \
    wget https://github.com/official-stockfish/Stockfish/releases/download/sf_16/stockfish-ubuntu-x86-64-avx2 -O stockfish && \
    chmod +x stockfish && \
    cd ..; \
fi

# Set working directory back to root
WORKDIR /app

# Expose port for keep-alive pings
EXPOSE 3000

# Run training
CMD ["python3", "chessy-1.6/train_cloud.py"]
