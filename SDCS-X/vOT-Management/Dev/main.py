# -------------------------------------------------------------------------------------------------- #
# Project:      OT Docker Container Management Service                                               #
# Description:  Added MQTT broker communication                                                      #
# Author:       R00110936                                                                            #
# -------------------------------------------------------------------------------------------------- #

# Library Package Import Definitions
import os
import sys
import time
import uvicorn
import paho.mqtt.client as mqtt
from docker_utils import DockerInterface, DockerController
from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from collections import deque
from influxdb_client import InfluxDBClient, Point, WritePrecision

# Initialize FastAPI and templates
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Initialize Docker Controller
docker = DockerInterface()
client = docker.docker_connect()
docker_ctrl = DockerController(client)

# Machine Configuration (Migrate to DB)
machines_data = [
    {"id": "machine_1", "name": "Machine A"},
    {"id": "machine_2", "name": "Machine B"}
]

# InfluxDB Configuration
INFLUXDB_URL = "http://localhost:8086"  # Use the container name in Docker network
INFLUXDB_TOKEN = "EfONdgGfDr3LSOgs8zdKOD12zz3sKRygX1oqibXA3lmpXCnWsA0WnOJ5bKo7S-FEHevvwf0DEEZfHqDXUbMyJg=="  # Token for authentication
INFLUXDB_ORG = "MTU"  # Organization name (set in InfluxDB UI)
INFLUXDB_BUCKET = "vHIS"  # Bucket name (created in UI)

# Initialize InfluxDB Client
influx_client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = influx_client.write_api()

# MQTT Config
BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC_ALL = "+/+"  # Listen to all microservices
TOPICS = {
    "vOT-Mgmt/status",
    "vPLC/status",
    "vHMI/alarm",
    "vHMI/status",
    "vHIS/log",
    "vHIS/status",
    "vVIS/result",
    "vVIS/status",
    "vROB/task",
    "vROB/status"
}
DISCOVERED = set()

# MQTT Connection Callback
MQTT_TOPIC = "vOT-Mgmt/status"
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")
    client.subscribe(MQTT_TOPIC)

mqtt_messages = deque(maxlen=100)
# MQTT Message Callback
def on_message(client, userdata, message):
    topic = message.topic
    payload = ""
    try:
        payload = message.payload.decode("utf-8")
        #print(f"Main Service Received: '{payload}' from topic '{topic}'")
    except UnicodeDecodeError:
        False
        #print(f"Received non-UTF-8 message from topic '{topic}': {message.payload}")
    
    #mqtt_messages.append(f"{topic}: {payload}")
    
    # Service Discovery - Log new topics dynamically
    if topic not in DISCOVERED:
        DISCOVERED.add(topic)
        #print(f"Discovered new topic: {topic}")

    # Only process messages from known microservices
    if topic in TOPICS:
        print(f"OT Manager Service Received: '{payload}' from topic '{topic}'")
        mqtt_messages.append(f"{topic}: {payload}")
        
        # Store MQTT messages in InfluxDB
        # Get current time in seconds and convert to nanoseconds
        timestamp = int(time.time() * 1e9)  # Convert to nanoseconds

        # Create a simple data point
        point = Point("mqtt_messages") \
            .tag("topic", "vPLC/status") \
            .field("message", "Container started") \
            .time(timestamp, WritePrecision.NS)
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)

        print(f"Stored in InfluxDB: {topic} -> {payload}")
    
# Create MQTT client
try:
    mqtt_client = mqtt.Client(client_id="main_service")
    mqtt_client.on_message = on_message
    mqtt_client.connect(BROKER, PORT)
    mqtt_client.subscribe(TOPIC_ALL)  # Listen to all microservices

    # Start listening
    mqtt_client.loop_start()
    
except Exception as e:
    print(f"Failed to connect to MQTT broker: {e}")

###############

@app.get("/machine/{machine_id}/controls")
def view_machine_controls(request: Request, machine_id: int):
    # Example control elements (Later, fetch from DB)
    controls = [
        {"id": 1, "name": "vPLC", "status": "Running", "status_class": "green"},
        {"id": 2, "name": "vHMI", "status": "Stopped", "status_class": "red"},
        {"id": 3, "name": "vROB", "status": "Idle", "status_class": "orange"},
    ]
    
    return templates.TemplateResponse("vOT_Mgmt_Machine_Elements.html", {
        "request": request,
        "machine_id": machine_id,
        "controls": controls
    })

@app.get("/machines")
async def get_machines(request: Request):
    return templates.TemplateResponse("vOT_Mgmt_Overview.html", {"request": request, "machines": machines_data})

@app.post("/add_machine")
async def add_machine(request: Request, machine_name: str):
    new_machine = {"id": f"machine_{len(machines_data)+1}", "name": machine_name}
    machines_data.append(new_machine)
    return templates.TemplateResponse("machine.html", {"request": request, "machines": machines_data})

@app.get("/containers/{machine_id}")
async def container_management(request: Request, machine_id: str):
    return templates.TemplateResponse("index.html", {"request": request, "machine_id": machine_id})



#################





@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    try:
        all_containers = docker_ctrl.list_all_containers()
        all_images = docker_ctrl.list_all_images()
        running_containers = docker_ctrl.list_running_containers()
        stopped_containers = docker_ctrl.list_stopped_containers()
    except Exception as e:
        print(f"Error retrieving containers: {e}")
        all_containers = []
        all_images = []

    return templates.TemplateResponse("index.html", {
        "request": request,
        "all_containers": all_containers,
        "all_images": all_images,
        "running_containers": running_containers,
        "stopped_containers": stopped_containers
    })


@app.post("/start_container")
async def start_container(image: str = Form(...)):
    if not image:
        return {"error": "Image name is required"}

    image = image.strip().lower()  # Ensure lowercase and remove spaces
    mqtt_client.publish(MQTT_TOPIC, f"Starting container with image: {image}")

    try:
        container_id = docker_ctrl.run_container(image)
        mqtt_client.publish(MQTT_TOPIC, f"Container {container_id} started")
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        print(f"Error starting container: {e}")
        return {"error": str(e)}


@app.post("/stop_container")
async def stop_container(container_id: str = Form(...)):
    docker_ctrl.stop_container(container_id)
    mqtt_client.publish(MQTT_TOPIC, f"Container {container_id} stopped")
    return RedirectResponse(url="/", status_code=303)


@app.post("/remove_container")
async def remove_container(container_id: str = Form(...)):
    docker_ctrl.remove_container(container_id)
    mqtt_client.publish(MQTT_TOPIC, f"Container {container_id} removed")
    return RedirectResponse(url="/", status_code=303)


@app.get("/mqtt_messages")
async def get_mqtt_messages():
    return JSONResponse(content=list(mqtt_messages))





if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9970)

