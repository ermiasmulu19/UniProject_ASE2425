import random

from rest_framework import viewsets
from .models import Duck, Auction
from .serializers import DuckSerializer, AuctionSerializer

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.utils.timezone import now



class DuckViewSet(viewsets.ModelViewSet):
    queryset = Duck.objects.all()
    serializer_class = DuckSerializer

class AuctionViewSet(viewsets.ModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer


# Регистрация нового пользователя
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('profile')  # Переход к профилю после регистрации
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# Вход пользователя
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')  # Переход к профилю после входа
    return render(request, 'login.html')

# Выход пользователя
def user_logout(request):
    logout(request)
    return redirect('login')  # Переход к странице входа
    
@login_required
def profile(request):
    # Fetch all auctions for the logged-in user
    user_auctions = Auction.objects.filter(owner=request.user)

    # Extract the ducks from those auctions
    ducks = [auction.duck for auction in user_auctions]

    return render(request, 'profile.html', {'ducks': ducks, 'user': request.user})



@login_required
def spin_duck(request):
    if request.method == 'POST':
        # Fetch all ducks
        ducks = Duck.objects.all()

        # Define rarity weights
        rarity_weights = {
            'C': 50,  # 50% chance
            'R': 30,  # 30% chance
            'SR': 15,  # 15% chance
            'UR': 4,   # 4% chance
            'SUR': 1    # 1% chance
        }

        # Build a weighted list of ducks
        weighted_ducks = []
        for duck in ducks:
            weighted_ducks.extend([duck] * rarity_weights[duck.rarity])

        # Randomly select a duck
        selected_duck = random.choice(weighted_ducks)

        # Create an Auction record to represent ownership
        auction = Auction.objects.create(
            duck=selected_duck,
            starting_price=0.00,  # Initial price if auctioned later
            current_price=0.00,
            end_time=now() + timedelta(days=7),  # Example: 7-day auction
            owner=request.user  # Assign the duck to the current user
        )

        # Render the result page
        return render(request, 'spin_result.html', {'duck': selected_duck})

    return render(request, 'spin.html')
