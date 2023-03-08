""" This API provides the /telemetry endpoint for the AppMod Lab """
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from mangum import Mangum
from . import models
from .db import insert as db

app = FastAPI()

@app.post("/telemetry")
async def post_telemetry_data(telemetry: models.Telemetry):
    """/telemtry API POST endpoint"""
    return db.insert(jsonable_encoder(telemetry))

handler = Mangum(app, lifespan="off")
