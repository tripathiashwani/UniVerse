# urls.py
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from account.views import LoginView 
from . import api 
from .api import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('me/', api.me, name='me'),
    path('signup/', api.signup, name='signup'),
    path('login/', LoginView.as_view(), name='token_obtain'),
    path('login1/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('profile_picture/', ProfilePictureUpdateView.as_view(), name='profile-picture-update'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('friends/<uuid:pk>/request/', api.send_friendship_request, name='send_friendship_request'),
    path('friends/<uuid:pk>/', api.friends, name='friends'),
    path('friends/<uuid:pk>/<str:status>/', api.handle_request, name='handle_request'),
    path('friends/suggested/', api.my_friendship_suggestions, name='my_friendship_suggestions'),
    path('chatbot/', ChatbotView.as_view(), name='chatbot'),
    path('google_login/', GoogleLoginView.as_view(), name='google_login'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

