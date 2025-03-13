# -------------------------------------------------------------------------------------------------- #
# Project:      OT Docker Container Management Service                                               #
# Description:                                                                                       #
# Author:       R00110936                                                                            #
# -------------------------------------------------------------------------------------------------- #

# Library Package Import Definitions
import os
import sys
import time
import uvicorn
from docker_utils import DockerInterface, DockerController
from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse

# Global variable Definitions

# Display Splash Screen
#start_menu = SplashScreen().load_splash_screen()

# Initialize FastAPI and templates
app = FastAPI()
templates = Jinja2Templates(directory="templates")

docker = DockerInterface()
client = docker.docker_connect()
print("Client: ", client)
docker_ctrl = DockerController(client)
print("Docker controller: ", docker_ctrl.client)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    try:
        all_containers = docker_ctrl.list_all_containers()  # Get running containers
        all_images = docker_ctrl.list_all_images()  # Get all images

        print("Containers: ", all_containers)
        print("Images: ", all_images)

#        if all_containers is None:
#            all_containers = []
#        if all_images is None:
#            all_images = []

    except Exception as e:
        print(f"Error retrieving containers: {e}")  # Debugging output
        all_containers = []  # Avoid NoneType error
        all_images = []

    return templates.TemplateResponse("index.html", {
        "request": request,
        "all_containers": all_containers,
        "all_images": all_images
    })

@app.post("/start_container")
async def start_container(image: str = Form(...)):
    docker_ctrl.run_container(image)
    return RedirectResponse(url="/", status_code=303)

@app.post("/stop_container")
async def stop_container(container_id: str = Form(...)):
    docker_ctrl.stop_container(container_id)
    return RedirectResponse(url="/", status_code=303)

@app.post("/remove_container")
async def remove_container(container_id: str = Form(...)):
    docker_ctrl.remove_container(container_id)
    return RedirectResponse(url="/", status_code=303)

@app.post("/execute_command")
async def execute_command(container_id: str = Form(...), command: str = Form(...)):
    docker_ctrl.exec_cmd_container(container_id, command)
    return RedirectResponse(url="/", status_code=303)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9970)

