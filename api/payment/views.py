from django.db import transaction
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Product, Purchase, Entitlement, PurchaseEvent
from .serializers import PurchaseSerializer, EntitlementSerializer


# Placeholder verification helpers. Real implementation should call Apple/Google APIs.
def verify_ios_transaction(token: str) -> dict:
    return {
        'product_id': 'credit_10',
        'transaction_id': token,
        'environment': 'sandbox',
        'type': Product.Type.CONSUMABLE,
    }


def verify_android_purchase(token: str) -> dict:
    return {
        'product_id': 'credit_10',
        'transaction_id': token,
        'environment': 'sandbox',
        'type': Product.Type.CONSUMABLE,
    }


class IOSVerifyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.data.get('transaction_jws')
        if not token:
            return Response({'detail': 'transaction_jws required'}, status=400)
        data = verify_ios_transaction(token)
        with transaction.atomic():
            product, _ = Product.objects.get_or_create(
                store=Product.Store.IOS,
                product_id=data['product_id'],
                environment=data['environment'],
                defaults={'type': data['type']}
            )
            purchase, created = Purchase.objects.get_or_create(
                idempotency_key=data['transaction_id'],
                defaults={
                    'user': request.user,
                    'store': Product.Store.IOS,
                    'product': product,
                    'transaction_id': data['transaction_id'],
                    'purchased_at': timezone.now(),
                    'raw_summary': data,
                }
            )
            if created and product.type == Product.Type.CONSUMABLE:
                ent, _ = Entitlement.objects.select_for_update().get_or_create(
                    user=request.user, feature=product.product_id, defaults={'balance': 0}
                )
                ent.balance += 1
                ent.last_purchase = purchase
                ent.save()
            PurchaseEvent.objects.create(
                purchase=purchase,
                event_type=PurchaseEvent.EventType.BUY,
                source=PurchaseEvent.Source.API,
                result='ok'
            )
        return Response(PurchaseSerializer(purchase).data)


class AndroidVerifyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.data.get('purchase_token')
        if not token:
            return Response({'detail': 'purchase_token required'}, status=400)
        data = verify_android_purchase(token)
        with transaction.atomic():
            product, _ = Product.objects.get_or_create(
                store=Product.Store.ANDROID,
                product_id=data['product_id'],
                environment=data['environment'],
                defaults={'type': data['type']}
            )
            purchase, created = Purchase.objects.get_or_create(
                idempotency_key=data['transaction_id'],
                defaults={
                    'user': request.user,
                    'store': Product.Store.ANDROID,
                    'product': product,
                    'transaction_id': data['transaction_id'],
                    'purchased_at': timezone.now(),
                    'raw_summary': data,
                }
            )
            if created and product.type == Product.Type.CONSUMABLE:
                ent, _ = Entitlement.objects.select_for_update().get_or_create(
                    user=request.user, feature=product.product_id, defaults={'balance': 0}
                )
                ent.balance += 1
                ent.last_purchase = purchase
                ent.save()
            PurchaseEvent.objects.create(
                purchase=purchase,
                event_type=PurchaseEvent.EventType.BUY,
                source=PurchaseEvent.Source.API,
                result='ok'
            )
        return Response(PurchaseSerializer(purchase).data)


class EntitlementsMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ents = Entitlement.objects.filter(user=request.user)
        serializer = EntitlementSerializer(ents, many=True)
        return Response(serializer.data)


class AppStoreWebhookView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        transaction_id = request.data.get('transactionId')
        if not transaction_id:
            return Response({'detail': 'transactionId required'}, status=400)
        try:
            purchase = Purchase.objects.select_related('product', 'user').get(idempotency_key=transaction_id)
        except Purchase.DoesNotExist:
            return Response(status=404)
        with transaction.atomic():
            purchase.state = Purchase.State.VOIDED
            purchase.save()
            if purchase.product.type == Product.Type.CONSUMABLE:
                ent = Entitlement.objects.select_for_update().filter(
                    user=purchase.user, feature=purchase.product.product_id
                ).first()
                if ent:
                    ent.balance = max(0, ent.balance - 1)
                    ent.save()
            PurchaseEvent.objects.create(
                purchase=purchase,
                event_type=PurchaseEvent.EventType.REFUND,
                source=PurchaseEvent.Source.STORE_WEBHOOK,
                result='ok'
            )
        return Response({'status': 'ok'})


class GooglePlayWebhookView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        purchase_token = request.data.get('purchaseToken')
        if not purchase_token:
            return Response({'detail': 'purchaseToken required'}, status=400)
        try:
            purchase = Purchase.objects.select_related('product', 'user').get(idempotency_key=purchase_token)
        except Purchase.DoesNotExist:
            return Response(status=404)
        with transaction.atomic():
            purchase.state = Purchase.State.VOIDED
            purchase.save()
            if purchase.product.type == Product.Type.CONSUMABLE:
                ent = Entitlement.objects.select_for_update().filter(
                    user=purchase.user, feature=purchase.product.product_id
                ).first()
                if ent:
                    ent.balance = max(0, ent.balance - 1)
                    ent.save()
            PurchaseEvent.objects.create(
                purchase=purchase,
                event_type=PurchaseEvent.EventType.REFUND,
                source=PurchaseEvent.Source.STORE_WEBHOOK,
                result='ok'
            )
        return Response({'status': 'ok'})
