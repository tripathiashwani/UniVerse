import logging
import jwt  # Import the PyJWT library
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from jwt.exceptions import InvalidTokenError


logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the Authorization header
        header_token = request.META.get('HTTP_AUTHORIZATION', None)
        # print(header_token, "inside logging middleware L")

        if header_token is not None and header_token.startswith('Bearer '):
            token = header_token.split('Bearer ')[1]
            
            try:
                # Attempt to decode the JWT token
                jwt_authenticator = JWTAuthentication()
                validated_token = jwt_authenticator.get_validated_token(token)
                user = jwt_authenticator.get_user(validated_token)
                
                request.user = user  # Set the correct user from the JWT
                # print(request.user, "Authenticated user inside middleware")
            except InvalidTokenError:
                logger.error("Invalid JWT token detected")
                request.user = None  # Set user as None if the token is invalid
            except AuthenticationFailed as e:
                logger.error(f"JWT Authentication failed: {str(e)}")
                request.user = None  # Set user as None if authentication fails
        else:
            print("No valid JWT token found")

        # Proceed with the request and response
        response = self.get_response(request)
        return response


class OrganizationMiddleware(object):

  def process_view(self, request, view_func, view_args, view_kwargs):
    print(request.user,"inside organization middleware O0000000000000000000000000000000000000")
    header_token = request.META.get('HTTP_AUTHORIZATION', None)
    if header_token is not None:
      try:
       token = sub('Token ', '', header_token)
       token_obj = Token.objects.get(key = token)
       request.user = token_obj.user
      except Token.DoesNotExist:
        pass
    #This is now the correct user
    print (request.user)
