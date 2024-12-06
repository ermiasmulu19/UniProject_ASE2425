import os
import django
from locust import HttpUser, task, between

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project_name.settings")  # Replace with your Django project name
django.setup()

from rest_framework.authtoken.models import Token

class UserBehavior(HttpUser):
    wait_time = between(1, 3)  # Simulate user wait time between tasks
    
    def on_start(self):
        """
        This method runs when a simulated user starts.
        """
        self.register_user()
        self.login_user()

    def register_user(self):
        """
        Simulate user registration.
        """
        self.username = f"user_{self.environment.runner.user_count}"
        self.password = "password123"

        response = self.client.post("/register/", data={
            "username": self.username,
            "password": self.password
        })

        if response.status_code == 201:
            print(f"User {self.username} registered successfully!")
        else:
            print(f"Registration failed for {self.username}: {response.json()}")

    def login_user(self):
        """
        Simulate user login.
        """
        response = self.client.post("/login/", data={
            "username": self.username,
            "password": self.password
        })

        if response.status_code == 200:
            self.token = response.json().get("token")
            self.client.headers.update({"Authorization": f"Token {self.token}"})
            print(f"User {self.username} logged in successfully!")
        else:
            print(f"Login failed for {self.username}: {response.json()}")

    @task(2)
    def view_all_gachas(self):
        """
        Simulate viewing all gachas (admin endpoint).
        """
        response = self.client.get("/admin/gachas/")
        if response.status_code == 200:
            print("Viewed all gachas successfully.")
        else:
            print(f"Failed to view gachas: {response.json()}")

    @task(1)
    def create_gacha(self):
        """
        Simulate creating a gacha (admin action).
        """
        data = {
            "name": f"Gacha_{self.environment.runner.user_count}",
            "description": "This is a test gacha."
        }
        response = self.client.post("/create_gacha/", json=data)
        if response.status_code == 201:
            print("Gacha created successfully.")
        else:
            print(f"Failed to create gacha: {response.json()}")

    @task(1)
    def modify_user(self):
        """
        Simulate modifying user details.
        """
        response = self.client.put("/modify_user/", json={
            "username": f"updated_{self.username}",
            "email": f"{self.username}@example.com"
        })
        if response.status_code == 200:
            print("User details updated successfully.")
        else:
            print(f"Failed to update user: {response.json()}")
