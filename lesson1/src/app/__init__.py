""" This API provides the /telemetry endpoint for the AppMod Lab """
from fastapi import FastAPI
from . import models

app = FastAPI()

@app.post("/telemetry")
async def post_telemetry_data(telemetry: models.Telemetry):
    """/telemtry API POST endpoint"""
    return telemetry
