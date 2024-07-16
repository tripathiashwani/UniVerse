from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, Like, Report
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@receiver(post_save, sender=Post)
def notify_post_created(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'user_{instance.user.id}',
            {
                'type': 'send_notification',
                'message': f'New post created: {instance.title}'
            }
        )

@receiver(post_save, sender=Like)
def notify_post_liked(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'user_{instance.post.user.id}',
            {
                'type': 'send_notification',
                'message': f'Your post was liked by {instance.user.username}'
            }
        )

@receiver(post_save, sender=Report)
def notify_post_reported(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'user_{instance.post.user.id}',
            {
                'type': 'send_notification',
                'message': f'Your post was reported by {instance.user.username}'
            }
        )
