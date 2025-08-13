from api.payment.models import Product, Purchase, PurchaseEvent, Entitlement
from django.contrib import admin


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    pass


@admin.register(PurchaseEvent)
class PurchaseEventAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class EntitlementAdmin(admin.ModelAdmin):
    pass
