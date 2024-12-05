from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views
# from api.views import register_api,login_api,user_delete_api,spin_duck_api,place_bid_api,roll_gacha_api,user_logout, profile,modify_user

from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
# router.register(r'ducks', DuckViewSet)
# router.register(r'auctions', AuctionViewSet)

urlpatterns = [
    path('home/', views.home_api, name='home'),
    path('admin/', admin.site.urls),
    path('', include(router.urls)), 
    path('register/', register_api, name='register'),
    path('login/', login_api, name='login'),
    path('logout/', user_logout, name='logout'),
    path('roll/', roll_gacha_api, name='roll_gacha'),
    path('profile/', profile, name='profile'),
    path('spin/', spin_duck_api, name='spin'),  
    path('user/delete/', user_delete_api, name='delete_user'),
    path('user/modify/', modify_user, name='userModify'),
    path('bid/<int:auction_id>/', place_bid_api, name='place_bid')
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
