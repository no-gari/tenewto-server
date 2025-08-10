import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from api.chat.models import Message, Chat
from django.db import transaction


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']

        self.chat = await self.get_chat()
        if self.chat and await self.check_user_in_chat():
            await self.channel_layer.group_add(
                self.chat_id,
                self.channel_name,
            )
            await self.accept()
        else:
            await self.close()

    @database_sync_to_async
    def check_user_in_chat(self):
        return self.chat.user_set.filter(pk=self.user.pk).exists()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_id,
            self.channel_name,
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        text = text_data_json['text']
        message = await self.create_message(text)

        # 채널 레이어로 전송할 때 더 많은 정보 포함
        await self.channel_layer.group_send(
            self.chat_id,
            {
                'type': 'send_message',
                'user': message.user.pk,
                'text': message.text,
                'created': message.created.isoformat(),
                'message_id': message.pk,  # 메시지 ID도 포함
            },
        )

    async def send_message(self, event):
        # 현재 사용자가 메시지 작성자인지 확인
        is_mine = event['user'] == self.user.pk

        await self.send(text_data=json.dumps({
            'user': event['user'],
            'text': event['text'],
            'created': event['created'],
            'isMine': is_mine,  # 추가
        }))

    @database_sync_to_async
    def get_chat(self):
        try:
            return Chat.objects.prefetch_related('user_set').get(pk=self.chat_id)
        except Chat.DoesNotExist:
            return None

    @database_sync_to_async
    @transaction.atomic
    def create_message(self, text):
        message = Message.objects.create(
            chat=self.chat,
            user=self.user,
            text=text,
        )
        self.chat.save()
        return message