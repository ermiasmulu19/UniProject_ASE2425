from django.utils import timezone

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status


from .models import Auction

from .models import Player

def secure_place_bid_api(request, auction_id):
    """
    Secure API endpoint to place a bid on an auction.
    """
    try:
        auction = Auction.objects.get(id=auction_id)
        if not auction.is_active():
            return Response({'error': 'Auction has expired'}, status=status.HTTP_400_BAD_REQUEST)

        player = Player.objects.get(user=request.user)
        bid_amount = float(request.data.get('bid_amount', 0))

        if bid_amount <= auction.current_price:
            return Response({'error': 'Bid amount must be greater than the current price'}, status=status.HTTP_400_BAD_REQUEST)

        if player.currency < bid_amount:
            return Response({'error': 'Insufficient currency'}, status=status.HTTP_400_BAD_REQUEST)

        auction.current_price = bid_amount
        auction.highest_bidder = player
        auction.save()

        return Response({'success': 'Bid placed successfully!', 'current_price': auction.current_price}, status=status.HTTP_200_OK)
    except Auction.DoesNotExist:
        return Response({'error': 'Auction not found'}, status=status.HTTP_404_NOT_FOUND)
    except Player.DoesNotExist:
        return Response({'error': 'Player not found'}, status=status.HTTP_404_NOT_FOUND)
