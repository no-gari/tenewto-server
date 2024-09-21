from django.contrib import admin

from .models import ApplyAvailable, Application, Board


@admin.register(ApplyAvailable)
class ApplyAvailableAdmin(admin.ModelAdmin):
    pass


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    pass


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    pass
