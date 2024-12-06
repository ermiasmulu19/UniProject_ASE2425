from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from .models import Auction, Player, User
from rest_framework.test import APIClient

class AuctionBidTests(TestCase):

    def setUp(self):
        """
        Set up the test environment.
        Create a user, player, and an auction.
        """
        # Create a user
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        
        # Create a player for the user
        self.player = Player.objects.create(user=self.user, currency=1000)
        
        # Create an auction
        self.auction = Auction.objects.create(
            name="Test Auction",
            description="A test auction",
            current_price=100,
            highest_bidder=None,
            end_time=timezone.now() + timezone.timedelta(hours=1)  # Auction will end in 1 hour
        )

        # Set up the API client
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_auction_not_found(self):
        """
        Test that trying to place a bid on a non-existent auction returns a 404 error.
        """
        url = reverse('place_bid', kwargs={'auction_id': 999})  # Non-existent auction ID
        response = self.client.post(url, {'bid_amount': 150})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Auction not found')

    def test_auction_expired(self):
        """
        Test that trying to place a bid on an expired auction returns an error.
        """
        # Create an expired auction
        expired_auction = Auction.objects.create(
            name="Expired Auction",
            description="This auction has expired",
            current_price=100,
            highest_bidder=None,
            end_time=timezone.now() - timezone.timedelta(hours=1)  # Auction ended 1 hour ago
        )
        url = reverse('place_bid', kwargs={'auction_id': expired_auction.id})
        response = self.client.post(url, {'bid_amount': 150})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Auction has expired')

    def test_bid_amount_less_than_current_price(self):
        """
        Test that trying to place a bid that is less than or equal to the current price returns an error.
        """
        url = reverse('place_bid', kwargs={'auction_id': self.auction.id})
        response = self.client.post(url, {'bid_amount': 50})  # Less than current price (100)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Bid amount must be greater than the current price')

    def test_insufficient_currency(self):
        """
        Test that trying to place a bid without sufficient currency returns an error.
        """
        # Set player's currency to less than the bid amount
        self.player.currency = 50
        self.player.save()

        url = reverse('place_bid', kwargs={'auction_id': self.auction.id})
        response = self.client.post(url, {'bid_amount': 150})  # Player has less than 150
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Insufficient currency')

    def test_successful_bid(self):
        """
        Test that a valid bid successfully updates the auction.
        """
        url = reverse('place_bid', kwargs={'auction_id': self.auction.id})
        response = self.client.post(url, {'bid_amount': 150})  # Valid bid amount (greater than current price)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], 'Bid placed successfully!')
        self.assertEqual(response.data['current_price'], 150)

        # Check that the auction's highest_bidder and current_price have been updated
        self.auction.refresh_from_db()
        self.assertEqual(self.auction.current_price, 150)
        self.assertEqual(self.auction.highest_bidder, self.player)

