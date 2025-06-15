from django.contrib import admin

from api.logger.models import EmailLog, PhoneLog


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('to', 'title', 'body', 'status')


@admin.register(PhoneLog)
class PhoneLogAdmin(admin.ModelAdmin):
    pass
