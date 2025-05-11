
from pathlib import Path
import os
import yaml
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field, validator
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
import uvicorn

# ------------------------------------------------------------------#
# Config
# ------------------------------------------------------------------#
DEFAULT_CFG_PATH = Path(os.getenv("TASK_METRICS_CFG", "config.yaml"))

def load_cfg():
    if DEFAULT_CFG_PATH.exists():
        with DEFAULT_CFG_PATH.open() as fp:
            return yaml.safe_load(fp) or {}
    return {}

cfg = load_cfg()
PORT = int(os.getenv("PORT", cfg.get("port", 8080)))

# ------------------------------------------------------------------#
# Metrics
# ------------------------------------------------------------------#
TASK_DURATION = Gauge(
    name="task_duration_seconds",
    documentation="Duration of external tasks in seconds",
    labelnames=("tool", "task", "status"),
)

# ------------------------------------------------------------------#
# Pydantic schema
# ------------------------------------------------------------------#
class TaskIn(BaseModel):
    tool: str = Field(..., example="upgrader")
    task: str = Field(..., example="healthchecks")
    status: str = Field(..., regex="^(completed|failed|succeeded)$")
    duration: int = Field(..., gt=0, example=120)

    @validator("duration")
    def duration_positive(cls, value):
        if value <= 0:
            raise ValueError("duration must be positive")
        return value

# ------------------------------------------------------------------#
# FastAPI app
# ------------------------------------------------------------------#
app = FastAPI(title="Task Metrics Service")

@app.post("/api/tasks", status_code=202)
def ingest(task: TaskIn):
    TASK_DURATION.labels(task.tool, task.task, task.status).set(task.duration)
    return {"accepted": True}

@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    data = generate_latest()
    return PlainTextResponse(content=data.decode(), media_type=CONTENT_TYPE_LATEST)

# ------------------------------------------------------------------#
# Entrypoint
# ------------------------------------------------------------------#

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")

