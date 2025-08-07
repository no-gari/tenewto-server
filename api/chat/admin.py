from django.contrib import admin
from api.chat.models import Chat, Message


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    pass


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'user', 'text', 'created')
    list_filter = ('created', 'user')
    search_fields = ('text', 'chat__id')