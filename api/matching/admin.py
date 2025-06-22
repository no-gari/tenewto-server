from django.contrib import admin
from .models import Like, Match, Block


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['from_user__email', 'to_user__email']


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['user1', 'user2', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user1__email', 'user2__email']


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ['blocker', 'blocked_user', 'reason', 'created_at']
    list_filter = ['created_at']
    search_fields = ['blocker__email', 'blocked_user__email', 'reason']
