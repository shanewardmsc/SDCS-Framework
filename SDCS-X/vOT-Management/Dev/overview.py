from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Sample Data Storage (Replace with Database in Future)
machines = [
    {"id": "machine_1", "name": "Machine A", "status": "running", "containers": []},
    {"id": "machine_2", "name": "Machine B", "status": "stopped", "containers": []}
]

@app.get("/")
async def production_line(request: Request):
    return templates.TemplateResponse("production_line.html", {"request": request, "machines": machines})

@app.post("/add_machine")
async def add_machine(request: Request, machine_name: str = Form(...)):
    new_machine = {"id": f"machine_{len(machines) + 1}", "name": machine_name, "status": "running", "containers": []}
    machines.append(new_machine)
    return RedirectResponse(url="/", status_code=303)

@app.get("/machine/{machine_id}")
async def machine_detail(request: Request, machine_id: str):
    machine = next((m for m in machines if m["id"] == machine_id), None)
    if not machine:
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse("machine_details.html", {"request": request, "machine": machine})

@app.post("/add_container/{machine_id}")
async def add_container(request: Request, machine_id: str, container_name: str = Form(...)):
    machine = next((m for m in machines if m["id"] == machine_id), None)
    if machine:
        new_container = {"id": f"container_{len(machine['containers']) + 1}", "name": container_name, "status": "running"}
        machine["containers"].append(new_container)
    return RedirectResponse(url=f"/machine/{machine_id}", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9030)
