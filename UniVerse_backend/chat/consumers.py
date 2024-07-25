from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from django.contrib.auth import get_user_model
from chat.models import Conversation, ConversationMessage

from account.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_email = text_data_json['sender']
        sent_to_id = text_data_json['sent_to']
        
        try:
            sender = await database_sync_to_async(User.objects.get)(email=sender_email)
            sent_to = await database_sync_to_async(User.objects.get)(id=sent_to_id)
            sender_name = sender.name
            print(f"Sender: {sender.name}")
            print(f"Sent To: {sent_to}")

            # Fetch or create the conversation
            conversation, created = await database_sync_to_async(Conversation.objects.get_or_create)(
                room=self.room_name
            )

            # Add users to the conversation if it's newly created
            if created:
                await database_sync_to_async(conversation.users.add)(sender, sent_to)

            # Save the message to the database
            message_obj =  await database_sync_to_async(ConversationMessage.objects.create)(
                conversation=conversation,
                sender=sender,
                sent_to=sent_to,
                message=message
            )

            message_data = {
            'message': message_obj.message,
            'sender': str(message_obj.sender.name),
            'sent_to': str(message_obj.sent_to),
            'created_at': message_obj.created_at_formatted()
            }
            # Broadcast the message to the group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message_data
                }
            )

        except User.DoesNotExist:
            # Handle user not found
            pass

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
        }))
