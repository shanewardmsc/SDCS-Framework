# Use an appropriate base image
FROM ubuntu:24.04

# Set the working directory
WORKDIR /home/openplc

# Update and install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    sudo \
    cmake \
    build-essential \
    autoconf \
    automake \
    bison \
    flex \
    libtool \
    pkg-config \
    python3 \
    python3-pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Add a non-root user
RUN useradd --create-home --shell /bin/bash openplc
USER openplc

# Clone the OpenPLC repository and build
RUN git clone https://github.com/thiagoralves/OpenPLC_v3.git
WORKDIR /home/openplc/OpenPLC_v3
RUN ./install.sh custom

# Copy your custom run.sh script into the container
COPY --chown=openplc:openplc run.sh /home/openplc/run.sh
RUN chmod +x /home/openplc/run.sh

# Copy the program files
COPY --chown=openplc:openplc openplc/program /home/openplc/OpenPLC_v3/webserver/st_files/

# Set entrypoint
CMD ["/home/openplc/run.sh"]

