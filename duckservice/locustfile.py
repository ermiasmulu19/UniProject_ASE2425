import os
import django
from locust import HttpUser, task, between
import random

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project_name.settings")  # Replace with your Django project name
django.setup()

from rest_framework.authtoken.models import Token
from duckservice.models import Duck, Player  # Replace with your actual app name and models

class GachaUser(HttpUser):
    wait_time = between(1, 3)  # Simulate user wait time between tasks
    
    def on_start(self):
        """
        Runs when a user starts.
        """
        self.login_user()
        self.setup_player()

    def login_user(self):
        """
        Simulate user login and get authentication token.
        """
        self.username = f"user_{self.environment.runner.user_count}"
        self.password = "password123"

        # Register and log in user
        self.client.post("/register/", data={
            "username": self.username,
            "password": self.password
        })

        response = self.client.post("/login/", data={
            "username": self.username,
            "password": self.password
        })

        if response.status_code == 200:
            self.token = response.json().get("token")
            self.client.headers.update({"Authorization": f"Token {self.token}"})
        else:
            print(f"Login failed for {self.username}: {response.json()}")

    def setup_player(self):
        """
        Ensure the player has sufficient currency for gacha rolls.
        """
        try:
            player = Player.objects.get(user__username=self.username)
            player.currency = 100  # Give the player some initial currency
            player.save()
        except Player.DoesNotExist:
            print(f"Player {self.username} not found!")

    @task(2)
    def spin_duck(self):
        """
        Simulate spinning for a duck.
        """
        response = self.client.post("/spin-duck/")
        if response.status_code == 200:
            result = response.json()
            print(f"Successfully spun a duck: {result.get('duck', {}).get('name')}")
        else:
            print(f"Spin failed: {response.json()}")

    @task(3)
    def roll_gacha(self):
        """
        Simulate rolling the gacha.
        """
        response = self.client.post("/roll-gacha/")
        if response.status_code == 200:
            result = response.json()
            print(f"Gacha roll result: {result.get('result')}")
        else:
            print(f"Gacha roll failed: {response.json()}")

    @task(1)
    def system_gacha_collection(self):
        """
        Simulate fetching the system-wide gacha collection.
        """
        response = self.client.get("/system-gacha-collection/")
        if response.status_code == 200:
            print("Retrieved system-wide gacha collection successfully.")
        else:
            print(f"Failed to retrieve system-wide gacha collection: {response.json()}")

    @task(1)
    def gacha_info(self):
        """
        Simulate fetching detailed info about a specific gacha.
        """
        ducks = Duck.objects.all()
        if not ducks.exists():
            print("No ducks available to fetch info.")
            return

        duck_id = random.choice(ducks).id
        response = self.client.get(f"/system-gacha-info/{duck_id}/")
        if response.status_code == 200:
            print(f"Retrieved info for gacha ID {duck_id}")
        else:
            print(f"Failed to retrieve info for gacha ID {duck_id}: {response.json()}")
