from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Player

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'username']
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }