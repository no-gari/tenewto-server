from rest_framework import serializers

from api.chat.models import Chat, Message
from api.user.models import User, Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['avatar', 'nickname']


class OpponentSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['profile']


class ChatListSerializer(serializers.ModelSerializer):
    opponent_set = serializers.SerializerMethodField()
    last_message = serializers.CharField(source='get_last_message')
    updated = serializers.DateTimeField()

    class Meta:
        model = Chat
        fields = ['id', 'opponent_set', 'last_message', 'updated']

    def get_opponent_set(self, obj):
        opponent_set = obj.user_set.exclude(pk=self.context['request'].user.pk)
        return OpponentSerializer(instance=opponent_set, many=True).data


class MessageListSerializer(serializers.ModelSerializer):
    is_mine = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['is_mine', 'text', 'image', 'created']

    def get_is_mine(self, obj):
        return self.context['request'].user == obj.user
