from rest_framework import serializers
from account.models import User
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class loginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=User
        fields=['email','password']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['email','name','id']
