from fastapi import FastAPI, HTTPException
import docker
import prometheus_client
from prometheus_client import Gauge
import uvicorn

app = FastAPI()
client = docker.from_env()

# Prometheus metrics
total_containers = Gauge("total_containers", "Total running containers")
faulted_containers = Gauge("faulted_containers", "Containers in a faulted state")

@app.get("/containers")
def list_containers():
    """List all running containers."""
    containers = client.containers.list()
    total_containers.set(len(containers))
    return [{"id": c.id, "name": c.name, "status": c.status} for c in containers]

@app.post("/containers/{container_id}/restart")
def restart_container(container_id: str):
    """Restart a specific container."""
    try:
        container = client.containers.get(container_id)
        container.restart()
        return {"message": f"Container {container_id} restarted successfully."}
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail="Container not found")

@app.get("/metrics")
def get_metrics():
    """Expose Prometheus metrics."""
    return prometheus_client.generate_latest()

# Health check & auto-restart failed containers
@app.get("/healthcheck")
def health_check():
    """Check container health and restart if needed."""
    containers = client.containers.list()
    faulted = 0
    for container in containers:
        if container.status != "running":
            container.restart()
            faulted += 1
    faulted_containers.set(faulted)
    return {"faulted_containers": faulted}

# Grafana Dashboards Configuration Endpoint
@app.get("/grafana-config")
def grafana_config():
    """Provide a basic Grafana dashboard configuration for monitoring."""
    dashboard = {
        "dashboard": {
            "title": "Docker Container Monitoring",
            "panels": [
                {
                    "title": "Total Containers",
                    "type": "gauge",
                    "targets": [{"expr": "total_containers", "legendFormat": "Total"}]
                },
                {
                    "title": "Faulted Containers",
                    "type": "gauge",
                    "targets": [{"expr": "faulted_containers", "legendFormat": "Faulted"}]
                }
            ]
        }
    }
    return dashboard

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9990)
