from django.urls import path, include

urlpatterns = [
    path('user/', include('api.user.urls')),
    path('notification/', include('api.notification.urls')),
    path('matching/', include('api.matching.urls')),
    path('chat/', include('api.chat.urls')),
    path('', include('api.payment.urls')),
]
