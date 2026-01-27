FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    python3 \
    python3-pip \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Download Stockfish if not present
RUN if [ ! -f stockfish/stockfish ]; then \
    mkdir -p stockfish && \
    wget -q https://github.com/official-stockfish/Stockfish/releases/download/sf_16/stockfish-ubuntu-x86-64-avx2 -O stockfish/stockfish && \
    chmod +x stockfish/stockfish; \
    fi

# Build the project
RUN chmod +x build.sh && ./build.sh

# Install Python dependencies
RUN pip install -r requirements.txt

# Run training
CMD ["python3", "train_cloud.py"]
