FROM python:3.11-slim-bookworm

# Install only runtime dependencies (no build tools)
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

# Create entrypoint script
RUN echo '#!/bin/bash\n\
# Create symlink for projectM library compatibility\n\
mkdir -p /usr/local/lib\n\
ln -sf /usr/lib/aarch64-linux-gnu/libprojectM.so /usr/local/lib/libprojectM-4.so\n\
echo "Created symlink: /usr/local/lib/libprojectM-4.so -> /usr/lib/aarch64-linux-gnu/libprojectM.so"\n\
ls -la /usr/local/lib/libprojectM*\n\
# Start the application\n\
exec ./venv/bin/python projectMAR.py' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# Expose ports for web interface (if any)
EXPOSE 8080

# Set the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
