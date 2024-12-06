import os
import django
from locust import HttpUser, task, between
import random

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project_name.settings")  # Replace with your Django project name
django.setup()

from rest_framework.authtoken.models import Token
from auction.models import Auction, Player  # Replace with your actual app name

class AuctionUser(HttpUser):
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

        # Create a test user if needed
        response = self.client.post("/register/", data={
            "username": self.username,
            "password": self.password
        })

        # Log in the user
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

    def setup_player(self):
        """
        Ensure the player has sufficient currency.
        """
        player = Player.objects.get(user__username=self.username)
        player.currency = 1000.00  # Give the player some initial currency
        player.save()

    def get_active_auction(self):
        """
        Retrieve an active auction.
        """
        active_auctions = Auction.objects.filter(end_time__gte=django.utils.timezone.now())
        if active_auctions.exists():
            return random.choice(active_auctions)
        return None

    @task
    def place_bid(self):
        """
        Simulate placing a bid on an active auction.
        """
        auction = self.get_active_auction()
        if not auction:
            print("No active auctions available for bidding.")
            return

        bid_amount = auction.current_price + random.uniform(1, 10)  # Bid slightly higher than the current price
        response = self.client.post(f"/auction/{auction.id}/bid/", json={
            "bid_amount": bid_amount
        })

        if response.status_code == 200:
            print(f"Successfully placed a bid of {bid_amount} on auction {auction.id}.")
        else:
            print(f"Failed to place bid: {response.json()}")
