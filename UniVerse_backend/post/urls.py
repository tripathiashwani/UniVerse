from django.urls import path
from . import api
print("reached at post.url")
urlpatterns = [
    path('', api.post_list_friends, name='post_list'),
    path('create/', api.create_post, name='create_post'),
    path('profile/<uuid:id>/', api.post_list_profile, name='profile_list'),
    path('<uuid:pk>/like/', api.post_like, name='post_like'),
    path('<uuid:pk>/report/', api.post_report, name='post_like'),
    path('<uuid:pk>/delete/', api.post_delete, name='post_like'),
    path('<uuid:pk>/',api.post_detail,name='post_view'),
    path('<uuid:pk>/comment/', api.post_create_comment, name='post_create_comment'),
]