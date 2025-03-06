# Use official InfluxDB image as base
FROM influxdb:2.0

# Set environment variables for InfluxDB setup
ENV INFLUXDB_DB=vplc_historian
ENV INFLUXDB_USER=admin
ENV INFLUXDB_PASSWORD=admin123
ENV INFLUXDB_ADMIN_USER=admin
ENV INFLUXDB_ADMIN_PASSWORD=admin123

# Expose the ports used by InfluxDB (HTTP API & UI)
EXPOSE 8086

# Initialize InfluxDB with a script if needed
COPY ./init-influxdb.sh /docker-entrypoint-initdb.d/

# Set entrypoint to start InfluxDB
ENTRYPOINT ["influxd"]

# Command to start the database
CMD ["--reporting-disabled"]
