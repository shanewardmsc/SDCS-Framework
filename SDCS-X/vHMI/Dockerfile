FROM grafana/grafana:latest

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary tools
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    jq \
    && rm -rf /var/lib/apt/lists/*

# Expose Grafana default port
EXPOSE 3000

# Copy custom configuration files if needed
# COPY grafana.ini /etc/grafana/grafana.ini

# Set up a provisioning mechanism (e.g., dashboards, data sources)
COPY provisioning /etc/grafana/provisioning

# Add an entrypoint script to configure data sources for vPLC
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Switch back to Grafana user
USER grafana

ENTRYPOINT ["/entrypoint.sh"]
