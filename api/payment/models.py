from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import uuid


class PointTransaction(models.Model):
    STATUS_CHOICES = [
        ('pending', '대기중'),
        ('completed', '완료'),
        ('failed', '실패'),
        ('cancelled', '취소'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='point_transactions',
        verbose_name=_('사용자')
    )
    amount = models.PositiveIntegerField(verbose_name=_('충전 금액'))
    transaction_id = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('거래 ID'),
        help_text=_('외부 결제 서비스 거래 ID')
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('상태')
    )
    payment_method = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_('결제 수단')
    )
    failure_reason = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('실패 사유')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('생성일시'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('수정일시'))

    class Meta:
        verbose_name = _('포인트 충전')
        verbose_name_plural = _('포인트 충전')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['transaction_id']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.user} - {self.amount}P 충전 ({self.get_status_display()})"

    def clean(self):
        if self.amount <= 0:
            raise ValidationError(_('충전 금액은 0보다 커야 합니다.'))


class PointUsage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='point_usages',
        verbose_name=_('사용자')
    )
    amount = models.PositiveIntegerField(verbose_name=_('사용 금액'))
    description = models.CharField(
        max_length=200,
        verbose_name=_('사용 내역')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('생성일시'))

    class Meta:
        verbose_name = _('포인트 사용')
        verbose_name_plural = _('포인트 사용')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return f"{self.user} - {self.amount}P 사용 ({self.description})"

    def clean(self):
        if self.amount <= 0:
            raise ValidationError(_('사용 금액은 0보다 커야 합니다.'))