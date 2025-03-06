# Start with an official Ubuntu image
FROM ubuntu:20.04

# Set environment variables to avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update and install necessary packages
RUN apt-get update && \
    apt-get install -y \
    wget \
    curl \
    unzip \
    build-essential \
    libglfw3-dev \
    libopencv-dev \
    libssl-dev \
    libprotobuf-dev \
    protobuf-compiler \
    libboost-all-dev \
    libcurl4-openssl-dev \
    python3-dev \
    python3-pip \
    && apt-get clean

# Install dependencies for MQTT (for communication with vPLC)
RUN pip3 install paho-mqtt

# Download and install CoppeliaSim (V-REP)
RUN mkdir -p /opt/coppeliaSim && \
    cd /opt/coppeliaSim && \
    wget https://www.coppeliarobotics.com/files/CoppeliaSim_Edu_V4_3_0_Ubuntu_20_04.tar.xz && \
    tar -xf CoppeliaSim_Edu_V4_3_0_Ubuntu_20_04.tar.xz && \
    rm CoppeliaSim_Edu_V4_3_0_Ubuntu_20_04.tar.xz

# Set up the CoppeliaSim environment
ENV COPPELIASIM_ROOT=/opt/coppeliaSim/CoppeliaSim_Edu_V4_3_0_Ubuntu_20_04
ENV PATH="${COPPELIASIM_ROOT}:${PATH}"

# Install additional Python libraries if required
RUN pip3 install numpy opencv-python

# Set working directory
WORKDIR /app

# Copy your custom simulation code, scripts, and configuration to the container
COPY . /app

# Expose ports if required for communication (e.g., MQTT)
EXPOSE 1883

# Run the simulation (launch script or custom configuration)
ENTRYPOINT ["bash", "-c", "$COPPELIASIM_ROOT/coppeliaSim.sh"]

# Command to start the simulation and interact with the vPLC
CMD ["--no-rendering", "--headless"]
