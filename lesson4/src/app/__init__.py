from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from mangum import Mangum
from pydantic import BaseModel, constr, confloat
from datetime import datetime
from .db import insert as db

class Telemetry(BaseModel):
    timestamp: datetime
    device_id: constr(min_length=1, max_length=100)
    memory_usage: confloat(ge=0.0, le=1.0)
    cpu_usage: confloat(ge=0.0, le=1.0)

app = FastAPI()

@app.post("/telemetry")
async def post_telemetry_data(telemetry: Telemetry):
    return db.insert(jsonable_encoder(telemetry))

handler = Mangum(app, lifespan="off")
