from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import register, user_delete, user_login, user_logout, profile, DuckViewSet, AuctionViewSet, spin_duck  # Импортируйте необходимые классы

router = DefaultRouter()
router.register(r'ducks', DuckViewSet)
router.register(r'auctions', AuctionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),  # Включаем маршруты API
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('spin/', spin_duck, name='spin'),  # Новый маршрут для спина
    path('user/delete', user_delete, name='delete_user')
]
