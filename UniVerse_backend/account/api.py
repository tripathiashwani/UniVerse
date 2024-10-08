from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.http import JsonResponse
from notification.utils import create_notification
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .forms import SignupForm, ProfileForm
from .models import User, FriendshipRequest
from .serializers import UserSerializer,FriendshipRequestSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.core.cache import cache
import requests
from rest_framework import status
import openai
from rest_framework_simplejwt.tokens import RefreshToken
from google.oauth2 import id_token
from google.auth.transport import requests
import google_auth_oauthlib.flow
import aiohttp  
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from .secret import *


from UniVerse_backend.middleware import ApiUsageTrackingMiddleware, RateLimitMiddleware



@api_view(['GET'])
def me(request):
    user = request.user
    cached_user = cache.get(f'user_{user.id}')
    
    if not cached_user:
        print('not redis')
        cached_user = UserSerializer(user).data
        cache.set(f'user_{user.id}', cached_user, timeout=60*5)  

    return JsonResponse(cached_user)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = 'success'
    print(data)
    form = SignupForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
    })

    if form.is_valid():
        user = form.save()
        user.is_active = True
        form.save()
        
        print("signup validated in api")


    else:
        message = form.errors.as_json()
    
    print(message)

    return JsonResponse({'message': message})




@api_view(['GET'])
def friends(request, pk):
    cache_key = f'friends_{pk}'
    cached_data = cache.get(cache_key)
    
    if not cached_data:
        user = User.objects.get(pk=pk)
        requests = []
        if user == request.user:
            requests = FriendshipRequest.objects.filter(created_for=request.user, status=FriendshipRequest.SENT)
            requests = FriendshipRequestSerializer(requests, many=True).data

        friends = user.friends.all()
        cached_data = {
            'user': UserSerializer(user).data,
            'friends': UserSerializer(friends, many=True).data,
            'requests': requests
        }
        cache.set(cache_key, cached_data, timeout=60*5)  

    return JsonResponse(cached_data, safe=False)



    
@api_view(['POST'])
def send_friendship_request(request, pk):
    user = User.objects.get(pk=pk)
    check1 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user)
    check2 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user)
    
    if not check1 and not check2:
        friendrequest = FriendshipRequest.objects.create(created_for=user, created_by=request.user)
        create_notification(request, 'new_friendrequest', friendrequest_id=friendrequest.id)
        cache.delete(f'friends_{request.user.id}') 
        cache.delete(f'friends_{user.id}')          
        return JsonResponse({'message': 'friendship request created'})
    else:
        return JsonResponse({'message': 'request already sent'})



@api_view(['POST'])
def handle_request(request, pk, status):
    user = User.objects.get(pk=pk)
    friendship_request = FriendshipRequest.objects.filter(created_for=request.user).get(created_by=user)
    friendship_request.status = status
    friendship_request.save()
    user.friends.add(request.user)
    user.friends_count += 1
    user.save()
    request_user = request.user
    request_user.friends_count += 1
    request_user.save()
    create_notification(request, 'accepted_friendrequest', friendrequest_id=friendship_request.id)
    
    cache.delete(f'friends_{request.user.id}')  
    cache.delete(f'friends_{user.id}')         
    
    return JsonResponse({'message': 'friendship request updated'})



@api_view(['GET'])
def my_friendship_suggestions(request):
    permission_classes = [IsAuthenticated]
    cache_key = f'friendship_suggestions_{request.user.id}'
    suggestions = cache.get(cache_key)
    
    if not suggestions:
        try:
            suggestions = UserSerializer(request.user.people_you_may_know.all(), many=True).data
            cache.set(cache_key, suggestions, timeout=60*5) 
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse(suggestions, safe=False)





class ProfilePictureUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request, *args, **kwargs):
        user_profile = request.user
        serializer = UserSerializer(user_profile, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            cache.delete(f'user_{request.user.id}') 
            return Response(serializer.data)
        
        return Response(serializer.errors, status=400)
    



@authentication_classes([])
@permission_classes([])
class ChatbotView(APIView):
    def post(self, request):
        user_message = request.data.get("message")
        openai.api_key = OPENAI_API_KEY
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=150,
                temperature=0.7,
            )
            bot_reply = response['choices'][0]['message']['content']
            return Response({"response": bot_reply}, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }




class GoogleLoginView(APIView):
    def post(self, request, *args, **kwargs):
        
        token = request.data.get('token')
        print(token)
        try:
            
            idinfo = id_token.verify_oauth2_token(
                token,
                google_requests.Request(),
                google_auth_key
            )

            
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            email = idinfo.get('email')
            user = User.objects.filter(email=email).first()
            
            if not user:
                user = User.objects.create_user(name=email, email=email, password=None)

            tokens = get_tokens_for_user(user)
            return Response({'msg': 'Login success', 'tokens': tokens}, status=status.HTTP_200_OK)

        except ValueError as e:
            print(f"Token verification failed: {e}")
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


