from fastapi import FastAPI
from pydantic import BaseModel, constr, confloat
from datetime import datetime

class Telemetry(BaseModel):
    timestamp: datetime
    device_id: constr(min_length=1, max_length=100)
    memory_usage: confloat(ge=0.0, le=1.0)
    cpu_usage: confloat(ge=0.0, le=1.0)

app = FastAPI()

@app.post("/telemetry")
async def post_telemetry_data(telemetry: Telemetry):
    return telemetry
