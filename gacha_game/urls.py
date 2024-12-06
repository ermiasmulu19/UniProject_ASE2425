from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views
from api.views import register_api,login_api,user_delete_api,spin_duck_api,roll_gacha_api,user_logout, profile,modify_user
from api.views import my_gacha_collection, gacha_info, system_gacha_collection, system_gacha_info, buy_currency,transaction_history, secure_place_bid_api
from api.views import create_gacha,update_gacha,delete_gacha,admin_view_all_gachas
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
# router.register(r'ducks', DuckViewSet)
# router.register(r'auctions', AuctionViewSet)

urlpatterns = [
    path('home/', views.home_api, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)), 
    path('register/', register_api, name='register'),
    path('login/', login_api, name='login'),
    path('logout/', user_logout, name='logout'),
    path('roll/', roll_gacha_api, name='roll_gacha'),
    path('profile/', profile, name='profile'),
    path('spin/', spin_duck_api, name='spin'),  
    path('user/delete/', user_delete_api, name='delete_user'),
    path('user/modify/', modify_user, name='userModify'),
    # path('bid/<int:auction_id>/', place_bid_api, name='place_bid'),
    path('my-collection/', my_gacha_collection, name='my_gacha_collection'),
    path('gacha-info/<int:gacha_id>/', gacha_info, name='gacha_info'),
    path('system-collection/', system_gacha_collection, name='system_gacha_collection'),
    path('system-gacha-info/<int:gacha_id>/', system_gacha_info, name='system_gacha_info'),
    path('buy_currency/', buy_currency, name='buy_currency'),
    path('transactions/', transaction_history, name='transaction_history'),
    path('secure-bid/<int:auction_id>/', secure_place_bid_api, name='secure_place_bid'),
    path('manag/duck/create/', create_gacha, name='create_gacha'),
    path('manag/duck/<int:gacha_id>/update/', update_gacha, name='update_gacha'),
    path('manag/duck/<int:gacha_id>/delete/', delete_gacha, name='delete_gacha'),
    path('manag/duck/all/', admin_view_all_gachas, name='admin_view_all_gachas'),
    # path('admin/logout/', admin_logout, name='admin_logout'),
]


urlpatterns += [
    
]
# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
