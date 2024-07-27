from django.db import models
from account.models import User
# Create your models here.

class Stock(models.Model):
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    change = models.FloatField()
    percent_change = models.FloatField()
    volume = models.FloatField()
    market_cap = models.FloatField()
    currency = models.CharField(max_length=10)
    exchange = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.symbol
    

class Groups(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name='group_members')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    stock= models.ForeignKey(Stock, on_delete=models.CASCADE ,null=True, blank=True, related_name='stock_group' )
    is_active = models.BooleanField(default=True)
    average_profit = models.FloatField(default=0)
    total_investment = models.FloatField(default=0)
    total_value = models.FloatField(default=0)
    total_gain = models.FloatField(default=0)
    total_loss = models.FloatField(default=0)
    total_stock = models.FloatField(default=0)

    def __str__(self):
        return self.name

    def __str__(self):
        return self.name