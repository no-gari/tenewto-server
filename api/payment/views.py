from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import logging

from .models import PointTransaction, PointUsage
from .serializers import (
    PointTransactionSerializer,
    PointUsageSerializer,
    PaymentWebhookSerializer
)
from .services import PointService

logger = logging.getLogger(__name__)


class PointTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """포인트 충전 내역 조회"""
    serializer_class = PointTransactionSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['status']
    ordering = ['-created_at']

    def get_queryset(self):
        return PointTransaction.objects.filter(user=self.request.user)


class PointUsageViewSet(viewsets.ModelViewSet):
    """포인트 사용 내역"""
    serializer_class = PointUsageSerializer
    permission_classes = [IsAuthenticated]
    ordering = ['-created_at']

    def get_queryset(self):
        return PointUsage.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """포인트 사용"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data['amount']
        description = serializer.validated_data['description']

        try:
            usage = PointService.use_points(
                user=request.user,
                amount=amount,
                description=description
            )

            response_serializer = self.get_serializer(usage)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


@method_decorator(csrf_exempt, name='dispatch')
class PaymentWebhookView(APIView):
    """결제 서비스 웹훅"""
    permission_classes = []

    def post(self, request):
        """결제 완료 웹훅 처리"""
        serializer = PaymentWebhookSerializer(data=request.data)

        if not serializer.is_valid():
            logger.error(f"웹훅 데이터 검증 실패: {serializer.errors}")
            return Response(
                {'error': '잘못된 요청입니다.', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validated_data = serializer.validated_data
            point_transaction = PointService.process_payment_webhook(
                user_id=validated_data['user_id'],
                amount=validated_data['amount'],
                transaction_id=validated_data['transaction_id'],
                status=validated_data.get('status', 'completed'),
                payment_method=validated_data.get('payment_method', ''),
                failure_reason=validated_data.get('failure_reason', '')
            )

            return Response({
                'success': True,
                'message': '처리 완료',
                'transaction_id': point_transaction.transaction_id,
                'status': point_transaction.status
            }, status=status.HTTP_200_OK)

        except ValidationError as e:
            logger.error(f"웹훅 처리 실패: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"웹훅 처리 중 오류: {str(e)}")
            return Response(
                {'error': '서버 오류'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )