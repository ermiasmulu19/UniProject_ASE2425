from django.utils import timezone

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from .models import Duck, Auction, Player


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
