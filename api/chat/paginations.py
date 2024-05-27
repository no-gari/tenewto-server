from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class MessagePagination(LimitOffsetPagination):
    default_limit = 10
