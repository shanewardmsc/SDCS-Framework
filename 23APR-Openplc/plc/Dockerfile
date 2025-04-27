FROM zakharbz/labshock-plc:v1.1.1

# Environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install Python and virtualenv
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-venv python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Create virtual environment and upgrade pip inside it
RUN python3 -m venv $VIRTUAL_ENV && \
    $VIRTUAL_ENV/bin/pip install --upgrade pip

# Copy app data files
COPY ./appdata/st_files /workdir/webserver/st_files
COPY ./appdata/openplc.db /workdir/webserver/openplc.db
COPY ./appdata/active_program /workdir/webserver/active_program
COPY ./appdata/plc_tags.csv /app/data/plc_tags.csv

# Copy Python script and requirements
COPY modbus_mqtt.py /app/modbus_mqtt.py
COPY requirements.txt /app/requirements.txt

# Install Python dependencies in the virtual environment
RUN $VIRTUAL_ENV/bin/pip install --no-cache-dir -r /app/requirements.txt

# Copy entrypoint and make it executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set entrypoint and default command
ENTRYPOINT ["/entrypoint.sh"]
CMD ["./start_openplc.sh"]

