from django.urls import path
from . import views

urlpatterns = [
    path('daily/', views.get_daily_recommendations, name='daily_recommendations'),
    path('viewed/<int:user_id>/', views.mark_recommendation_viewed, name='mark_viewed'),
    path('liked/<int:user_id>/', views.mark_recommendation_liked, name='mark_liked'),
    path('history/', views.get_recommendation_history, name='recommendation_history'),
]
