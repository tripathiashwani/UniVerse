from django.urls import path
from . import api
print("reached at post.url")
urlpatterns = [
    path('', api.post_list, name='post_list'),
    path('create/', api.create_post, name='create_post'),
    path('profile/<uuid:id>/', api.profile_list, name='profile_list'),
    path('<uuid:pk>/like/', api.post_like, name='post_like'),
    path('<uuid:pk>/report/', api.post_report, name='post_like'),
    path('<uuid:pk>/delete/', api.post_delete, name='post_like'),
]