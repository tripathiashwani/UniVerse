from django.urls import path

from .api import StripeCheckoutView  
urlpatterns = [
    path('', StripeCheckoutView.as_view()),
]