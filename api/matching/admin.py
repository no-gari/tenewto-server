from django.contrib import admin
from api.matching.models import Like, Match


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    pass
