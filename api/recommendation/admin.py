from django.contrib import admin
from .models import DailyRecommendation, RecommendationSettings, RecommendationHistory


@admin.register(DailyRecommendation)
class DailyRecommendationAdmin(admin.ModelAdmin):
    list_display = ['user', 'recommended_user', 'date', 'created']
    list_filter = ['date', 'created']
    search_fields = ['user__username', 'recommended_user__username']
    ordering = ['-created']


@admin.register(RecommendationSettings)
class RecommendationSettingsAdmin(admin.ModelAdmin):
    list_display = ['daily_limit', 'is_active', 'created', 'updated']
    list_filter = ['is_active']

    def has_add_permission(self, request):
        # 설정은 하나만 존재하도록 제한
        return not RecommendationSettings.objects.exists()


@admin.register(RecommendationHistory)
class RecommendationHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'recommended_user', 'viewed', 'liked', 'created']
    list_filter = ['viewed', 'liked', 'created']
    search_fields = ['user__username', 'recommended_user__username']
    ordering = ['-created']
