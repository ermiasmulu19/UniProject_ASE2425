from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views
from api.views import place_bid, register, roll_gacha, user_delete, user_login, user_logout, profile, modify_user, DuckViewSet, AuctionViewSet, spin_duck

from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'ducks', DuckViewSet)
router.register(r'auctions', AuctionViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('', include(router.urls)), 
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('roll/', roll_gacha, name='roll_gacha'),
    path('profile/', profile, name='profile'),
    path('spin/', spin_duck, name='spin'),  
    path('user/delete', user_delete, name='delete_user'),
    path('user/modify/', modify_user, name='userModify'),
    path('bid/<int:auction_id>/', place_bid, name='place_bid'),
    path('duck/<int:duck_id>/', views.duck_detail, name='duck_detail'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
