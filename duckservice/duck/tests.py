from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Duck, Auction, Player, User
from datetime import timedelta
from unittest.mock import patch

class GachaTests(TestCase):

    def setUp(self):
        """
        Set up the test environment with ducks, users, and players.
        """
        # Create a user
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        
        # Create a player for the user
        self.player = Player.objects.create(user=self.user, currency=100)

        # Create ducks with various rarities
        self.duck_common = Duck.objects.create(name="Common Duck", rarity="C")
        self.duck_rare = Duck.objects.create(name="Rare Duck", rarity="R")
        self.duck_super_rare = Duck.objects.create(name="Super Rare Duck", rarity="SR")
        self.duck_ultra_rare = Duck.objects.create(name="Ultra Rare Duck", rarity="UR")
        self.duck_special_rare = Duck.objects.create(name="Special Ultra Rare Duck", rarity="SUR")
        
        # Set up the API client
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_system_gacha_info(self):
        """
        Test that the system gacha info endpoint retrieves the correct gacha information.
        """
        url = reverse('system_gacha_info', kwargs={'gacha_id': self.duck_common.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.duck_common.name)
        self.assertEqual(response.data['rarity'], self.duck_common.rarity)

    def test_system_gacha_info_not_found(self):
        """
        Test that the system gacha info endpoint returns an error for a non-existing duck.
        """
        url = reverse('system_gacha_info', kwargs={'gacha_id': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Gacha not found in the system')

    def test_gacha_info(self):
        """
        Test that the gacha info endpoint retrieves the correct gacha owned by the player.
        """
        # Create a duck for the player
        url = reverse('gacha_info', kwargs={'gacha_id': self.duck_common.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.duck_common.name)

    def test_gacha_info_not_found(self):
        """
        Test that the gacha info endpoint returns an error for a non-existing duck.
        """
        url = reverse('gacha_info', kwargs={'gacha_id': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Gacha not found')

    def test_system_gacha_collection(self):
        """
        Test that the system-wide gacha collection is retrieved successfully.
        """
        url = reverse('system_gacha_collection')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['system_gacha_collection']), 5)  # 5 ducks created

    @patch('random.choice')
    def test_spin_duck_api(self, mock_random_choice):
        """
        Test the spin duck API, ensuring it creates an auction for the duck.
        """
        # Mock the random duck selection
        mock_random_choice.return_value = self.duck_common
        
        url = reverse('spin_duck')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that the duck and auction info are returned
        self.assertEqual(response.data['duck']['name'], self.duck_common.name)
        self.assertEqual(response.data['auction']['duck'], self.duck_common.id)

        # Check that the auction was created
        auction = Auction.objects.get(id=response.data['auction']['id'])
        self.assertEqual(auction.duck, self.duck_common)

    def test_spin_duck_api_unauthenticated(self):
        """
        Test that the spin duck API returns an error if the user is not authenticated.
        """
        self.client.logout()
        url = reverse('spin_duck')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], 'Authentication required')

    @patch('random.random')
    def test_roll_gacha_api(self, mock_random):
        """
        Test the roll gacha API, ensuring it correctly handles the gacha roll and auction creation.
        """
        # Mock the random roll value
        mock_random.return_value = 0.02  # Simulate a 'R' (Rare) roll

        url = reverse('roll_gacha')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the correct duck and auction details are returned
        self.assertIn('You got a Rare Duck', response.data['result'])
        self.assertEqual(response.data['currency'], 90)  # Currency should be reduced by 10
        self.assertEqual(response.data['duck']['rarity'], 'R')

        # Check that the auction was created
        auction = Auction.objects.get(id=response.data['duck']['auction_id'])
        self.assertEqual(auction.duck.name, 'Rare Duck')

    def test_roll_gacha_api_insufficient_currency(self):
        """
        Test that the roll gacha API returns an error when the player has insufficient currency.
        """
        self.player.currency = 5  # Less than 10
        self.player.save()

        url = reverse('roll_gacha')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Not enough currency')

    def test_roll_gacha_api_unauthenticated(self):
        """
        Test that the roll gacha API returns an error if the user is not authenticated.
        """
        self.client.logout()
        url = reverse('roll_gacha')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], 'Authentication required')
