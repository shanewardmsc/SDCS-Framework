FROM python:3.11-slim

# Install dependencies
RUN pip install requests smtplib

# Copy the alerting script
COPY alert_listener.py /app/alert_listener.py

# Set the working directory
WORKDIR /app

# Run the alert listener script
CMD ["python", "alert_listener.py"]
