FROM python:3.11-slim

WORKDIR /app
COPY mqtt_to_influx.py .

RUN pip install paho-mqtt influxdb-client

CMD ["python", "mqtt_to_influx.py"]
