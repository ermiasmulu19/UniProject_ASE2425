import sys

from .serializers import AuctionSerializer, DuckSerializer
from rest_framework.permissions import IsAuthenticated
from decimal import Decimal
from .models import Player,Duck

# from api.models import Player
sys.path.append('/home/em/unipi/UniProject_ASE2425/gacha_game/')


from django.utils import timezone

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

# from api.serializers import DuckSerializer


from .models import Auction
# from duckService.duck.models import Duck
# from player.models import Player

# import random
# from rest_framework.authtoken.models import Token
# from django.contrib.auth.models import User
# from rest_framework.permissions import IsAuthenticated
# from django.contrib.auth import logout
# from django.contrib.auth import authenticate
# from rest_framework.permissions import AllowAny


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
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_history(request):
    """
    API endpoint to view the player's transaction history.
    """
    try:
        player = Player.objects.get(user=request.user)
        bids = Auction.objects.filter(highest_bidder=player)
        auctions = Auction.objects.filter(seller=player)

        bid_data = AuctionSerializer(bids, many=True).data
        auction_data = AuctionSerializer(auctions, many=True).data

        return Response({
            "player": player.user.username,
            "bids": bid_data,
            "auctions": auction_data,
        }, status=status.HTTP_200_OK)
    except Player.DoesNotExist:
        return Response({'error': 'Player not found'}, status=status.HTTP_404_NOT_FOUND)
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def buy_currency(request):
    """
    API endpoint to buy in-game currency.
    """
    amount = request.data.get('amount')
    if not amount or float(amount) <= 0:
        return Response({'error': 'Invalid amount'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        player = Player.objects.get(user=request.user)
        player.currency += Decimal(amount)
        player.save()

        return Response({'success': 'Currency purchased successfully', 'new_balance': player.currency}, status=status.HTTP_200_OK)
    except Player.DoesNotExist:
        return Response({'error': 'Player not found'}, status=status.HTTP_404_NOT_FOUND)
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_gacha_collection(request):
    """
    API endpoint to retrieve the player's gacha collection.
    """
    try:
        player = Player.objects.get(user=request.user)
        my_ducks = Duck.objects.filter(auction__seller=player).distinct()
        ducks_data = DuckSerializer(my_ducks, many=True).data

        return Response({
            "player": player.user.username,
            "gacha_collection": ducks_data,
        }, status=status.HTTP_200_OK)
    except Player.DoesNotExist:
        return Response({'error': 'Player not found'}, status=status.HTTP_404_NOT_FOUND)