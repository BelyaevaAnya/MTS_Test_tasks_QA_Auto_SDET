from locust import HttpUser, task, between
import random
import string

def random_string(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
class APILoadTest(HttpUser):
  
    wait_time = between(1, 10)
    host = "http://127.0.0.1:5000"

    @task(1)
    def test_inverse(self):
        self.client.post("/inverse", json={random_string(): random_string()})

    @task(2)
    def test_unstable(self):
        self.client.get("/unstable")
    
  