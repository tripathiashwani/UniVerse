import graphene
from graphene_django.types import DjangoObjectType
from chat.models import Conversation, ConversationMessage
from account.models import User

class UserType(DjangoObjectType):
    class Meta:
        model = User

class ConversationMessageType(DjangoObjectType):
    class Meta:
        model = ConversationMessage

class ConversationType(DjangoObjectType):
    class Meta:
        model = Conversation

class Query(graphene.ObjectType):
    all_conversations = graphene.List(ConversationType)
    conversation = graphene.Field(ConversationType, room=graphene.String(required=True))

    def resolve_all_conversations(self, info, **kwargs):
        return Conversation.objects.all()

    def resolve_conversation(self, info, room):
        try:
            return Conversation.objects.get(room=room)
        except Conversation.DoesNotExist:
            return None

schema = graphene.Schema(query=Query)
