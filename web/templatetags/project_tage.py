# -*- coding:utf-8 -*-
# inclusion_tag ,传一个html模板文件
import re
from web import models
from django import template
from django.shortcuts import reverse

register = template.Library()


@register.inclusion_tag('web/inclusion/all_project_list.html')
def all_project_list(request):  # 前端调用先load该py文件，再引用函数。
    my_project_list = models.Project.objects.filter(creator=request.tracer.user)
    my_join_list = models.ProjectUser.objects.filter(participant=request.tracer.user)
    count = models.Project.objects.all().count()
    if count > 10:
        all_list = models.Project.objects.all().order_by("-id")[0, 10]  # 大于10倒序展示最后10个
    else:
        all_list = models.Project.objects.all().order_by("-id")  # 小于10倒序展示全部

    return {
        'my_create_list': my_project_list,  # 创建的项目对象
        'my_join_list': my_join_list,  # 参与的项目对象
        'all_list': all_list  # 全部的项目对象（最多显示10条）
    }


@register.inclusion_tag('web/inclusion/all_project_menu.html')
def all_project_menu(request):
    data_lst = [
        {"title": "概览", "url": reverse("manage_dashboard", kwargs={"project_id": request.tracer.project.id})},
        {"title": "问题", "url": reverse("manage_issue", kwargs={"project_id": request.tracer.project.id})},
        {"title": "统计", "url": reverse("manage_statistics", kwargs={"project_id": request.tracer.project.id})},
        {"title": "文件", "url": reverse("manage_file", kwargs={"project_id": request.tracer.project.id})},
        {"title": "wiki", "url": reverse("manage_wiki", kwargs={"project_id": request.tracer.project.id})},
        {"title": "设置", "url": reverse("manage_setting", kwargs={"project_id": request.tracer.project.id})},
    ]
    # reverse反向解析之后的值得到：/web/manage/1/dashboard/
    # print(reverse("manage_dashboard", kwargs={"project_id": request.tracer.project.id}))

    # 判断请求的url是哪一个
    for item in data_lst:
        if request.path_info.startswith(item.get("url")):
            # 请求的url开头匹配上，则增加一个元素
            item["class"] = "myactive"

    return {
        "data_lst": data_lst,
    }
