from django.conf import settings
from django.db import models
from django.utils import timezone


class Product(models.Model):
    class Store(models.TextChoices):
        IOS = 'ios', 'iOS'
        ANDROID = 'android', 'Android'

    class Type(models.TextChoices):
        CONSUMABLE = 'consumable', 'Consumable'
        NON_CONSUMABLE = 'non_consumable', 'Non-consumable'

    store = models.CharField(max_length=10, choices=Store.choices)
    product_id = models.CharField(max_length=128)
    type = models.CharField(max_length=20, choices=Type.choices)
    environment = models.CharField(max_length=16, default='production')

    class Meta:
        unique_together = ('store', 'product_id', 'environment')
        verbose_name = '상품'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.store}:{self.product_id}"


class Purchase(models.Model):
    class State(models.TextChoices):
        PURCHASED = 'purchased', 'Purchased'
        VOIDED = 'voided', 'Voided'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    store = models.CharField(max_length=10, choices=Product.Store.choices)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    transaction_id = models.CharField(max_length=128)
    state = models.CharField(max_length=20, choices=State.choices, default=State.PURCHASED)
    purchased_at = models.DateTimeField(default=timezone.now)
    idempotency_key = models.CharField(max_length=128, unique=True)
    raw_summary = models.JSONField(default=dict, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['store', 'transaction_id']),
        ]
        verbose_name = '구매'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.user_id}:{self.transaction_id}"


class Entitlement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    feature = models.CharField(max_length=64)
    balance = models.PositiveIntegerField(default=0)
    last_purchase = models.ForeignKey(Purchase, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = ('user', 'feature')
        verbose_name = '권한'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.user_id}:{self.feature}={self.balance}"


class PurchaseEvent(models.Model):
    class EventType(models.TextChoices):
        BUY = 'buy', 'Buy'
        CONSUME = 'consume', 'Consume'
        REFUND = 'refund', 'Refund'
        REVOKE = 'revoke', 'Revoke'

    class Source(models.TextChoices):
        STORE_WEBHOOK = 'store_webhook', 'Store Webhook'
        CRON = 'cron', 'Cron'
        API = 'api', 'API'

    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=20, choices=EventType.choices)
    source = models.CharField(max_length=20, choices=Source.choices)
    result = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.purchase_id}:{self.event_type}"

    class Meta:
        verbose_name = '구매 내역'
        verbose_name_plural = verbose_name
