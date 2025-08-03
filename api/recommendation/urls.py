from django.urls import path
from . import views

urlpatterns = [
    path('daily/', views.RecommendationAPIView.as_view(), name='daily_recommendations'),
    path('viewed/<int:user_id>/', views.mark_recommendation_viewed, name='mark_viewed'),
    path('liked/<int:user_id>/', views.mark_recommendation_liked, name='mark_liked'),
]
