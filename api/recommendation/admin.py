from django.contrib import admin
from .models import RecommendationHistory


@admin.register(RecommendationHistory)
class RecommendationHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'recommended_user', 'viewed', 'liked', 'created']
    list_filter = ['viewed', 'liked', 'created']
    search_fields = ['user__email', 'recommended_user__email']
    ordering = ['-created']
