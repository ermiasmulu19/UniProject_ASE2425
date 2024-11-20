from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
def get_default_seller():
    try:
        user = User.objects.get(username='default_user')
    except User.DoesNotExist:
        user = User.objects.create(username='default_user')
    player, created = Player.objects.get_or_create(user=user)
    return player.id

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currency = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)

    def __str__(self):
        return self.user.username
class Duck(models.Model):
    RARITY_CHOICES = [
        ('C', 'Common'),
        ('R', 'Rare'),
        ('SR', 'SuperRare'),
        ('UR', 'UltraRare'),
        ('SUR', 'SuperUltraRare'),
    ]

    name = models.CharField(max_length=100)
    rarity = models.CharField(max_length=3, choices=RARITY_CHOICES)
    profession = models.CharField(max_length=100) 
    image = models.ImageField(upload_to='ducks/', null=True, blank=True)  

    def __str__(self):
        return f"{self.name} - {self.get_rarity_display()}"

class Auction(models.Model):
    duck = models.ForeignKey(Duck, on_delete=models.CASCADE)
    seller = models.ForeignKey(Player, related_name='auctions', on_delete=models.CASCADE, default=get_default_seller)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    highest_bidder = models.ForeignKey(Player, related_name='bids', on_delete=models.SET_NULL, null=True, blank=True)
    end_time = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def is_active(self):
        return self.end_time > timezone.now()

    def __str__(self):
        return f"Auction for {self.duck.name} by {self.owner.username}"
