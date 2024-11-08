import random

from django.http import HttpResponseForbidden, JsonResponse
from rest_framework import viewsets
from .models import Duck, Auction
from .serializers import DuckSerializer, AuctionSerializer

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods  # Ensure this line is present


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
    
def profile(request):
    # Получаем аукционы пользователя
    auctions = Auction.objects.filter(owner=request.user)
    # Получаем уникальные уточки из аукционов
    ducks = Duck.objects.filter(auction__in=auctions).distinct()
    return render(request, 'profile.html', {'ducks': ducks, 'user': request.user})
@require_http_methods(["GET"])
def user_delete(request):
    if request.method == 'GET':
        user = request.user

        if user.is_authenticated:
            print('aleeeeeeeeeeeeeeee')
            user.delete()
            logout(request) 
            
            return redirect('profile')
    return redirect('login') 

        
    
    
def spin_duck(request):
    if request.method == 'POST':
        # Получаем все уточки
        ducks = Duck.objects.all()

        # Определяем шансы на выпадение в зависимости от редкости
        rarity_weights = {
            'C': 50,  # 50% шанс
            'R': 30,  # 30% шанс
            'SR': 15,  # 15% шанс
            'UR': 4,   # 4% шанс
            'SUR': 1    # 1% шанс
        }

        # Создаем список, который будет включать уточек с учетом редкости
        weighted_ducks = []
        for duck in ducks:
            weighted_ducks.extend([duck] * rarity_weights[duck.rarity])

        # Выбираем случайную уточку
        selected_duck = random.choice(weighted_ducks)

        return render(request, 'spin_result.html', {'duck': selected_duck})

    return render(request, 'spin.html')
