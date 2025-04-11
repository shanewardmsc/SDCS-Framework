from fastapi import FastAPI
import paho.mqtt.client as mqtt
from opcua import Client
from influxdb import InfluxDBClient

app = FastAPI()

# MQTT Client
mqtt_client = mqtt.Client()
mqtt_client.connect("vtrans", 1883, 60)

# OPC UA Client
opcua_client = Client("opc.tcp://localhost:4840")
opcua_client.connect()

# InfluxDB Client
influx_client = InfluxDBClient("vhis", 8086, database="sensor_data")

@app.post("/translate/")
def translate(data: dict):
    protocol = data.get("protocol")
    message = data["message"]

    if protocol == "MQTT":
        mqtt_client.publish("iot/topic", message)
    elif protocol == "OPC UA":
        opcua_client.get_node("ns=2;i=3").set_value(message)
    elif protocol == "HISTORIAN":
        influx_client.write_points([{
            "measurement": "sensor_data",
            "fields": {"value": float(message)}
        }])
    return {"status": "Message Translated"}
