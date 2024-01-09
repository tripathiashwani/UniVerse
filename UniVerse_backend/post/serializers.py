from rest_framework import serializers
from .models import Post ,Postattachments
from account.serializers import UserSerializer



class PostAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postattachments
        fields = ('id', 'img')


class PostSerializer(serializers.ModelSerializer):
    created_by=UserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ('id', 'body', 'created_by', 'created_at_formatted', 'attachments')

