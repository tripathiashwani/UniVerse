
from django.contrib import admin
from django.urls import path,include
from graphene_django.views import GraphQLView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("account.urls")),
    path("api/posts/", include("post.urls")),
    path("api/search/", include("search.urls")),
    path("api/chats/", include("chat.urls")),
    path('api/notifications/', include('notification.urls')),
    path('api/payment/', include('payment.urls')),
    path('graphql/', GraphQLView.as_view(graphiql=True)),
]
