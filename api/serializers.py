from rest_framework import serializers
from .models import Duck, Auction

class DuckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Duck
        fields = '__all__'

class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = '__all__'
