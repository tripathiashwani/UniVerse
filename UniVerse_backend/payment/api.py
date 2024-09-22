from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from django.http import JsonResponse
from .secret import *
import stripe

stripe.api_key = stripe_secret_key
class StripeCheckoutView(APIView):
    def post(self, request):
        try:
            
            email = request.data.get('email')
            
            checkout_session = stripe.checkout.Session.create(
                customer_email=email,  
                line_items=[
                    {
                        'price': product_id,
                        'quantity': 1,
                    },
                ],
                payment_method_types=['card'],
                mode='payment',
                success_url=settings.SITE_URL + "?success=true",
                cancel_url=settings.SITE_URL + "?canceled=true",
            )
            # print(checkout_session)
            return JsonResponse({'url':checkout_session.url})
        except Exception as e:
            # print(str(e))
            return Response(
                {'error': 'Something went wrong when creating stripe checkout session'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
