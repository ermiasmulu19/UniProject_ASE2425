from django.utils import timezone

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from api.serializers import DuckSerializer
from .models import Duck, Auction, Player
from datetime import timedelta
import random
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny




@api_view(['GET'])
def home_api(request):
    """
    API endpoint to retrieve active auctions and the player's details.
    """
    print(f"Request User: {request.user}")

    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        
        player = Player.objects.get(user=request.user)
        print(player)
        print(player, 'this one is a player ena let me check it out')
        active_auctions = Auction.objects.filter(end_time__gt=now())
        
        auctions_data = [
            {
                'id': auction.id,
                'duck': {
                    'name': auction.duck.name,
                    'rarity': auction.duck.rarity,
                },
                'current_price': auction.current_price,
                'end_time': auction.end_time,
            }
            for auction in active_auctions
        ]

        return Response({
            'player': {'id': player.id, 'username': player.user.username, 'currency': player.currency},
            'auctions': auctions_data,
        }, status=status.HTTP_200_OK)
    except Player.DoesNotExist:
        return Response({'error': 'Player not found'}, status=status.HTTP_404_NOT_FOUND)

    
@api_view(['POST'])
def register_api(request):
    username = request.data.get('username')
    password = request.data.get('password')
    print(username, password, "this is the user name and password")

    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.create_user(username=username, password=password)
        Token.objects.create(user=user)  # Generate a token for authentication if needed
        return Response({'success': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):

    username = request.data.get('username')
    password = request.data.get('password')
    print(username, password, 'eski endezi eneyew ayshalmm apapicho')

    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        player, created=Player.objects.get_or_create(user=user)
        
        if created:
            player.currency==0.00
            player.save()  
      
        
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
@api_view(['POST'])
def user_logout(request):
    if not request.user.is_authenticated:
        return Response({"message": "Authentication required."}, status=401)

    logout(request)

    return Response({"message": "User logged out successfully"}, status=200)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def user_delete_api(request):
    """
    API endpoint to delete the authenticated user's account.
    """
    user = request.user

    try:
        user.delete()  # Deletes the user account
        return Response({'success': 'User account deleted successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': f'Failed to delete user: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
def profile(request):
    if not request.user.is_authenticated:
        return Response({"message": "Authentication required."}, status=401)

    auctions = Auction.objects.filter(owner=request.user)

    ducks = Duck.objects.filter(auction__in=auctions).distinct()

    ducks_data = DuckSerializer(ducks, many=True).data

    return Response({
        "user": request.user.username,
        "ducks": ducks_data
    }, status=200)
    
@api_view(['PUT'])
def modify_user(request):
    if not request.user.is_authenticated:
        return Response({"message": "Authentication required."}, status=401)

    user = request.user
    
    username = request.data.get('username')
    email = request.data.get('email')

    if username:
        user.username = username
    if email:
        user.email = email

    if 'password' in request.data:
        user.set_password(request.data['password'])  # Hash the password properly

    user.save()

    return Response({"message": "User updated successfully", "username": user.username, "email": user.email}, status=status.HTTP_200_OK)  
   
@api_view(['POST'])
def spin_duck_api(request):
    """
    API endpoint to spin for a duck and create an associated auction.
    """
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

    ducks = Duck.objects.all()

    rarity_weights = {
        'C': 50,  # Common
        'R': 30,  # Rare
        'SR': 15,  # Super Rare
        'UR': 4,   # Ultra Rare
        'SUR': 1   # Special Ultra Rare
    }

    weighted_ducks = []
    for duck in ducks:
        weighted_ducks.extend([duck] * rarity_weights.get(duck.rarity, 0))

    if not weighted_ducks:
        return Response({'error': 'No ducks available for spinning'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Randomly select a duck
    selected_duck = random.choice(weighted_ducks)

    auction = Auction.objects.create(
        duck=selected_duck,
        starting_price=0.00,  # Initial price if auctioned later
        current_price=0.00,
        end_time=timezone.now() + timedelta(days=7),  # Example: 7-day auction
        owner=request.user  # Assign the duck to the current user
    )

    return Response({
        'duck': {
            'id': selected_duck.id,
            'name': selected_duck.name,
            'rarity': selected_duck.rarity
        },
        'auction': {
            'id': auction.id,
            'end_time': auction.end_time
        }
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
def place_bid_api(request, auction_id):
    """
    API endpoint to place a bid on an auction.
    """
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        auction = Auction.objects.get(id=auction_id)
        player = Player.objects.get(user=request.user)
        bid_amount = float(request.data.get('bid_amount', 0))

        if bid_amount <= auction.current_price or player.currency < bid_amount:
            return Response({'error': 'Invalid bid'}, status=status.HTTP_400_BAD_REQUEST)

        auction.current_price = bid_amount
        auction.highest_bidder = player
        auction.save()

        return Response({'success': 'Bid placed successfully!', 'current_price': auction.current_price}, status=status.HTTP_200_OK)
    except Auction.DoesNotExist:
        return Response({'error': 'Auction not found'}, status=status.HTTP_404_NOT_FOUND)
    except Player.DoesNotExist:
        return Response({'error': 'Player not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def roll_gacha_api(request):
    """
    API endpoint to roll the gacha system and get a reward.
    """
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        player = Player.objects.get(user=request.user)
        if player.currency < 10:
            return Response({'error': 'Not enough currency'}, status=status.HTTP_400_BAD_REQUEST)

        player.currency -= 10  
        player.save()

        # Gacha logic based on rarity probabilities
        roll = random.random()
        if roll < 0.0005:
            rarity = 'SUR'  # Super Ultra Rare
        elif roll < 0.005:
            rarity = 'UR'  # Ultra Rare
        elif roll < 0.05:
            rarity = 'SR'  # Super Rare
        elif roll < 0.40:
            rarity = 'R'   # Rare
        else:
            rarity = 'C'   # Common

        ducks = Duck.objects.filter(rarity=rarity)
        if not ducks.exists():
            return Response({'error': f'No ducks available for rarity {rarity}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        selected_duck = ducks.order_by('?').first()

        auction = Auction.objects.create(
            duck=selected_duck,
            starting_price=0.00,
            current_price=0.00,
            end_time=timezone.now() + timedelta(days=7), 
            owner=request.user
        )

        return Response({
            'result': f'You got a {selected_duck.name} ({selected_duck.get_rarity_display()})!',
            'currency': player.currency,
            'duck': {
                'name': selected_duck.name,
                'rarity': selected_duck.rarity,
                'profession': selected_duck.profession,
                'image': selected_duck.image.url if selected_duck.image else None,
                'auction_id': auction.id,
                'auction_end_time': auction.end_time
            }
        }, status=status.HTTP_200_OK)

    except Player.DoesNotExist:
        return Response({'error': 'Player not found'}, status=status.HTTP_404_NOT_FOUND)

