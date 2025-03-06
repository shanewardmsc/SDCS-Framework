# Use the official Ubuntu image as a base
FROM ubuntu:20.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install necessary dependencies
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    cmake \
    git \
    wget \
    curl \
    unzip \
    libgtk-3-dev \
    pkg-config \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    python3-dev \
    python3-numpy \
    libusb-1.0-0-dev \
    libopencv-dev \
    libgtk-3-dev \
    libglfw3-dev \
    libssl-dev \
    libprotobuf-dev \
    protobuf-compiler \
    libgoogle-glog-dev \
    libgflags-dev \
    libeigen3-dev \
    libopencv-core-dev \
    libopencv-highgui-dev \
    libopencv-imgproc-dev \
    libopencv-video-dev \
    libopencv-objdetect-dev \
    && apt-get clean

# Install Intel RealSense SDK
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-key 9B0D5D97AC2C732D && \
    echo "deb [arch=amd64] https://librealsense.intel.com/Debian/apt stable main" | tee /etc/apt/sources.list.d/librealsense.list && \
    apt-get update && \
    apt-get install -y \
    librealsense2-utils \
    librealsense2-dev \
    librealsense2-dkms \
    && apt-get clean

# Install OpenCV (optional if not pre-installed)
RUN git clone https://github.com/opencv/opencv.git /opencv && \
    cd /opencv && \
    git checkout 4.x && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make -j$(nproc) && \
    make install

# Set the working directory
WORKDIR /app

# Copy your OpenCV application code into the container
COPY . /app

# Set entrypoint to run your OpenCV script
ENTRYPOINT ["python3", "realsense_opencv.py"]
