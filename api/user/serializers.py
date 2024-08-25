from django.db import transaction
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from api.user.models import User, SocialKindChoices, Profile, ProfileImage


class UserSocialLoginSerializer(serializers.Serializer):
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    code = serializers.CharField(write_only=True)
    email = serializers.CharField(write_only=True)
    social_type = serializers.CharField(write_only=True)

    def validate(self, attrs):
        code = attrs['code']
        email = attrs['email']
        social_type = attrs['social_type']

        if social_type not in SocialKindChoices:
            raise ValidationError({'kind': '지원하지 않는 소셜 타입입니다.'})

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        code = validated_data['code']
        email = validated_data['email']
        social_type = validated_data['social_type']
        user, created = User.objects.get_or_create(email=email, defaults={'password': make_password(None)})

        if created:
            user_profile = Profile.objects.create(user=user, kind=social_type, code=code)
            user_profile.save()

        refresh = RefreshToken.for_user(user)
        return {
            'access': refresh.access_token,
            'refresh': refresh,
        }


class UserNicknameUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('nickname',)


class ProfileImageSerializer(serializers.ModelSerializer):
    image = serializers.FileField(required=False)

    class Meta:
        model = ProfileImage
        exclude = ('profile', )


class ProfileSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = (
            'profile_image', 'points', 'firebase_token', 'latitude', 'longitude', 'birthdate', 'age',
            'nationality', 'city', 'gender', 'blocked_profiles', 'likes', 'religion', 'smoke', 'height',
            'mbti', 'keywords', 'job', 'job_detail', 'school_level', 'school_name', 'school_major', 'profile_image',
        )

    def get_profile_image(self, obj):
        return ProfileImageSerializer(obj.profileimage_set.all(), many=True).data
