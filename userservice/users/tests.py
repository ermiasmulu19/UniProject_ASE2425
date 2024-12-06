from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from api.models import Duck, Player
from rest_framework.authtoken.models import Token

class UserServiceTests(TestCase):
    def setUp(self):
        # Create a normal user and an admin user
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.admin_user = User.objects.create_superuser(username="adminuser", password="adminpassword")
        
        # Create a player for the normal user
        self.player = Player.objects.create(user=self.user, currency=0.0)

        # Set up the API client
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # Set up the API client for admin
        self.admin_client = APIClient()
        self.admin_client.force_authenticate(user=self.admin_user)

    def test_register_api_success(self):
        url = '/api/register/'
        data = {'username': 'newuser', 'password': 'newpassword'}
        response = self.client.post(url, data, format='json')
        
        # Check if the user is successfully created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['success'], 'User registered successfully!')

    def test_register_api_missing_fields(self):
        url = '/api/register/'
        data = {'username': 'newuser'}
        response = self.client.post(url, data, format='json')
        
        # Check if the missing password returns the correct error
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Username and password are required')

    def test_register_api_username_exists(self):
        url = '/api/register/'
        data = {'username': 'testuser', 'password': 'newpassword'}
        response = self.client.post(url, data, format='json')
        
        # Check if it returns error when username already exists
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Username already exists')

    def test_login_api_success(self):
        url = '/api/login/'
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')
        
        # Check if login is successful and a token is returned
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_api_invalid_credentials(self):
        url = '/api/login/'
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(url, data, format='json')
        
        # Check if invalid credentials return the correct error
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], 'Invalid credentials')

    def test_user_logout(self):
        url = '/api/logout/'
        response = self.client.post(url)
        
        # Check if user logout is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'User logged out successfully')

    def test_user_logout_unauthenticated(self):
        self.client.logout()
        url = '/api/logout/'
        response = self.client.post(url)
        
        # Check if logout fails for unauthenticated users
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'], 'Authentication required.')

    def test_user_delete_api_success(self):
        url = '/api/delete_user/'
        response = self.client.delete(url)
        
        # Check if the user is deleted successfully
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], 'User account deleted successfully')

    def test_user_delete_api_unauthenticated(self):
        self.client.logout()
        url = '/api/delete_user/'
        response = self.client.delete(url)
        
        # Check if trying to delete while unauthenticated returns the correct error
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'], 'Authentication required.')

    def test_modify_user_success(self):
        url = '/api/modify_user/'
        data = {'username': 'newusername', 'email': 'newemail@example.com'}
        response = self.client.put(url, data, format='json')
        
        # Check if the user info is updated successfully
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'newusername')
        self.assertEqual(response.data['email'], 'newemail@example.com')

    def test_modify_user_unauthenticated(self):
        self.client.logout()
        url = '/api/modify_user/'
        data = {'username': 'newusername'}
        response = self.client.put(url, data, format='json')
        
        # Check if unauthenticated users are blocked
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'], 'Authentication required.')

    def test_create_gacha_success(self):
        url = '/api/create_gacha/'
        self.client.force_authenticate(user=self.admin_user)  # Ensure admin access
        data = {'name': 'Rare Duck', 'rarity': 'R'}
        response = self.admin_client.post(url, data, format='json')
        
        # Check if the gacha (duck) is created successfully
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['success'], 'Gacha created successfully!')
    
    def test_create_gacha_permission_error(self):
        url = '/api/create_gacha/'
        data = {'name': 'Rare Duck', 'rarity': 'R'}
        response = self.client.post(url, data, format='json')
        
        # Check if permission error occurs when non-admin tries to create a gacha
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_gacha_success(self):
        # Create a gacha first
        gacha = Duck.objects.create(name='Duck', rarity='C')
        
        url = f'/api/update_gacha/{gacha.id}/'
        data = {'rarity': 'R'}
        response = self.admin_client.put(url, data, format='json')
        
        # Check if the gacha is updated successfully
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], 'Gacha updated successfully!')

    def test_update_gacha_not_found(self):
        url = '/api/update_gacha/999/'
        data = {'rarity': 'R'}
        response = self.admin_client.put(url, data, format='json')
        
        # Check if error is returned for a non-existing gacha
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_gacha_success(self):
        gacha = Duck.objects.create(name='Duck', rarity='C')
        
        url = f'/api/delete_gacha/{gacha.id}/'
        response = self.admin_client.delete(url)
        
        # Check if gacha is deleted successfully
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], 'Gacha deleted successfully!')

    def test_delete_gacha_not_found(self):
        url = '/api/delete_gacha/999/'
        response = self.admin_client.delete(url)
        
        # Check if error is returned for a non-existing gacha
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_view_all_gachas(self):
        # Create a few gachas
        Duck.objects.create(name="Duck 1", rarity="C")
        Duck.objects.create(name="Duck 2", rarity="R")
        
        url = '/api/admin_view_all_gachas/'
        response = self.admin_client.get(url)
        
        # Check if all gachas are returned successfully
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['gachas']), 2)
