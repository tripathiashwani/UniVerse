from django.core.cache import cache
from django.http import JsonResponse
from django.core.cache import cache
from time import time
from django.http import HttpResponseForbidden
from rest_framework_simplejwt.authentication import JWTAuthentication
from jwt.exceptions import InvalidTokenError

class ApiUsageTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        header_token = request.META.get('HTTP_AUTHORIZATION', None)
        if header_token is not None and header_token.startswith('Bearer'):
            token = header_token.split('Bearer ')[1]
            jwt_authenticator = JWTAuthentication()
            validated_token = jwt_authenticator.get_validated_token(token)
            user = jwt_authenticator.get_user(validated_token)
                    
            request.user = user 
            user_key = f"api_usage_{request.user.id}"
            usage_count = cache.get(user_key, 0)
            cache.set(user_key, usage_count + 1, timeout=None)  

            response = self.get_response(request)
            return response
        else:
            response = self.get_response(request)
            return response





class RestrictAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        if request.method == 'POST' and not request.user.is_authenticated:
            return HttpResponseForbidden("You must be logged in to make POST requests.")
        restricted_paths = ['/restricted-endpoint/']
        if request.path in restricted_paths:
            return HttpResponseForbidden("This endpoint is restricted.")

        response = self.get_response(request)
        return response





class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.rate_limit = 10  
        self.time_window = 60  

    def __call__(self, request):
       
        user_key = f"rate_limit_{request.user.id}"
        request_history = cache.get(user_key, [])
        
        request_history = [t for t in request_history if time() - t < self.time_window]
        
        if len(request_history) >= self.rate_limit:
            return JsonResponse({"error": "Rate limit exceeded. Try again later."}, status=429)

        
        request_history.append(time())
        cache.set(user_key, request_history, timeout=self.time_window)

        response = self.get_response(request)
        return response
