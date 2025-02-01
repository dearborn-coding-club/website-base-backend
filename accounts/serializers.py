from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'role', 'phone_number', 'email', 'address', 'about_me', 'leetcode_username']