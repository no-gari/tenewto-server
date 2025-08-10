from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.user.views import UserSocialLoginView, ProfileDetailUpdateView, UserRegisterView, ProfileImageUploadView, \
    ProfileImageDeleteView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('social_login/', UserSocialLoginView.as_view()),
    path('email_signup/', UserRegisterView.as_view()),
    path('profile/', ProfileDetailUpdateView.as_view()),
    path('profile/image/', ProfileImageUploadView.as_view()),
    path('profile/image/<uuid:pk>/', ProfileImageDeleteView.as_view()),
]
