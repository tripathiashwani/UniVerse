from django.contrib import admin

from .models import Post, Postattachments


admin.site.register(Post)
admin.site.register(Postattachments)