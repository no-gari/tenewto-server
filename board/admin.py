from django.contrib import admin

from .models import ApplyAvailable, Application


@admin.register(ApplyAvailable)
class ApplyAvailableAdmin(admin.ModelAdmin):
    pass


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    pass
