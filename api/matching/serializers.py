from rest_framework import serializers
from .models import Match, Like
from api.user.serializers import ProfileSerializer

class LikeSerializer(serializers.ModelSerializer):
    to_user_profile = ProfileSerializer(source='to_user.profile', read_only=True)
    from_user_profile = ProfileSerializer(source='from_user.profile', read_only=True)
    
    class Meta:
        model = Like
        fields = ['id', 'from_user', 'to_user', 'status', 'created_at', 'updated_at', 
                 'to_user_profile', 'from_user_profile']
        read_only_fields = ['created_at', 'updated_at', 'from_user']

class MatchSerializer(serializers.ModelSerializer):
    user1_profile = ProfileSerializer(source='user1.profile', read_only=True)
    user2_profile = ProfileSerializer(source='user2.profile', read_only=True)
    other_user_profile = serializers.SerializerMethodField()
    
    class Meta:
        model = Match
        fields = ['id', 'user1', 'user2', 'created_at', 
                 'user1_profile', 'user2_profile', 'other_user_profile']
        read_only_fields = ['created_at']
    
    def get_other_user_profile(self, obj):
        """요청한 사용자가 아닌 상대방의 프로필 반환"""
        request = self.context.get('request')
        if request and request.user:
            if obj.user1 == request.user:
                return ProfileSerializer(obj.user2.profile).data
            else:
                return ProfileSerializer(obj.user1.profile).data
        return None

class LikeResponseSerializer(serializers.Serializer):
    """좋아요에 대한 응답(수락/거절) 시리얼라이저"""
    action = serializers.ChoiceField(choices=['accept', 'reject'])
    
    def validate_action(self, value):
        if value not in ['accept', 'reject']:
            raise serializers.ValidationError("action은 'accept' 또는 'reject'여야 합니다.")
        return value