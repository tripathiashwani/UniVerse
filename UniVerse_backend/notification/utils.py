from .models import Notification

from post.models import Post
from account.models import FriendshipRequest

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification
# create_notification(request, 'post_like', 'lskjf-j12l3-jlas-jdfa', 'lskjf-j12l3-jlas-jdfa')


def create_notification(request, type_of_notification, post_id=None, friendrequest_id=None):
    created_for = None

    if type_of_notification == 'post_like':
        body = f'{request.user.name} liked one of your posts!'
        post = Post.objects.get(pk=post_id)
        created_for = post.created_by
    elif type_of_notification == 'post_comment':
        body = f'{request.user.name} commented on one of your posts!'
        post = Post.objects.get(pk=post_id)
        created_for = post.created_by
    elif type_of_notification == 'new_friendrequest':
        friendrequest = FriendshipRequest.objects.get(pk=friendrequest_id)
        created_for = friendrequest.created_for
        body = f'{request.user.name} sent you a friend request!'
    elif type_of_notification == 'accepted_friendrequest':
        friendrequest = FriendshipRequest.objects.get(pk=friendrequest_id)
        created_for = friendrequest.created_for
        body = f'{request.user.name} accepted your friend request!'
    elif type_of_notification == 'rejected_friendrequest':
        friendrequest = FriendshipRequest.objects.get(pk=friendrequest_id)
        created_for = friendrequest.created_for
        body = f'{request.user.name} rejected your friend request!'

    notification = Notification.objects.create(
        body=body,
        type_of_notification=type_of_notification,
        created_by=request.user,
        post_id=post_id,
        created_for=created_for
    )

    return notification


# def create_notification(request, notification_type, **kwargs):
    # user = request.user
    # recipient = kwargs.get('friendrequest_id').created_for

    # notification = Notification.objects.create(
    #     body=f"You have a new {notification_type.replace('_', ' ')}",
    #     type_of_notification=notification_type,
    #     created_by=user,
    #     created_for=recipient,
    # )

    # # Send a real-time notification
    # channel_layer = get_channel_layer()
    # async_to_sync(channel_layer.group_send)(
    #     f'notifications_{recipient.id}',
    #     {
    #         'type': 'notification_message',
    #         'message': notification.body,
    #     }
    # )
    # return notification