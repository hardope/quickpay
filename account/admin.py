from django.contrib import admin

# Register your models here.
from .models import UserProfile, Transaction, OTP

admin.site.register(UserProfile)
admin.site.register(Transaction)
admin.site.register(OTP)