from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from account.views import LoginView 
from .api import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('get_room_chat/<str:room>/', Get_Room  , name='friends'),
]