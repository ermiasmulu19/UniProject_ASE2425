from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient
from decimal import Decimal
from .models import Player, Duck, Auction
from django.contrib.auth.models import User
from unittest.mock import patch

class PlayerServiceTests(TestCase):

    def setUp(self):
        """
        Set up the test environment with users, players, ducks, and auctions.
        """
        # Create a user
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        
        # Create a player for the user
        self.player = Player.objects.create(user=self.user, currency=100)

        # Create ducks
        self.duck1 = Duck.objects.create(name="Duck 1", rarity="C")
        self.duck2 = Duck.objects.create(name="Duck 2", rarity="R")
        
        # Create auctions for the player
        self.auction1 = Auction.objects.create(duck=self.duck1, owner=self.user, starting_price=0.0, current_price=10.0, end_time=timezone.now() + timedelta(days=1))
        self.auction2 = Auction.objects.create(duck=self.duck2, owner=self.user, starting_price=0.0, current_price=20.0, end_time=timezone.now() + timedelta(days=1))

        # Set up the API client
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_home_api(self):
        """
        Test that the home API endpoint returns the player's details and active auctions.
        """
        url = reverse('home_api')
        response = self.client.get(url)
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check player's details
        self.assertEqual(response.data['player']['username'], self.user.username)
        self.assertEqual(response.data['player']['currency'], self.player.currency)

        # Check auctions data
        self.assertEqual(len(response.data['auctions']), 2)
        self.assertEqual(response.data['auctions'][0]['duck']['name'], self.duck1.name)
        self.assertEqual(response.data['auctions'][1]['duck']['name'], self.duck2.name)

    def test_home_api_unauthenticated(self):
        """
        Test that the home API returns an error if the user is not authenticated.
        """
        self.client.logout()
        url = reverse('home_api')
        response = self.client.get(url)
        
        # Check status code and error message
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], 'Authentication required')

    def test_profile(self):
        """
        Test that the profile endpoint returns the player's ducks and username.
        """
        url = reverse('profile')
        response = self.client.get(url)
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check player's ducks in response
        self.assertEqual(len(response.data['ducks']), 2)
        self.assertEqual(response.data['user'], self.user.username)

    def test_transaction_history(self):
        """
        Test that the transaction history API returns the player's bids and auctions.
        """
        # Create a bid for the player on an auction
        self.auction1.highest_bidder = self.player
        self.auction1.save()

        url = reverse('transaction_history')
        response = self.client.get(url)

        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the bids and auctions
        self.assertEqual(len(response.data['bids']), 1)
        self.assertEqual(len(response.data['auctions']), 2)  # Player has 2 auctions

    def test_buy_currency(self):
        """
        Test that the buy currency API successfully adds currency to the player's account.
        """
        url = reverse('buy_currency')
        response = self.client.post(url, {'amount': 50.0})
        
        # Check status code and updated currency balance
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.player.refresh_from_db()
        self.assertEqual(self.player.currency, Decimal('150.0'))

    def test_buy_currency_invalid_amount(self):
        """
        Test that the buy currency API returns an error for invalid amount.
        """
        url = reverse('buy_currency')
        response = self.client.post(url, {'amount': 0.0})  # Invalid amount
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid amount')

    def test_my_gacha_collection(self):
        """
        Test that the my gacha collection endpoint returns the player's ducks.
        """
        url = reverse('my_gacha_collection')
        response = self.client.get(url)
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the player's ducks are in the response
        self.assertEqual(len(response.data['gacha_collection']), 2)

    def test_my_gacha_collection_player_not_found(self):
        """
        Test that the my gacha collection API returns an error if the player is not found.
        """
        self.client.logout()
        url = reverse('my_gacha_collection')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Player not found')
