# Stage 1: Build projectM
FROM debian:bookworm-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    git \
    cmake \
    build-essential \
    pkg-config \
    libglm-dev \
    libgl1-mesa-dev \
    libegl1-mesa-dev \
    libfreetype6-dev \
    libfontconfig1-dev \
    libglfw3-dev \
    libglew-dev \
    libassimp-dev \
    libboost-all-dev \
    && rm -rf /var/lib/apt/lists/*

# Build projectM
WORKDIR /tmp
RUN git clone --depth 1 https://github.com/projectM-visualizer/projectM.git && \
    cd projectM && \
    mkdir build && cd build && \
    cmake .. -DCMAKE_BUILD_TYPE=Release -DUSE_NATIVE_GL=ON && \
    make -j$(nproc) && \
    make install

# Stage 2: Runtime container
FROM python:3.11-slim-bookworm

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    pulseaudio \
    pulseaudio-utils \
    libasound2-dev \
    libpulse-dev \
    python3-pip \
    python3-venv \
    libgl1-mesa-glx \
    libglu1-mesa \
    libsdl2-2.0-0 \
    libsdl2-dev \
    libx11-6 \
    libxext6 \
    libxrandr2 \
    libxrender1 \
    libxss1 \
    libxtst6 \
    && rm -rf /var/lib/apt/lists/*

# Copy projectM libraries from builder stage
COPY --from=builder /usr/local/lib/libprojectM* /usr/local/lib/
COPY --from=builder /usr/local/include/projectM /usr/local/include/
RUN ldconfig

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Create virtual environment and install dependencies
RUN python3 -m venv venv
RUN . venv/bin/activate && pip install --upgrade pip
RUN . venv/bin/activate && pip install -r requirements.txt

# Copy the application code
COPY . .

# Make projectMAR.py executable
RUN chmod +x projectMAR.py

# Ensure configuration directory exists and copy config file
RUN mkdir -p /app/conf && chmod 755 /app/conf
COPY conf/projectMAR.conf /app/conf/projectMAR.conf

# Create a symlink to ensure the lib directory can find the conf directory
RUN ln -sf /app/conf /app/lib/conf

# Expose ports for web interface (if any)
EXPOSE 8080

# Set the command to run the application with the correct entry point
CMD ["./venv/bin/python", "projectMAR.py"]
