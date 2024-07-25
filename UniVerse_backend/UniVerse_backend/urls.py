
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("account.urls")),
    path("api/posts/", include("post.urls")),
    path("api/search/", include("search.urls")),
    path("api/chats/", include("chat.urls")),
    path('api/notifications/', include('notification.urls')),
]
