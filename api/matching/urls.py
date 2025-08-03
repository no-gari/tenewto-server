from django.urls import path
from .views import MatchViewSet, RecommendViewSet, LikeViewSet, BlockViewSet

urlpatterns = [
    # 좋아요 관련
    path('likes/', LikeViewSet.as_view({'get': 'list', 'post': 'create'}), name='likes'),
    path('likes/<uuid:pk>/', LikeViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}), name='like-detail'),
    path('likes/received/', LikeViewSet.as_view({'get': 'received'}), name='likes-received'),
    path('likes/respond/<uuid:pk>/', LikeViewSet.as_view({'post': 'respond'}), name='like-respond'),
    
    # 차단 관련
    path('blocks/', BlockViewSet.as_view({'get': 'list', 'post': 'create'}), name='blocks'),
    path('blocks/<uuid:pk>/', BlockViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}), name='block-detail'),
    path('blocks/unblock/<uuid:pk>/', BlockViewSet.as_view({'delete': 'unblock'}), name='block-unblock'),
    path('blocks/blocked-users/', BlockViewSet.as_view({'get': 'blocked_users'}), name='blocked-users'),
    
    # 매칭 관련 (읽기 전용)
    path('matches/', MatchViewSet.as_view({'get': 'list'}), name='matches'),
    path('matches/<uuid:pk>/', MatchViewSet.as_view({'get': 'retrieve'}), name='match-detail'),
    
    # 추천
    path('recommend/', RecommendViewSet.as_view({'get': 'list'}), name='recommend'),
]