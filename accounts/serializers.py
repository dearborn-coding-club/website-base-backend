from rest_framework import serializers
from .models import Profile, DCCUser


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'role', 'phone_number', 'email', 'address', 'about_me', 'leetcode_username']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = DCCUser
        fields = ['id', 'profile', 'password', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'bio', 'date_joined', 'bio', 'birthdate']
