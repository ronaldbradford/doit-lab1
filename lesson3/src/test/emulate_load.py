import numpy as np
from datetime import datetime
from locust import HttpUser, between, task
import time

class Telemetry(HttpUser):
    wait_time = between(1, 2)

    @task
    def send(self):
        self.client.post("/telemetry", json={
            "timestamp": f'{datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]}Z',
            "device_id": f"abc{round(np.random.uniform(100))}",
            "memory_usage": round(np.random.default_rng().uniform(0,1),2),
            "cpu_usage": round(np.random.random(),2)
        })
