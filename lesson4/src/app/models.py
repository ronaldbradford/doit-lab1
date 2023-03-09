""" Data Struture Models used for this lesson """
from datetime import datetime
from pydantic import BaseModel, Field, constr, confloat
from typing import Union

class Telemetry(BaseModel):
    """Base class for Telemtry object"""
    timestamp: datetime = Field(title="The recorded timestamp of the telemetry data")
    device_id: constr(min_length=1, max_length=100) = Field(title="The device Identifier")
    memory_usage: confloat(ge=0.0, le=1.0) = Field(title="The Memory usage of the device")
    cpu_usage: confloat(ge=0.0, le=1.0) = Field(title="The CPU usage of the device")

class Status(BaseModel):
    """Base class for Response Status"""
    success: bool = Field(title="The success of the endpoint")
    error:  Union[str, None] = Field(title="An error message if there is one")
