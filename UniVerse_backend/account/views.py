from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from account.serializers import loginSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class LoginView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=loginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)
            print(user)
            if user is not None:
                tokens=get_tokens_for_user(user)
                return Response({'msg':'login success','tokens':tokens},status=status.HTTP_200_OK)
            else :
               return  Response({'erros':{'non_field_errors':['email or password is invalid']}},status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
    