from api.notification.models import Notification
from django.contrib import admin


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    pass
