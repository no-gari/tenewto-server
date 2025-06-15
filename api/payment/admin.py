from api.payment.models import PointUsage, PointTransaction
from django.contrib import admin


@admin.register(PointUsage)
class PointUsageAdmin(admin.ModelAdmin):
    pass


@admin.register(PointTransaction)
class PointTransactionAdmin(admin.ModelAdmin):
    pass
