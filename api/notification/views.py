from rest_framework.generics import (
    UpdateAPIView,
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from api.notification.models import Notification
from api.notification.serializers import NotificationSerializer
from api.notification.fcm import send_push
from api.user.models import Profile


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10


class NotificationListView(ListAPIView):
    serializer_class = NotificationSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Notification.objects.all()


class NotificationDetailView(RetrieveAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.hits += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_object(self):
        return Notification.objects.get(id=self.kwargs['id'])


class AdminPushView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        """Send an FCM push to all users or a specific user."""
        title = request.data.get("title")
        body = request.data.get("body")
        user_id = request.data.get("user_id")
        data = request.data.get("data") or {}

        if not title or not body:
            return Response({"detail": "title and body are required"}, status=400)

        queryset = Profile.objects.exclude(firebase_token__isnull=True).exclude(
            firebase_token=""
        )
        if user_id:
            queryset = queryset.filter(user_id=user_id)

        count = 0
        for token in queryset.values_list("firebase_token", flat=True):
            send_push(token, title, body, data)
            count += 1

        return Response({"sent": count})
