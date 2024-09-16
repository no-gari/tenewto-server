from django.urls import path, include
from django.shortcuts import render
from .views import info, apply

urlpatterns = [
    path('info/', info),
    path('apply/', apply, name='apply'),
    path('apply/success/', lambda request: render(request, 'success.html'), name='apply-success'),
]