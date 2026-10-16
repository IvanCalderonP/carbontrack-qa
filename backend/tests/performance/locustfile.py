"""Optional local smoke load: locust -f tests/performance/locustfile.py --host=http://localhost:8000."""

import os

from locust import HttpUser, between, task


class PortfolioReader(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        email = os.environ["LOAD_TEST_EMAIL"]
        password = os.environ["LOAD_TEST_PASSWORD"]
        response = self.client.post("/api/v1/auth/login", json={"email": email, "password": password})
        response.raise_for_status()
        self.client.headers.update({"Authorization": f"Bearer {response.json()['access_token']}"})

    @task(3)
    def products(self):
        self.client.get("/api/v1/products?page=1&page_size=10")

    @task(1)
    def dashboard(self):
        self.client.get("/api/v1/dashboard/summary")
