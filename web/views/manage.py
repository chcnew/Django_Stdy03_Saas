# -*- coding:utf-8 -*-
from django.shortcuts import render


def manage_dashboard(request, project_id):
    return render(request, "web/manage_dashboard.html")


def manage_statistics(request, project_id):
    return render(request, "web/manage_statistics.html")



