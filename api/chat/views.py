from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from api.chat.models import Chat, Message
from api.chat.paginations import MessagePagination
from api.chat.permissions import IsChatOwner
from api.chat.serializers import ChatListSerializer, MessageListSerializer


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
        return self.queryset.filter(chat_id=self.kwargs['pk'])
