FROM ubuntu:18.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Update system and install required dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    software-properties-common \
    sudo \
    lsb-release \
    && rm -rf /var/lib/apt/lists/*

# Add NVIDIA package repositories and install CUDA drivers
RUN wget https://developer.download.nvidia.com/embedded/L4T/r32_Release_v4.3/T210/jetson-ota-public.asc -O /etc/apt/trusted.gpg.d/jetson-ota-public.asc && \
    add-apt-repository "deb https://repo.download.nvidia.com/jetson/common r32.4 main" && \
    add-apt-repository "deb https://repo.download.nvidia.com/jetson/t210 r32.4 main" && \
    apt-get update && \
    apt-get install -y --no-install-recommends nvidia-l4t-core && \
    rm -rf /var/lib/apt/lists/*

# Install CODESYS dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libxrandr2 \
    libxcursor1 \
    libglib2.0-0 \
    libfreetype6 \
    libfontconfig1 \
    && rm -rf /var/lib/apt/lists/*

# Download and install CODESYS runtime (modify URL based on your version)
RUN wget -O /tmp/codesys-runtime.deb "https://store.codesys.com/media/n98_media_assets/files/4f/22/Runtime_ARM.deb" && \
    dpkg -i /tmp/codesys-runtime.deb && \
    rm /tmp/codesys-runtime.deb

# Configure NVIDIA runtime for Docker
RUN apt-get update && apt-get install -y --no-install-recommends \
    nvidia-container-runtime \
    && rm -rf /var/lib/apt/lists/*

# Expose CODESYS Web Server Port
EXPOSE 8080

# Set up entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
