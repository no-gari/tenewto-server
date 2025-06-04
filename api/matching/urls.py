from django.urls import path
from .views import MatchViewSet, RecommendViewSet, LikeViewSet

urlpatterns = [
    # 좋아요 관련
    path('likes/', LikeViewSet.as_view({'get': 'list', 'post': 'create'}), name='likes'),
    path('likes/<uuid:pk>/', LikeViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}), name='like-detail'),
    path('likes/received/', LikeViewSet.as_view({'get': 'received'}), name='likes-received'),
    path('likes/<uuid:pk>/respond/', LikeViewSet.as_view({'post': 'respond'}), name='like-respond'),
    
    # 매칭 관련 (읽기 전용)
    path('matches/', MatchViewSet.as_view({'get': 'list'}), name='matches'),
    path('matches/<uuid:pk>/', MatchViewSet.as_view({'get': 'retrieve'}), name='match-detail'),
    
    # 추천
    path('recommend/', RecommendViewSet.as_view({'get': 'list'}), name='recommend'),
]