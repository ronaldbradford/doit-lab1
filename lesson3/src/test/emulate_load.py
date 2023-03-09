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
            memory_usage = round(np.random.default_rng().uniform(0,1),2)
            cpu_usage = round(np.random.random(),2)
            if (int(iterations/4)) == 0:
                num += round(np.random.uniform(100))*round(np.random.uniform(6))
                memory_usage /= 2
            if int(num/9) == 0 and cpu_usage > 0.25:
                cpu_usage -= 0.21
            if int(num/2) == 0 and cpu_usage > 0.85:
                cpu_usage -= 0.06
            if int(num/10) == 0 and cpu_usage < 0.10:
                cpu_usage += 0.16
            if int(num/7) == 0 and memory_usage < 0.45:
                memory_usage *= 2

            self.client.post("/telemetry", json={
                "timestamp": f'{datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]}Z',
                "device_id": f"abc{num}",
                "memory_usage": memory_usage,
                "cpu_usage": cpu_usage
            })
