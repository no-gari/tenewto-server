from django.urls import path
from .views import (
    IOSVerifyView,
    AndroidVerifyView,
    EntitlementsMeView,
    AppStoreWebhookView,
    GooglePlayWebhookView,
)

urlpatterns = [
    path('iap/ios/verify/', IOSVerifyView.as_view()),
    path('iap/android/verify/', AndroidVerifyView.as_view()),
    path('iap/ios/notify/', AppStoreWebhookView.as_view()),
    path('iap/android/notify/', GooglePlayWebhookView.as_view()),
    path('entitlements/me/', EntitlementsMeView.as_view()),
]
