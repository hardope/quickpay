from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
import random

class UserProfile(User):

     wallet_balance = models.FloatField(default=0.0)

     def __str__(self):
          return self.username
     
class Transaction(models.Model):

     transaction_types = (
          ('credit', 'Credit'),
          ('debit', 'Debit')
     )

     user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
     id = models.UUIDField(default=uuid4, editable=False, unique=True, primary_key=True)
     amount = models.FloatField()
     transaction_type = models.CharField(max_length=10, choices=transaction_types, blank=False)
     created_at = models.DateTimeField(auto_now_add=True)
     additional_data = models.CharField(max_length=100, blank=True)

     def __str__(self):
          return self.transaction_id

class OTP(models.Model):

     purpose_types = (
          ('registration', 'Registration'),
          ('password_reset', 'Password Reset'),
          ('phone_verification', 'Phone Verification'),
          ('email_verification', 'Email Verification')
     )

     user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
     code = models.IntegerField(default=random.randint(100000, 999999))
     created_at = models.DateTimeField(auto_now_add=True)
     purpose = models.CharField(max_length=30, choices=purpose_types, blank=False)
     additional_data = models.CharField(max_length=100, blank=True)