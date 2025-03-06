FROM ubuntu:22.04

# Install dependencies
RUN apt update && apt install -y wget curl sudo 

# Add CODESYS runtime (Replace with your actual installation method)
COPY CODESYS_Runtime.tar.gz /tmp/
RUN tar -xzf /tmp/CODESYS_Runtime.tar.gz -C /opt/codesys && \
    rm /tmp/CODESYS_Runtime.tar.gz

# Install MQTT client (if needed)
RUN apt install -y mosquitto-clients

# Copy the vPLC application
COPY vPLC_Project.project /opt/codesys/

# Set environment variables
ENV CODESYS_HOME="/opt/codesys"

# Expose necessary ports (e.g., for web and OPC UA)
EXPOSE 8080 4840 1883

# Start CODESYS runtime
CMD ["/opt/codesys/start-runtime.sh"]
