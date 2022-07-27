# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect, HttpResponse


def home_index(request):
    return render(request, "web/home_index.html")
