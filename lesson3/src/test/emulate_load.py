import numpy as np
from datetime import datetime
from locust import HttpUser, between, task
import time

class Telemetry(HttpUser):
    wait_time = between(1, 2)

    @task
    def send(self):
        num = round(np.random.uniform(100))
        for iterations in range(int(num/14)):
            memory_usage = round(np.random.default_rng().uniform(0,num/100),2)
            cpu_usage = round(np.random.random(),2)
            if (int(iterations/2)) == 0:
                num += round(np.random.uniform(100))*round(np.random.uniform(6))
            if int(num/9) == 0:
                cpu_usage -= 0.21

            self.client.post("/telemetry", json={
                "timestamp": f'{datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]}Z',
                "device_id": f"abc{num}",
                "memory_usage": memory_usage,
                "cpu_usage": cpu_usage
            })
