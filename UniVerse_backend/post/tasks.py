# myapp/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from .models import Post, Like
from account.models import User
from notification.utils import create_notification , create_like_notification
from rest_framework.response import Response
from .models import Post, Like, Report, Comment
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer


@shared_task
def handle_like(pk, created_by, user_name,action):
    post = Post.objects.get(pk=pk)
    if action == 'like':
        userinstance = User.objects.get(email=created_by)
        like = Like.objects.create(created_by=userinstance)
        post = Post.objects.get(pk=pk)
        post.likes_count = post.likes_count + 1
        post.likes.add(like)
        post.save()
        notification = create_like_notification(user_name, pk, created_by)
    elif action == 'dislike':
        userinstance = User.objects.get(email=created_by)
        like = post.likes.filter(created_by=userinstance)
        like.delete()
        post = Post.objects.get(pk=pk)
        post.likes_count = post.likes_count -1
        post.save()
