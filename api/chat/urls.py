from django.urls import path

from api.chat.views import ChatListView, MessageListView, MessageImageCreateView

urlpatterns = [
    path('', ChatListView.as_view()),
    path('<int:pk>/message/', MessageListView.as_view()),
    path('<int:pk>/message/image/', MessageImageCreateView.as_view()),
]
