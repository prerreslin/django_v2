from django.contrib.auth.models import User
from rest_framework import serializers

from ..models import Profile
from .user_serializer import UserSerializer




class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        profile = Profile