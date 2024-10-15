from django.db import models
from django.contrib.auth.models import User

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
    profession = models.CharField(max_length=100)  # Профессия уточки
    image = models.ImageField(upload_to='ducks/', null=True, blank=True)  # Путь для хранения изображений

    def __str__(self):
        return f"{self.name} - {self.get_rarity_display()}"

class Auction(models.Model):
    duck = models.ForeignKey(Duck, on_delete=models.CASCADE)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    end_time = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Auction for {self.duck.name} by {self.owner.username}"
