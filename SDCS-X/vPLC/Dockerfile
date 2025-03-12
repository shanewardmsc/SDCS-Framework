# Base image for NVIDIA Jetson Nano (Ubuntu 18.04, ARM64)
# Use ARM64 base image for the NVIDIA Jetson Nano
FROM arm64v8/ubuntu:18.04


# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /opt/codesys

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    sudo \
    libx11-xcb1 \
    libxrender1 \
    libxkbcommon-x11-0 \
    libglu1-mesa \
    mosquitto-clients \
    && rm -rf /var/lib/apt/lists/*

# Copy manually downloaded CODESYS ARM SL package
COPY ./codesyscontrol_linuxarm64_4.14.0.0_arm64.deb /opt/codesys/codesys_arm.deb

# Install CODESYS
RUN dpkg -i /opt/codesys/codesys_arm.deb && rm /opt/codesys/codesys_arm.deb

# Expose necessary ports
EXPOSE 8080 1217 11740 1883 8883

# Start CODESYS runtime
CMD ["/etc/init.d/codesyscontrol", "start"]
