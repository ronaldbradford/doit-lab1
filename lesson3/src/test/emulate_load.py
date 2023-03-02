import numpy as np
from datetime import datetime
from locust import HttpUser, between, task

class Telemetry(HttpUser):
    wait_time = between(1, 2)
    
    @task
    def send(self):
        self.client.post("/telemetry", json={
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "device_id": f"abc{round(np.random.uniform(100))}",
            "memory_usage": round(np.random.uniform(),2),
            "cpu_usage": round(np.random.uniform(),2)
        })
