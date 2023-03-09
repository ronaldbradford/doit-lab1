""" This API provides the /telemetry endpoint for the AppMod Lab """
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from mangum import Mangum
from . import models
from .db import insert as db

app = FastAPI()

@app.post("/telemetry")
async def post_telemetry_data(telemetry: models.Telemetry) -> models.Status:
    """/telemtry API POST endpoint"""
    status = db.insert(jsonable_encoder(telemetry))
    if status.success == True:
      return status

    raise HTTPException(status_code=418, detail=jsonable_encoder(status))

handler = Mangum(app, lifespan="off")
