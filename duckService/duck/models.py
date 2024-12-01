from django.db import models

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