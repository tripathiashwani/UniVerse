from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.http import JsonResponse
from account.models import User
# Your code here
from notification.utils import create_notification
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from chat.models import ConversationMessage, Conversation
from chat.serializers import MessageSerializer,ConversationSerializer

# @api_view(['GET'])
# def Get_Messages(request):
#     messages = Message.objects.all()
#     serializer = MessageSerializer(messages, many=True)
#     return JsonResponse(serializer.data, safe=False)

def create_message(message, sender, room_name):
    conversation, created = Conversation.objects.get_or_create(room=room_name)
    user = User.objects.get(name=sender)  # Or use a different method to get the user

    ConversationMessage.objects.create(
        conversation=conversation,
        body=message,
        sent_to=conversation.users.exclude(name=sender).first(),  # Assuming the conversation has only 2 users
        created_by=user,
    )

@api_view(['GET'])
def Get_Room(request, room):
    messages = Conversation.objects.filter(room=room)  # Use filter instead of get
    print(messages)
    serializer = ConversationSerializer(messages, many=True)
    print(serializer.data)
    return JsonResponse(serializer.data[0], safe=False)