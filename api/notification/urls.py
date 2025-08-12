from django.urls import path
from api.notification.views import (
    NotificationListView,
    NotificationDetailView,
    AdminPushView,
)

urlpatterns = [
    path('', NotificationListView.as_view()),
    path('<int:id>/', NotificationDetailView.as_view()),
    path('push/', AdminPushView.as_view()),
]
