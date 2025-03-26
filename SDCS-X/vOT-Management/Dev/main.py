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
from collections import deque

# Initialize FastAPI and templates
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Initialize Docker Controller
docker = DockerInterface()
client = docker.docker_connect()
docker_ctrl = DockerController(client)

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
    
    mqtt_messages.append(f"{topic}: {payload}")
    
    # Service Discovery - Log new topics dynamically
    if topic not in DISCOVERED:
        DISCOVERED.add(topic)
        #print(f"Discovered new topic: {topic}")

    # Only process messages from known microservices
    if topic in TOPICS:
        print(f"OT Manager Service Received: '{payload}' from topic '{topic}'")
    
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

