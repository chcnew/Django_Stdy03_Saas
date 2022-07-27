# -*- coding:utf-8 -*-
from web import models
from django.http import JsonResponse
from web.myforms.project import DeleteProjectModelForm
from django.shortcuts import render, HttpResponse

from utils.tencent import cos


def manage_setting(request, project_id):
    return render(request, "web/manage_setting.html")


def setting_add(request, project_id):
    return render(request, "web/setting_add.html")


def setting_edit(request, project_id):
    return render(request, "web/setting_edit.html")


def setting_delete(request, project_id):
    """需要删除的项需要校验反馈"""
    if request.method != "POST":
        form = DeleteProjectModelForm(request, instance=request.tracer.project)
        return render(request, "web/setting_delete.html", {"form": form})
    else:
        form = DeleteProjectModelForm(request, data=request.POST, instance=request.tracer.project)
        if not form.is_valid():
            return JsonResponse({"status": False, "errors": form.errors})
        else:
            return JsonResponse({"status": True})  # 名称校验成功


def setting_delete_sure(request, project_id):
    """需要删除的项目已经校验确认后在此直接删除"""
    delete_obj = models.Project.objects.filter(project_name=request.POST.get("project_name"), creator=request.tracer.user).first()
    if not delete_obj:
        return JsonResponse({"status": False, "error": "项目不存在或已被删除！"})
    else:
        tf = cos.cos_delete_bucket(delete_obj.bucket)  # cos删除文件及碎片
        if tf:
            delete_obj.delete()
            return JsonResponse({"status": True})  # 删除成功
        else:
            return JsonResponse({"status": False, "error": "项目的Cos桶不存在！"})