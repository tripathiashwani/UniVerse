from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.http import HttpResponse
from . import api

print('reached at url.py page login')
urlpatterns = [
    path('signup/',api.signup, name='signup'),
    path('login/',TokenObtainPairView.as_view(),name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
