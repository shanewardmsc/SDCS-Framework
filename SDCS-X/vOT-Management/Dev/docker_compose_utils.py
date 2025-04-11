import os
import subprocess
import yaml

# Create Docker Compose file
def generate_docker_compose_file(machines_data, compose_file_path="./docker-compose.yml"):
    compose_content = {
        "version": "3.8",
        "services": {}
    }

    for machine in machines_data:
        compose_content["services"][machine["name"]] = {
            "image": f"your_image_for_{machine['name']}",
            "ports": ["8080:80"],
            "environment": {"ENV_VAR": "value"}
        }

    with open(compose_file_path, 'w') as f:
        yaml.dump(compose_content, f, default_flow_style=False)
    
    return compose_file_path


# Start Docker Compose services
def start_docker_compose(compose_file_path="./docker-compose.yml"):
    if not os.path.exists(compose_file_path):
        return None, "Docker Compose file not found"

    result = subprocess.run(["docker-compose", "-f", compose_file_path, "up", "-d"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode('utf-8'), result.stderr.decode('utf-8')


# Stop Docker Compose services
def stop_docker_compose(compose_file_path="./docker-compose.yml"):
    if not os.path.exists(compose_file_path):
        return None, "Docker Compose file not found"

    result = subprocess.run(["docker-compose", "-f", compose_file_path, "down"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode('utf-8'), result.stderr.decode('utf-8')


# Check Docker Compose status
def get_docker_compose_status(compose_file_path="./docker-compose.yml"):
    if not os.path.exists(compose_file_path):
        return None, "Docker Compose file not found"

    result = subprocess.run(["docker-compose", "-f", compose_file_path, "ps"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode('utf-8'), result.stderr.decode('utf-8')
