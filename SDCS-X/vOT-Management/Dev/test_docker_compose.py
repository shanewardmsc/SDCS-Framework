from docker_compose_utils import generate_docker_compose_file, start_docker_compose, stop_docker_compose, get_docker_compose_status

# Example FastAPI endpoint
#@app.post("/create_docker_compose")
#async def create_docker_compose(request: Request):
#    username = request.cookies.get("username")
#    if not username or username not in logged_in_users:
#        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

machines_data = [
    {
        "id": "00101_Depal_Cell",
        "name": "Robotic Depalletizer",
        "type": "Robotic",
        "container_image": "robotics/depal_container:latest",
        "status": "active",
        "ports": ["8081:80"],
        "environment": {
            "ENV_VAR": "value1",
            "DEVICE_ID": "12345"
        },
        "resources": {
            "memory": "2GB",
            "cpu": "1"
        },
        "created_timestamp": "2025-04-10T10:00:00"
    },
    {
        "id": "00102_Inspect_Cell",
        "name": "Vision Quality Inspection",
        "type": "Vision",
        "container_image": "vision/inspect_container:latest",
        "status": "inactive",
        "ports": ["8082:80"],
        "environment": {
            "ENV_VAR": "value2",
            "DEVICE_ID": "67890"
        },
        "resources": {
            "memory": "4GB",
            "cpu": "2"
        },
        "created_timestamp": "2025-04-09T15:30:00"
    },
    {
        "id": "00103_Pack_Cell",
        "name": "Robotic Packaging",
        "type": "Robotic",
        "container_image": "robotics/pack_container:latest",
        "status": "inactive",
        "ports": ["8083:80"],
        "environment": {
            "ENV_VAR": "value3",
            "DEVICE_ID": "11223"
        },
        "resources": {
            "memory": "3GB",
            "cpu": "1"
        },
        "created_timestamp": "2025-04-08T14:20:00"
    }
]





    
    # Generate Docker Compose file based on machines data
compose_file_path = generate_docker_compose_file(machines_data)
    
#    return JSONResponse(content={"message": "Docker Compose file created successfully", "file_path": compose_file_path})


#@app.post("/start_docker_compose")
#async def start_docker_compose_service(request: Request):
#    username = request.cookies.get("username")
#    if not username or username not in logged_in_users:
#        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    # Ensure Docker Compose file exists
#    if not os.path.exists("docker-compose.yml"):
#        return JSONResponse(content={"error": "Docker Compose file not found"}, status_code=400)
    

#########

#stdout, stderr = start_docker_compose()

#########

#    if stderr:
#        return JSONResponse(content={"error": stderr}, status_code=400)
#    return JSONResponse(content={"message": "Docker Compose services started", "stdout": stdout})


#@app.post("/stop_docker_compose")
#async def stop_docker_compose_service(request: Request):
#    username = request.cookies.get("username")
#    if not username or username not in logged_in_users:
#        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

########

#stdout, stderr = stop_docker_compose()

########

#    if stderr:
#        return JSONResponse(content={"error": stderr}, status_code=400)
#    return JSONResponse(content={"message": "Docker Compose services stopped", "stdout": stdout})


#@app.get("/docker_compose_status")
#async def docker_compose_status(request: Request):
#    username = request.cookies.get("username")
#    if not username or username not in logged_in_users:
#        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

stdout, stderr = get_docker_compose_status()
#    if stderr:
#        return JSONResponse(content={"error": stderr}, status_code=400)
    
#    return JSONResponse(content={"status": stdout})
