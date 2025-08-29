FROM python:3.11-slim-bookworm

# Install ALL dependencies including build tools
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

# Build projectM v4.x from source
WORKDIR /tmp
RUN echo "Building projectM v4.x from source..." && \
    git clone --depth 1 --branch v4.1.0 https://github.com/projectM-visualizer/projectM.git && \
    echo "Repository cloned successfully" && \
    cd projectM && \
    echo "Current directory: $(pwd)" && \
    echo "Directory contents: $(ls -la)" && \
    mkdir build && cd build && \
    echo "Build directory created: $(pwd)" && \
    cmake .. -DCMAKE_BUILD_TYPE=Release -DUSE_NATIVE_GL=ON && \
    echo "CMake configuration successful" && \
    make -j$(nproc) && \
    echo "Make successful" && \
    make install && \
    echo "Install successful" && \
    ldconfig && \
    echo "Ldconfig successful"

# Verify the build worked
RUN echo "Checking for projectM libraries:" && \
    find /usr -name "*libprojectM*" 2>/dev/null && \
    find /usr/local -name "*libprojectM*" 2>/dev/null && \
    echo "Library search complete"

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

# Final verification
RUN echo "Final verification:" && \
    ls -la /usr/local/lib/libprojectM* 2>/dev/null || echo "No projectM libraries in /usr/local/lib" && \
    ls -la /usr/lib/*/libprojectM* 2>/dev/null || echo "No projectM libraries in /usr/lib"

# Expose ports for web interface (if any)
EXPOSE 8080

# Set the command to run the application with the correct entry point
CMD ["./venv/bin/python", "projectMAR.py"]
