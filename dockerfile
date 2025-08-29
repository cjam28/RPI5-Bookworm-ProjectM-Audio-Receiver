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
    g++ \
    libprojectm-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Create virtual environment and install dependencies
RUN python3 -m venv venv
RUN . venv/bin/activate && pip install --upgrade pip
RUN . venv/bin/activate && pip install -r requirements.txt

# Copy the wrapper source file FIRST
COPY projectm_wrapper.cpp /tmp/

# Build projectM wrapper with better error handling
RUN echo "Building projectM wrapper..." && \
    cd /tmp && \
    echo "Current directory: $(pwd)" && \
    echo "Files in /tmp: $(ls -la)" && \
    echo "Checking projectM library..." && \
    pkg-config --libs projectM || echo "pkg-config failed, trying direct linking" && \
    echo "Compiling wrapper..." && \
    g++ -v -shared -fPIC -o /usr/local/lib/libprojectm_wrapper.so projectm_wrapper.cpp -lprojectM -std=c++11 2>&1 || \
    (echo "First attempt failed, trying with different flags..." && \
     g++ -v -shared -fPIC -o /usr/local/lib/libprojectm_wrapper.so projectm_wrapper.cpp -lprojectM -std=c++11 -I/usr/include/projectM 2>&1) || \
    (echo "Second attempt failed, trying without std flag..." && \
     g++ -v -shared -fPIC -o /usr/local/lib/libprojectm_wrapper.so projectm_wrapper.cpp -lprojectM 2>&1) || \
    (echo "All compilation attempts failed. Checking what's available:" && \
     echo "projectM headers:" && find /usr -name "projectM.hpp" 2>/dev/null && \
     echo "projectM libraries:" && find /usr -name "*projectM*" 2>/dev/null && \
     echo "pkg-config output:" && pkg-config --cflags --libs projectM 2>&1 || echo "pkg-config not available" && \
     exit 1)

# Copy the rest of the application code
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
