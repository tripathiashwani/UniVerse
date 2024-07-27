# myapp/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from .models import Post, Like
from account.models import User
from notification.utils import create_notification
from rest_framework.response import Response
from .models import Post, Like, Report, Comment
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer


@shared_task
def handle_like(post_id, user_id, action):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=user_id)
    
    if action == 'like':
        # Perform actions for liking a post
        post.likes_count += 1
        post.save()
        # Example notification (you can add real notification logic here)
        # notification = create_notification(request, 'post_like', post_id=post.id)
    elif action == 'unlike':
        # Perform actions for unliking a post
        post.likes_count -= 1
        post.save()
