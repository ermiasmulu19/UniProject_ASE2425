from django.contrib import admin
from .models import Duck, Auction

@admin.register(Duck)
class DuckAdmin(admin.ModelAdmin):
    list_display = ('name', 'rarity', 'profession')

@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ('duck', 'starting_price', 'current_price', 'end_time', 'owner')
