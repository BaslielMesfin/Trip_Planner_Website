from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

# -------------------------------
# Profile Serializer
# -------------------------------
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio']  # removed profile_picture

# -------------------------------
# User Serializer
# -------------------------------
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        # update nested profile
        profile = instance.profile
        profile.bio = profile_data.get('bio', profile.bio)
        profile.save()
        return instance

# -------------------------------
# Register Serializer
# -------------------------------
class RegisterSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'bio']

    def create(self, validated_data):
        bio = validated_data.pop('bio', '')
        user = User.objects.create_user(**validated_data)
        profile = user.profile
        if bio:
            profile.bio = bio
        profile.save()
        return user
