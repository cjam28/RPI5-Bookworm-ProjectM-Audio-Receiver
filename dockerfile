FROM python:3.11-slim-bookworm

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    pulseaudio \
    pulseaudio-utils \
    libasound2-dev \
    libpulse-dev \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Clone the repository
RUN git clone https://github.com/kholbrook1303/RPI5-Bookworm-ProjectM-Audio-Receiver.git /app
WORKDIR /app

# Create virtual environment and install dependencies
RUN python3 -m venv venv
RUN . venv/bin/activate && pip install -r requirements.txt

# Expose ports for web interface (if any)
EXPOSE 8080

# Set the command to run the application
CMD ["./venv/bin/python", "main.py"]
