from django.utils import timezone

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from duckservice.duck.serializers import DuckSerializer

# from api.serializers import DuckSerializer
from .models import Duck, Auction, Player
from datetime import timedelta
import random
from rest_framework.permissions import AllowAny


import random

@api_view(['GET'])
@permission_classes([AllowAny])
def system_gacha_info(request, gacha_id):
    """
    API endpoint to retrieve detailed info of a system gacha.
    """
    try:
        duck = Duck.objects.get(id=gacha_id)
        return Response(DuckSerializer(duck).data, status=status.HTTP_200_OK)
    except Duck.DoesNotExist:
        return Response({'error': 'Gacha not found in the system'}, status=status.HTTP_404_NOT_FOUND)
    
    
def gacha_info(request, gacha_id):
    """
    API endpoint to retrieve detailed info of a gacha owned by the player.
    """
    try:
        duck = Duck.objects.get(id=gacha_id)
        return Response(DuckSerializer(duck).data, status=status.HTTP_200_OK)
    except Duck.DoesNotExist:
        return Response({'error': 'Gacha not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([AllowAny])
def system_gacha_collection(request):
    """
    API endpoint to retrieve the system-wide gacha collection.
    """
    ducks = Duck.objects.all()
    ducks_data = DuckSerializer(ducks, many=True).data

    return Response({"system_gacha_collection": ducks_data}, status=status.HTTP_200_OK)


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