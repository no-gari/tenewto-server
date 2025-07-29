from rest_framework import serializers
from .models import DailyRecommendation, RecommendationSettings, RecommendationHistory
from api.user.serializers import UserSerializer


class DailyRecommendationSerializer(serializers.ModelSerializer):
    recommended_user = UserSerializer(read_only=True)

    class Meta:
        model = DailyRecommendation
        fields = ['id', 'recommended_user', 'date', 'created']
        read_only_fields = ['id', 'created']


class RecommendationSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendationSettings
        fields = ['id', 'daily_limit', 'is_active', 'created', 'updated']
        read_only_fields = ['id', 'created', 'updated']


class RecommendationHistorySerializer(serializers.ModelSerializer):
    recommended_user = UserSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = RecommendationHistory
        fields = ['id', 'user', 'recommended_user', 'viewed', 'liked', 'created']
        read_only_fields = ['id', 'user', 'recommended_user', 'created']


class RecommendationResponseSerializer(serializers.Serializer):
    """추천 결과 응답 시리얼라이저"""
    users = UserSerializer(many=True, read_only=True)
    remaining_count = serializers.IntegerField(read_only=True)
    next_reset_time = serializers.DateTimeField(read_only=True)
