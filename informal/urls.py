# -*- coding:utf-8 -*-
from django.urls import path
from informal.views import account

urlpatterns = [
    path('user/login/', account.user_login),
    path('user/register/', account.user_register),
]
