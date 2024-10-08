from django.urls import path, include
from django.shortcuts import render
from .views import info, apply, board_list, board_detail, apply_init, info_img

urlpatterns = [
    path('info/', info),
    path('info-img/', info_img),
    path('apply/', apply, name='apply'),
    path('privacy-agreement/', apply_init, name='privacy-agreement'),
    path('apply/success/', lambda request: render(request, 'success.html'), name='apply-success'),
    path('boards/', board_list, name='board_list'),
    path('board/<int:board_id>/', board_detail, name='board_detail'),
]
