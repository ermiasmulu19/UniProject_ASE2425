from django.db import models
from django.contrib.auth.models import User
class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currency = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)

    def __str__(self):
        return self.user.username
