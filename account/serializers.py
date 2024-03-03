from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    ValidationError,
    EmailField)
from rest_framework import serializers

from comms.activation import send_activation_mail
from .models import UserProfile as User
from django.core import exceptions
import django.contrib.auth.password_validation as validators


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'wallet_balance',
        ]
        extra_kwargs = {'password': {'write_only': True,
                                     'required': True}, 'email': {'required': True}}

    def create(self, validated_data):

        user = User.objects.create_user(**validated_data)
        user.is_active = False
        user.save()
        try:
            send_activation_mail(user)
        except:
            pass
        return user

    def validate(self, data):

        if self.context['request'].method == 'POST':
            if User.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError(
                    {'email': 'Email already exists'})

        if data.get('password', False):
            try:
                validators.validate_password(data['password'])
            except exceptions.ValidationError as e:
                raise serializers.ValidationError(
                    {'password': list(e.messages)})

        if data.get('is_superuser', False):
            raise serializers.ValidationError(
                {'is_superuser': 'You cannot create a superuser'})
        if data.get('is_staff', False):
            raise serializers.ValidationError(
                {'is_staff': 'You cannot create a staff'})
        if data.get('is_active', False):
            raise serializers.ValidationError(
                {'is_active': 'You cannot create an active user'})
        if data.get('wallet_balance', 0) != 0:
            raise serializers.ValidationError(
                {'wallet_balance': 'You cannot create a user with a wallet balance'})
        return data

class EmailResetSerializer(Serializer):
    """Email reset serializer"""
    email = EmailField()
