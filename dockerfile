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

# Expose ports for web interface (if any)
EXPOSE 8080

# Set the command to run the application with the correct entry point
CMD ["./venv/bin/python", "projectMAR.py"]

# Build projectM wrapper
RUN echo "Building projectM wrapper..." && \
    cd /tmp && \
    echo '#include <projectM.hpp>' > projectm_wrapper.cpp && \
    echo '#include <cstring>' >> projectm_wrapper.cpp && \
    echo '' >> projectm_wrapper.cpp && \
    echo 'extern "C" {' >> projectm_wrapper.cpp && \
    echo '    static projectM* g_projectm = nullptr;' >> projectm_wrapper.cpp && \
    echo '    int projectm_init(int width, int height, int mesh_x, int mesh_y, int fps, int texture_size) {' >> projectm_wrapper.cpp && \
    echo '        try {' >> projectm_wrapper.cpp && \
    echo '            if (g_projectm) delete g_projectm;' >> projectm_wrapper.cpp && \
    echo '            g_projectm = new projectM();' >> projectm_wrapper.cpp && \
    echo '            g_projectm->projectM_init(width, height, mesh_x, mesh_y, fps, texture_size);' >> projectm_wrapper.cpp && \
    echo '            return 0;' >> projectm_wrapper.cpp && \
    echo '        } catch (...) { return -1; }' >> projectm_wrapper.cpp && \
    echo '    }' >> projectm_wrapper.cpp && \
    echo '    void projectm_render_frame() { if (g_projectm) g_projectm->renderFrame(); }' >> projectm_wrapper.cpp && \
    echo '    void projectm_reset() { if (g_projectm) g_projectm->projectM_reset(); }' >> projectm_wrapper.cpp && \
    echo '    void projectm_cleanup() { if (g_projectm) { delete g_projectm; g_projectm = nullptr; } }' >> projectm_wrapper.cpp && \
    echo '}' >> projectm_wrapper.cpp && \
    g++ -shared -fPIC -o /usr/local/lib/libprojectm_wrapper.so projectm_wrapper.cpp -lprojectM -std=c++11 && \
    echo "Wrapper built successfully"
