# # notifications/routing.py
# from django.urls import re_path
# from . import consumers
# from django.urls import path

# websocket_urlpatterns = [
#     path('ws/notifications/', consumers.NotificationConsumer.as_asgi()),
#     re_path(r'ws/notifications/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
#     path('ws/notifications/<str:user_id>/', consumers.NotificationConsumer.as_asgi()),
# ]
