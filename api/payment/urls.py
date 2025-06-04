from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PointTransactionViewSet, PointUsageViewSet, PaymentWebhookView

router = DefaultRouter()
router.register(r'transactions', PointTransactionViewSet, basename='point-transactions')
router.register(r'usages', PointUsageViewSet, basename='point-usages')

urlpatterns = [
    # REST API
    path('', include(router.urls)),

    # 웹훅
    path('webhook/', PaymentWebhookView.as_view(), name='payment-webhook'),
]

# 생성되는 URL:
# GET    /api/points/transactions/     - 충전 내역 목록
# GET    /api/points/transactions/{id}/ - 충전 내역 상세
# GET    /api/points/usages/           - 사용 내역 목록
# POST   /api/points/usages/           - 포인트 사용
# GET    /api/points/usages/{id}/      - 사용 내역 상세
# POST   /api/points/webhook/          - 결제 웹훅