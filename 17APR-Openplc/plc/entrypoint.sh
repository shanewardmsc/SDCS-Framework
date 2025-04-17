#!/bin/sh

# Add default route via the router
ip route add 192.168.3.0/24 via 192.168.2.254

# Run the main application process
exec "$@"
