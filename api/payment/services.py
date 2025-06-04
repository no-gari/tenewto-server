from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import PointTransaction, PointUsage
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


class PointService:
    """포인트 관련 비즈니스 로직"""

    @staticmethod
    @transaction.atomic
    def process_payment_webhook(user_id, amount, transaction_id, **kwargs):
        """결제 웹훅 처리"""
        try:
            user = User.objects.select_for_update().get(id=user_id)
        except User.DoesNotExist:
            raise ValidationError("존재하지 않는 사용자입니다.")

        # 중복 거래 체크
        if PointTransaction.objects.filter(transaction_id=transaction_id).exists():
            raise ValidationError("이미 처리된 거래입니다.")

        status = kwargs.get('status', 'completed')
        payment_method = kwargs.get('payment_method', '')
        failure_reason = kwargs.get('failure_reason', '')

        # 거래 내역 생성
        point_transaction = PointTransaction.objects.create(
            user=user,
            amount=amount,
            transaction_id=transaction_id,
            status=status,
            payment_method=payment_method,
            failure_reason=failure_reason
        )

        # 결제 성공시에만 포인트 적립
        if status == 'completed':
            user.points += amount
            user.save()
            logger.info(f"포인트 충전 완료 - 사용자: {user.id}, 금액: {amount}P")

        return point_transaction

    @staticmethod
    @transaction.atomic
    def use_points(user, amount, description):
        """포인트 사용"""
        # 락을 걸고 사용자 정보 조회
        user = User.objects.select_for_update().get(id=user.id)

        # 포인트 잔액 확인
        if user.points < amount:
            raise ValidationError(f"포인트가 부족합니다. (보유: {user.points}P, 필요: {amount}P)")

        # 포인트 차감
        user.points -= amount
        user.save()

        # 사용 내역 생성
        usage = PointUsage.objects.create(
            user=user,
            amount=amount,
            description=description
        )

        logger.info(f"포인트 사용 완료 - 사용자: {user.id}, 금액: {amount}P, 내역: {description}")
        return usage