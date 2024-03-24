from django.db import models
from django.utils.timesince import timesince
import uuid
from account.models import User


class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(User, related_name='reports', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)
    
    def created_at_formatted(self):
       return timesince(self.created_at)

class Postattachments(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    img=models.ImageField(upload_to='post_attachments')
    created_by=models.ForeignKey(User,related_name='post_attachments',on_delete=models.CASCADE)


class Post(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    body=models.TextField(blank=True,null=True)
    # attachments=models.ManyToManyField(Postattachments,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    likes = models.ManyToManyField(Like, blank=True)
    likes_count = models.IntegerField(default=0)
    reports = models.ManyToManyField(Report, blank=True)
    reports_count = models.IntegerField(default=0)


    # class Meta:
    #     ordering=('-created_at') 


    def created_at_formatted(self):
        return timesince(self.created_at)
    

