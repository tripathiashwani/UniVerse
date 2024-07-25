from rest_framework import serializers
from account.models import User
# from account.serializers import UserSerializer
from chat.models import ConversationMessage, Conversation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['name','avatar']

class MessageSerializer(serializers.ModelSerializer):
    sender=UserSerializer()
    class Meta:
        model = ConversationMessage
        fields = ['id', 'message', 'sender', 'created_at']

class ConversationSerializer(serializers.ModelSerializer):
    messages=MessageSerializer(many=True,read_only=True)
    class Meta:
        model = Conversation
        fields = [ 'messages']