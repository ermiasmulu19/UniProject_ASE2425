"""
URL configuration for userservice project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users.views import admin_view_all_gachas, create_gacha, delete_gacha, modify_user, update_gacha, user_delete_api,register_api,login_api



urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/modify/', modify_user, name='userModify'),
    path('user/delete', user_delete_api, name='delete_user'),
    path('register/', register_api, name='register'),
    path('login/', login_api, name='login'),
    # admin gacha managment 
    path('manag/duck/create/', create_gacha, name='create_gacha'),
    path('manag/duck/<int:gacha_id>/update/', update_gacha, name='update_gacha'),
    path('manag/duck/<int:gacha_id>/delete/', delete_gacha, name='delete_gacha'),
    path('manag/duck/all/', admin_view_all_gachas, name='admin_view_all_gachas'),
]
