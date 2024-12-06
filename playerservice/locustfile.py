import os
import django
from locust import HttpUser, task, between
from decimal import Decimal

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project_name.settings")  # Replace with your Django project name
django.setup()

from playerservice.player.models import Player  # Replace with your app and model names

class PlayerUser(HttpUser):
    wait_time = between(1, 3)  # Simulate wait time between tasks

    def on_start(self):
        """
        Runs when a user starts. Logs in and sets up the player.
        """
        self.login_user()
        self.setup_player()

    def login_user(self):
        """
        Simulate user login and store the token for authentication.
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
        Ensure the player has sufficient currency for testing.
        """
        try:
            player = Player.objects.get(user__username=self.username)
            player.currency = Decimal(100)  # Give the player initial currency
            player.save()
        except Player.DoesNotExist:
            print(f"Player {self.username} not found!")

    @task(3)
    def view_home_api(self):
        """
        Simulate viewing the home page with active auctions and player details.
        """
        response = self.client.get("/home-api/")
        if response.status_code == 200:
            print("Home API fetched successfully.")
        else:
            print(f"Failed to fetch home API: {response.json()}")

    @task(2)
    def view_profile(self):
        """
        Simulate viewing the player's profile.
        """
        response = self.client.get("/profile/")
        if response.status_code == 200:
            print("Profile fetched successfully.")
        else:
            print(f"Failed to fetch profile: {response.json()}")

    @task(2)
    def view_transaction_history(self):
        """
        Simulate viewing the player's transaction history.
        """
        response = self.client.get("/transaction-history/")
        if response.status_code == 200:
            print("Transaction history fetched successfully.")
        else:
            print(f"Failed to fetch transaction history: {response.json()}")

    @task(2)
    def buy_currency(self):
        """
        Simulate buying currency for the player.
        """
        response = self.client.post("/buy-currency/", json={"amount": 50})
        if response.status_code == 200:
            print("Currency purchased successfully.")
        else:
            print(f"Failed to purchase currency: {response.json()}")

    @task(1)
    def view_my_gacha_collection(self):
        """
        Simulate viewing the player's gacha collection.
        """
        response = self.client.get("/my-gacha-collection/")
        if response.status_code == 200:
            print("Gacha collection fetched successfully.")
        else:
            print(f"Failed to fetch gacha collection: {response.json()}")
