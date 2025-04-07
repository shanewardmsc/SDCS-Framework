# Use official InfluxDB image as base
FROM influxdb:latest

# Set environment variables
ENV INFLUXDB_DB=historian
ENV INFLUXDB_HTTP_AUTH_ENABLED=true
ENV INFLUXDB_ADMIN_USER=admin
ENV INFLUXDB_ADMIN_PASSWORD=admin123
ENV INFLUXDB_USER=historian_user
ENV INFLUXDB_USER_PASSWORD=historian_pass

# Expose necessary ports
EXPOSE 8086 8088 2003 4242 25826

# Create necessary volumes for persistent storage
VOLUME ["/var/lib/influxdb"]

# Start InfluxDB
CMD ["influxd"]

