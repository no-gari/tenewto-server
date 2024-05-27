import json
from urllib.parse import parse_qsl, urlsplit

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db import transaction

from api.chat.models import Message, Chat


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']

        # 채팅방이 있는지 확인
        self.chat = await self.get_chat()
        if self.chat:
            if self.user in self.chat.user_set.all():
                await self.channel_layer.group_add(
                    self.chat_id,
                    self.channel_name,
                )
                await self.accept()
            else:
                await self.close()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_id,
            self.channel_name,
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        text = text_data_json['text']
        message = await self.create_message(text)

        await self.channel_layer.group_send(
            self.chat_id,
            {
                'type': 'send_message',
                'user': message.user.pk,
                'text': message.text,
                'created': message.created,
            },
        )

    async def send_message(self, event):
        sender_type = event['sender_type']
        text = event['text']
        created = event['created']
        await self.send(text_data=json.dumps({
            'senderType': sender_type,
            'text': text,
            'created': created,
        }))

    @database_sync_to_async
    def get_chat(self):
        try:
            chat = Chat.objects.prefetch_related('user_set').get(pk=self.chat_id)
        except Chat.DoesNotExist:
            chat = None
        return chat

    @database_sync_to_async
    @transaction.atomic
    def create_message(self, text):
        message = Message.objects.create(
            chat=self.chat,
            user=self.user,
            text=text,
        )

        self.chat.updated = message.created
        self.chat.save()
        return message

