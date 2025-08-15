from django.db import transaction
from rest_framework import serializers
from api.user.validators import validate_password
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from api.user.models import User, SocialKindChoices, Profile, ProfileImage
from django.core.exceptions import ValidationError as DjangoValidationError


class UserRegisterSerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
    password_confirm = serializers.CharField(write_only=True, required=False)

    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm', None)

        if 'password' in User.REGISTER_FIELDS:
            errors = {}
            # 비밀번호 검증
            if password != password_confirm:
                errors['password'] = ['비밀번호가 일치하지 않습니다.']
                errors['password_confirm'] = ['비밀번호가 일치하지 않습니다.']
            else:
                try:
                    validate_password(password)
                except DjangoValidationError as error:
                    errors['password'] = list(error)
                    errors['password_confirm'] = list(error)

            if errors:
                raise ValidationError(errors)

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create_user(
            **validated_data,
        )
        Profile.objects.create(user=user)

        refresh = RefreshToken.for_user(user)

        return {
            'access': refresh.access_token,
            'refresh': refresh,
        }


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


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImage
        exclude = ('profile', )

class ProfileSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField(read_only=True)
    avatar = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'nickname', 'avatar', 'created_at', 'points', 'firebase_token', 'latitude', 'longitude',
                  'birthdate', 'age', 'city', 'gender', 'religion', 'smoke', 'height', 'mbti', 'keywords',
                  'job', 'job_detail', 'school_level', 'school_name', 'school_major', 'hobby', 'profile_image')
        read_only_fields = ('id', 'created_at', 'points', 'profile_image')

    def get_profile_image(self, obj):
        return ProfileImageSerializer(obj.images.all(), many=True, context=self.context).data

    def get_avatar(self, obj):
        avatar_image = obj.images.filter(is_avatar=True).first()
        if avatar_image:
            avatar_image_url = ProfileImageSerializer(avatar_image, context=self.context).data.get('profile_image', None)
            return avatar_image_url
        return None
