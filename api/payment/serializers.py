from rest_framework import serializers
from django.utils import timezone
from .models import PointTransaction, PointUsage


class PointTransactionSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = PointTransaction
        fields = [
            'id', 'amount', 'transaction_id', 'status', 'status_display',
            'payment_method', 'failure_reason', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'status', 'status_display', 'failure_reason',
            'created_at', 'updated_at'
        ]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("충전 금액은 0보다 커야 합니다.")
        return value


class PointUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointUsage
        fields = ['id', 'amount', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("사용 금액은 0보다 커야 합니다.")
        return value


class PaymentWebhookSerializer(serializers.Serializer):
    """결제 웹훅용 시리얼라이저"""
    user_id = serializers.UUIDField()
    amount = serializers.IntegerField(min_value=1)
    transaction_id = serializers.CharField(max_length=100)
    payment_method = serializers.CharField(max_length=50, required=False)
    status = serializers.ChoiceField(
        choices=['completed', 'failed', 'cancelled'],
        default='completed'
    )
    failure_reason = serializers.CharField(max_length=500, required=False, allow_blank=True)

    def validate_transaction_id(self, value):
        if PointTransaction.objects.filter(transaction_id=value).exists():
            raise serializers.ValidationError("이미 처리된 거래입니다.")
        return value