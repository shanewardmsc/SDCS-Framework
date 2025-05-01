import docker

# Create a client connected via Unix socket
client = docker.DockerClient(base_url='unix:///var/run/docker.sock')

try:
    # Try to list containers to verify connection
    containers = client.containers.list()
    print(f"Connected to Docker! Found containers: {containers}")
except docker.errors.DockerException as error:
    print(f"Failed to connect to Docker: {error}")
except Exception as error:
    print(f"Unexpected error: {error}")
