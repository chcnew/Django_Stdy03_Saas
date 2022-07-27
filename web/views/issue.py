# -*- coding:utf-8 -*-
from web import models
from django.shortcuts import render
from web.myforms.issue import Issue
from django.http import JsonResponse


def manage_issue(request, project_id):
    if request.method != "POST":
        form = Issue(request)
        all_obj = models.Issue.objects.all()
        return render(request, "web/manage_issue.html", {"form": form, "all_obj": all_obj})
    form = Issue(request, data=request.POST)
    if form.is_valid():
        form.instance.project = request.tracer.project
        form.instance.creator = request.tracer.user
        form.save()
        return JsonResponse({"status": True})
    else:
        return JsonResponse({"status": False, "errors": form.errors})


def issue_add(request, project_id):
    if request.method != "POST":
        form = Issue(request)
        all_obj = models.Issue.objects.all()
        return render(request, "web/issue_add.html", {"form": form, "all_obj": all_obj})
