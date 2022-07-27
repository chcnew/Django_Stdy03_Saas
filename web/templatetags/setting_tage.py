# -*- coding:utf-8 -*-
from web import models
from django import template
from django.shortcuts import reverse

register = template.Library()


@register.inclusion_tag('web/inclusion/all_setting_menu.html')
def all_setting_menu(request):  # 前端调用先load该py文件，再引用函数。
    data_lst = [
        {"title": "全部项目", "url": reverse("manage_setting", kwargs={"project_id": request.tracer.project.id})},
        {"title": "新建项目", "url": reverse("setting_add", kwargs={"project_id": request.tracer.project.id})},
        {"title": "编辑项目", "url": reverse("setting_edit", kwargs={"project_id": request.tracer.project.id})},
        {"title": "删除项目", "url": reverse("setting_delete", kwargs={"project_id": request.tracer.project.id})},
    ]

    # 判断请求的url是哪一个
    for item in data_lst:
        if request.path_info.startswith(item.get("url")):
            # 请求的url开头匹配上，则增加一个元素
            item["class"] = True

    return {
        "data_lst": data_lst
    }
