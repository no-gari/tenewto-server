from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from api.chat.models import Chat, Message
from api.chat.paginations import MessagePagination
from api.chat.serializers import ChatListSerializer, MessageListSerializer, MessageImageCreateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from api.chat.permissions import IsChatOwner
from api.notification.fcm import send_push


class ChatListView(ListAPIView):
    queryset = Chat.objects.prefetch_related('user_set').all()
    serializer_class = ChatListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user_set=user)


class MessageListView(ListAPIView):
    queryset = Message.objects.select_related('user').all()
    serializer_class = MessageListSerializer
    pagination_class = MessagePagination
    permission_classes = [IsChatOwner]

    def get_queryset(self):
        return self.queryset.filter(chat_id=self.kwargs['pk']).order_by('-id')


class MessageImageCreateView(APIView):
    permission_classes = [IsChatOwner]

    def post(self, request, pk):
        """
        채팅방에 이미지 전송 (텍스트 포함 가능)
        """
        chat = get_object_or_404(Chat.objects.prefetch_related('user_set'), pk=pk)

        serializer = MessageImageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message = serializer.save(chat=chat, user=request.user)
        chat.save()  # updated 갱신

        recipients = chat.user_set.exclude(id=request.user.id).values_list(
            "profile__firebase_token", flat=True
        )
        title = getattr(request.user.profile, "nickname", request.user.email)
        body = message.text or "이미지가 도착했습니다"
        for token in recipients:
            if token:
                send_push(
                    token,
                    title,
                    body,
                    {"chat_id": str(chat.id), "message_id": str(message.id)},
                )

        # 응답 직렬화
        out = MessageListSerializer(message, context={'request': request}).data

        # 채널 브로드캐스트
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            str(chat.id),
            {
                "type": "send_message",  # consumers.py에서 send_message 메서드로 처리
                "user": message.user.pk,
                "text": message.text,
                "image": message.message_image.url if message.message_image else None,
                "created": message.created.isoformat(),
                "message_id": message.pk
            }
        )

        return Response(out, status=status.HTTP_201_CREATED)
