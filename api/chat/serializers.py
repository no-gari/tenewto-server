from rest_framework import serializers

from api.chat.models import Chat, Message
from api.user.models import User, Profile


class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['avatar', 'nickname', 'id']

    def get_id(self, obj):
        return obj.user.id


class OpponentSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['profile']


class ChatListSerializer(serializers.ModelSerializer):
    opponent_set = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    updated = serializers.DateTimeField()

    class Meta:
        model = Chat
        fields = ['id', 'opponent_set', 'last_message', 'updated']

    def get_opponent_set(self, obj):
        opponent_set = obj.user_set.exclude(pk=self.context['request'].user.pk).first()
        return OpponentSerializer(instance=opponent_set, context=self.context).data if opponent_set else None

    def get_last_message(self, obj):
        last_msg = obj.message_set.first()
        if not last_msg:
            return None
        return last_msg.text or '사진'


class MessageListSerializer(serializers.ModelSerializer):
    is_mine = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    created = serializers.DateTimeField(
        format='%Y-%m-%d %H:%M:%S%z',
    )

    class Meta:
        model = Message
        fields = ['id', 'is_mine', 'text', 'image', 'created']

    def get_is_mine(self, obj):
        return self.context['request'].user == obj.user

    def get_image(self, obj):
        if obj.message_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.message_image.url)
            return obj.message_image.url
        return None


class MessageImageCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source='message_image', write_only=True)
    # 응답은 리스트용과 동일하게
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    created = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'text', 'image', 'created']

    def create(self, validated_data):
        # view에서 chat, user를 주입
        return Message.objects.create(**validated_data)