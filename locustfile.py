from locust import HttpUser, task, between


class AIplatformUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def health_check(self):
        self.client.get("/health")

    @task(1)
    def chat(self):
        self.client.post("/chat", json={
            "message": "What is DevOps?",
            "session_id": "loadtest"
        })
