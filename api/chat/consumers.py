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

        # datetime 객체를 ISO 형식 문자열로 변환하여 채널 레이어로 전송
        await self.channel_layer.group_send(
            self.chat_id,
            {
                'type': 'send_message',
                'user': message.user.pk,
                'text': message.text,
                'created': message.created.isoformat(),
            },
        )

    async def send_message(self, event):
        # 채널 레이어에서 받은 이벤트는 이미 직렬화 가능한 데이터
        await self.send(text_data=json.dumps({
            'user': event['user'],
            'text': event['text'],
            'created': event['created'],
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