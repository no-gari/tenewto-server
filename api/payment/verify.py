import jwt
import time
import requests
from .models import Product
from django.conf import settings
from google.oauth2 import service_account
from googleapiclient.discovery import build

# ------------------------------
# iOS 결제 검증 (App Store Server API)
# ------------------------------


def _generate_apple_jwt():
    """Apple API 호출용 JWT 생성"""
    headers = {
        "alg": "ES256",
        "kid": settings.APPLE_KEY_ID
    }
    payload = {
        "iss": settings.APPLE_ISSUER_ID,
        "iat": int(time.time()),
        "exp": int(time.time()) + 1200,  # 20분
        "aud": "appstoreconnect-v1"
    }
    return jwt.encode(payload, settings.APPLE_PRIVATE_KEY, algorithm="ES256", headers=headers)


def verify_ios_transaction(transaction_id: str) -> dict:
    """
    App Store Server API로 transactionId 검증
    """
    token = _generate_apple_jwt()
    url = f"https://api.storekit.itunes.apple.com/inApps/v1/transactions/{transaction_id}"
    headers = {"Authorization": f"Bearer {token}"}

    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise ValueError(f"Apple API error: {resp.status_code} - {resp.text}")

    data = resp.json()
    # 참고: https://developer.apple.com/documentation/appstoreserverapi/get_transaction_info
    return {
        'product_id': data.get('productId'),
        'transaction_id': data.get('transactionId'),
        'environment': data.get('environment', 'production'),
        'type': Product.Type.CONSUMABLE  # 필요 시 productType에 따라 NON_CONSUMABLE 처리
    }


# ------------------------------
# Android 결제 검증 (Google Play Developer API)
# ------------------------------
def verify_android_purchase(purchase_token: str, product_id: str) -> dict:
    """
    Google Play Developer API로 purchaseToken 검증
    """
    creds = service_account.Credentials.from_service_account_file(
        settings.GOOGLE_SERVICE_ACCOUNT_FILE,
        scopes=['https://www.googleapis.com/auth/androidpublisher']
    )

    service = build('androidpublisher', 'v3', credentials=creds)
    result = service.purchases().products().get(
        packageName=settings.GOOGLE_PACKAGE_NAME,
        productId=product_id,
        token=purchase_token
    ).execute()

    # 참고: https://developers.google.com/android-publisher/api-ref/rest/v3/purchases.products
    purchase_state = result.get("purchaseState", 1)  # 0: 구매완료, 1: 취소, 2: 보류
    if purchase_state != 0:
        raise ValueError(f"Purchase not valid. State: {purchase_state}")

    return {
        'product_id': result.get('productId'),
        'transaction_id': result.get('orderId', purchase_token),
        'environment': 'production',  # 테스트 환경이면 'sandbox'
        'type': Product.Type.CONSUMABLE
    }